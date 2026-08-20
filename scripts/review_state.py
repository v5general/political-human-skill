"""Activation-state executor: the only supported way to transition persona review status.

Subcommands (see core/activation_gate.md "Executor"):
  check   <persona_id>  Preflight. Emits JSON {decision: activate|confirm_prompt|blocked,
                        reasons, next_action}. Recovers interrupted transactions and
                        auto-invalidates incoherent states. Exit 1 when blocked.
  commit  <persona_id>  After a full technical/safety review passes (mechanical artifact
                        validation AND semantic validators/), stores the artifact hash and
                        moves all three status fields to `reviewed`.
  confirm <persona_id>  After explicit user approval, moves a valid `reviewed` persona to
                        `confirmed`. Never alters validation or hash fields.

All subcommands accept --persona-dir <path> for explicit external persona directories.
Never hand-edit latest_review_status, the persona.yaml mirrors, validation_status,
review_invalidated_by_modification, or reviewed_artifact_hash.

Concurrency contract: each command runs recovery, reads, decisions, and any transition
under one persona-local lock. confirm refuses when any interrupted-transaction evidence
or incoherence exists; commit always rebuilds state from the unconfirmed baseline.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT = SCRIPTS_DIR.parent
LOCAL_PACKAGE_DIR = ROOT / ".python-packages"
if LOCAL_PACKAGE_DIR.exists():
    sys.path.insert(0, str(LOCAL_PACKAGE_DIR))

import yaml  # noqa: E402

from persona_runtime_contracts import (  # noqa: E402
    PersonaContractError,
    activation_errors,
    activation_readiness_errors,
    compute_review_artifact_hash,
    load_json,
    load_persona,
    persona_directory_errors,
    resolve_persona_dir,
)

STATUSES = ("unconfirmed", "reviewed", "confirmed")
MIRROR_KEYS = ("creation_review_status", "last_review_status")
# Mirror line: key, value, optional quotes, optional trailing comment. Longest-first
# alternation is irrelevant here (keys are mutually exclusive anchors).
MIRROR_LINE = re.compile(
    r"^(\s*(?:creation_review_status|last_review_status)\s*:\s*[\"']?)"
    r"(unconfirmed|reviewed|confirmed)"
    r"([\"']?\s*(?:#.*)?)$"
)
LOCK_DIR = ".review_state.lock"  # dir containing an `owner` file with the holder PID
MARKER_FILE = ".review_txn.marker"
RESERVED_NAMES = frozenset({MARKER_FILE, "meta.json.review_stage", "persona.yaml.review_stage"})


class ExecutorError(RuntimeError):
    """Raised when a transition cannot be completed; the state stays fail-closed."""


def _fsync_dir(directory: Path) -> None:
    try:
        handle = os.open(str(directory), os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(handle)
    finally:
        os.close(handle)


def _pid_alive(pid: int) -> bool:
    """POSIX fallback: only a child we can reap counts as verifiably dead."""
    try:
        info = os.waitpid(pid, os.WNOHANG)
        return info == (0, 0)
    except OSError:
        return True  # unknown => conservatively alive


def _process_alive(pid: int) -> bool:
    """Best-effort liveness probe without psutil; conservative (unknown => alive)."""
    if sys.platform == "win32":
        try:
            import ctypes

            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            STILL_ACTIVE = 259
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            if not handle:
                return kernel32.GetLastError() != 87  # ERROR_INVALID_PID => verifiably dead
            try:
                code = ctypes.c_ulong()
                if kernel32.GetExitCodeProcess(handle, ctypes.byref(code)):
                    return code.value == STILL_ACTIVE
                return True
            finally:
                kernel32.CloseHandle(handle)
        except Exception:  # noqa: BLE001 - probe failure must not brick the executor
            return True
    return _pid_alive(pid)


class _PersonaLock:
    """Exclusive persona-local lock (atomic mkdir of one canonical directory) with an
    `owner` file recording the holder PID. A stale lock is reclaimed only when its
    recorded PID is verifiably not running; anything unknown stays fail-closed.
    Lock artifacts are excluded from the review hash walk (see persona_runtime_contracts)."""

    def __init__(self, directory: Path) -> None:
        self._path = directory / LOCK_DIR
        self._owned = False

    def __enter__(self) -> "_PersonaLock":
        try:
            self._path.mkdir()
        except FileExistsError:
            if not self._try_reclaim():
                raise ExecutorError(
                    f"persona lock held (owner unreadable or alive): {self._path}; "
                    "if no review_state process is running, remove that directory and retry"
                ) from None
            self._path.mkdir()
        (self._path / "owner").write_text(str(os.getpid()), encoding="ascii")
        self._owned = True
        return self

    def _try_reclaim(self) -> bool:
        try:
            pid = int((self._path / "owner").read_text(encoding="ascii").strip())
        except (OSError, ValueError):
            return False  # unreadable owner: fail closed, require manual removal
        if pid == os.getpid() or _process_alive(pid):
            return False
        try:
            (self._path / "owner").unlink()
            self._path.rmdir()
        except OSError:
            return False
        return True

    def __exit__(self, *exc_info: object) -> None:
        if self._owned:
            try:
                (self._path / "owner").unlink()
                self._path.rmdir()
            except OSError:
                pass


def _recover_interrupted_txn(directory: Path) -> str | None:
    """Remove reserved transaction artifacts. Caller must hold the lock; the presence
    of any of them invalidates all statuses (handled by the caller)."""
    recovered: set[str] = set()
    for name in sorted(RESERVED_NAMES):
        path = directory / name
        if path.is_file():
            path.unlink()
            recovered.add(name)
    return f"removed {sorted(recovered)}" if recovered else None


def _apply_meta_review_fields(meta: dict[str, Any], target: str, commit_hash: str | None = None) -> None:
    if target == "unconfirmed":
        meta["latest_review_status"] = "unconfirmed"
        meta["validation_status"] = "pending"
        meta["review_invalidated_by_modification"] = True
        meta["reviewed_artifact_hash"] = ""
    elif target == "reviewed":
        if not commit_hash:
            raise ExecutorError("transition to reviewed requires commit_hash")
        meta["latest_review_status"] = "reviewed"
        meta["validation_status"] = "passed"
        meta["review_invalidated_by_modification"] = False
        meta["reviewed_artifact_hash"] = commit_hash
    elif target == "confirmed":
        meta["latest_review_status"] = "confirmed"
    else:
        raise ExecutorError(f"unsupported status {target!r}")


def _mirror_semantic_values(persona: dict[str, Any]) -> list[str | None]:
    persona_meta = persona.get("meta") if isinstance(persona, dict) else None
    provenance = persona.get("source_provenance") if isinstance(persona, dict) else None
    return [
        persona_meta.get("creation_review_status") if isinstance(persona_meta, dict) else None,
        provenance.get("last_review_status") if isinstance(provenance, dict) else None,
    ]


def _rewrite_persona_mirrors(persona_text: str, target: str) -> str:
    lines = persona_text.splitlines(keepends=True)
    replaced = 0
    for index, line in enumerate(lines):
        bare = line.rstrip("\r\n")
        match = MIRROR_LINE.match(bare)
        if match is None:
            continue
        newline = "\r\n" if line.endswith("\r\n") else "\n"
        lines[index] = f"{match.group(1)}{target}{match.group(3)}{newline}"
        replaced += 1
    if replaced != 2:
        raise ExecutorError(
            f"expected exactly 2 review-status mirror lines in persona.yaml, rewrote {replaced}; "
            "expected meta.creation_review_status and source_provenance.last_review_status "
            "as standalone `key: \"status\"` lines"
        )
    return "".join(lines)


def _transition(directory: Path, target: str, commit_hash: str | None = None) -> None:
    """One atomic status transition across meta.json and both persona.yaml mirrors.

    Caller holds the lock. Marker -> staged+fsynced writes -> os.replace each ->
    dir fsync -> clear marker. A crash mid-transaction leaves the marker; the next
    locked run recovers and invalidates (fail closed).
    """
    meta = load_json(directory / "meta.json")
    with (directory / "persona.yaml").open("r", encoding="utf-8", newline="") as handle:
        persona_text = handle.read()

    before = yaml.safe_load(persona_text)
    _apply_meta_review_fields(meta, target, commit_hash)
    new_persona_text = _rewrite_persona_mirrors(persona_text, target)
    after = yaml.safe_load(new_persona_text)
    if _mirror_semantic_values(after) != [target, target]:
        raise ExecutorError("post-rewrite persona.yaml mirrors do not parse back to the target status")
    if before is not None and after is not None and before != after:
        # Only the two mirror values may differ between parses.
        patched_before = yaml.safe_load(_rewrite_persona_mirrors(persona_text, target))
        if patched_before != after:
            raise ExecutorError("persona.yaml rewrite changed more than the mirror values")

    marker = directory / MARKER_FILE
    with marker.open("w", encoding="utf-8") as handle:
        handle.write(json.dumps({"op": target, "ts": time.time()}, ensure_ascii=False))
        handle.flush()
        os.fsync(handle.fileno())
    _fsync_dir(directory)

    staged: list[tuple[Path, Path]] = []
    try:
        for name, payload in (
            ("meta.json", (json.dumps(meta, ensure_ascii=False, indent=2) + "\n").encode("utf-8")),
            ("persona.yaml", new_persona_text.encode("utf-8")),
        ):
            stage = directory / f"{name}.review_stage"
            with stage.open("wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            staged.append((stage, directory / name))
        for stage, final in staged:
            os.replace(stage, final)
        _fsync_dir(directory)
    finally:
        for stage, _ in staged:
            stage.unlink(missing_ok=True)
    marker.unlink(missing_ok=True)
    _fsync_dir(directory)


def _resolve(args: argparse.Namespace) -> Path:
    persona_dir = Path(args.persona_dir) if args.persona_dir else None
    return resolve_persona_dir(args.persona_id, persona_dir)


def _emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _remediation(args: argparse.Namespace) -> str:
    suffix = f" --persona-dir {args.persona_dir}" if args.persona_dir else ""
    return (
        "run the full technical/safety review (validators/), then: "
        f"uv run python scripts/review_state.py commit {args.persona_id}{suffix}"
    )


def _invalidate(directory: Path, reasons: list[str]) -> None:
    _transition(directory, "unconfirmed")
    reasons.append("state atomically invalidated to unconfirmed")


def cmd_check(args: argparse.Namespace) -> int:
    directory = _resolve(args)
    with _PersonaLock(directory):
        recovered = _recover_interrupted_txn(directory)
        persona = load_persona(directory / "persona.yaml")
        meta = load_json(directory / "meta.json")

        canonical = meta.get("latest_review_status")
        mirrors = _mirror_semantic_values(persona)
        coherent = canonical in STATUSES and all(m == canonical for m in mirrors)

        hash_valid = False
        if coherent and canonical in {"reviewed", "confirmed"}:
            try:
                current = compute_review_artifact_hash(directory, persona, meta)
                hash_valid = (
                    meta.get("validation_status") == "passed"
                    and meta.get("review_invalidated_by_modification") is False
                    and meta.get("reviewed_artifact_hash") == current
                )
            except Exception:  # noqa: BLE001 - any failure means not valid; fail closed below
                hash_valid = False

        reasons: list[str] = []
        decision = "blocked"

        if recovered or not coherent or (canonical in {"reviewed", "confirmed"} and not hash_valid):
            if recovered:
                reasons.append(f"interrupted transaction recovered ({recovered})")
            if not coherent:
                reasons.append(f"activation status mismatch canonical={canonical!r} mirrors={mirrors!r}")
            elif canonical in {"reviewed", "confirmed"} and not hash_valid:
                reasons.append("reviewed_artifact_hash does not match current artifacts; review is stale")
            _invalidate(directory, reasons)
            next_action = _remediation(args)
        elif canonical == "unconfirmed":
            reasons.append("no committed review (latest_review_status=unconfirmed)")
            next_action = _remediation(args)
        else:
            artifact_errors = persona_directory_errors(directory, args.persona_id)
            if artifact_errors:
                reasons.extend(artifact_errors)
                next_action = "fix artifact contract errors, then re-run check"
            elif canonical == "reviewed":
                decision = "confirm_prompt"
                suffix = f" --persona-dir {args.persona_dir}" if args.persona_dir else ""
                next_action = (
                    "present creation_review.md summary; on explicit user approval run: "
                    f"uv run python scripts/review_state.py confirm {args.persona_id}{suffix}"
                )
            else:
                decision = "activate"
                next_action = ""

        _emit(
            {
                "persona_id": args.persona_id,
                "persona_dir": str(directory),
                "decision": decision,
                "observed_status": canonical,
                "resulting_status": "unconfirmed" if "invalidated" in "".join(reasons) else canonical,
                "reasons": reasons,
                "next_action": next_action,
            }
        )
        return 0 if decision in {"activate", "confirm_prompt"} else 1


def cmd_commit(args: argparse.Namespace) -> int:
    directory = _resolve(args)
    with _PersonaLock(directory):
        _recover_interrupted_txn(directory)

        # 1. Idempotent reset to the coherent unconfirmed baseline.
        _transition(directory, "unconfirmed")

        # 2. Full mechanical artifact validation in that baseline state.
        errors = persona_directory_errors(directory, args.persona_id)
        if errors:
            _emit({"committed": False, "persona_id": args.persona_id, "errors": errors})
            return 1

        # 3. Store the hash and move all three statuses to reviewed.
        persona = load_persona(directory / "persona.yaml")
        meta = load_json(directory / "meta.json")
        digest = compute_review_artifact_hash(directory, persona, meta)
        _transition(directory, "reviewed", commit_hash=digest)

        # 4. Verify the committed state is coherent; roll back otherwise.
        persona = load_persona(directory / "persona.yaml")
        meta = load_json(directory / "meta.json")
        problems = activation_readiness_errors(directory, persona, meta)
        if problems:
            _transition(directory, "unconfirmed")
            _emit({"committed": False, "persona_id": args.persona_id, "errors": [*problems, "rolled back to unconfirmed"]})
            return 1
        _emit({"committed": True, "persona_id": args.persona_id, "reviewed_artifact_hash": digest})
        return 0


def cmd_confirm(args: argparse.Namespace) -> int:
    directory = _resolve(args)
    with _PersonaLock(directory):
        recovered = _recover_interrupted_txn(directory)
        persona = load_persona(directory / "persona.yaml")
        meta = load_json(directory / "meta.json")

        problems = activation_readiness_errors(directory, persona, meta)
        if (
            recovered
            or meta.get("latest_review_status") != "reviewed"
            or problems
        ):
            reasons = []
            if recovered:
                reasons.append(f"interrupted transaction recovered ({recovered}); refusing to confirm")
            if meta.get("latest_review_status") != "reviewed":
                reasons.append("confirm requires a valid reviewed state (run check first)")
            reasons.extend(problems)
            try:
                _invalidate(directory, reasons)
            except ExecutorError as exc:
                reasons.append(f"invalidation failed; state left as-is: {exc}")
            _emit({"confirmed": False, "persona_id": args.persona_id, "errors": reasons})
            return 1

        _transition(directory, "confirmed")
        persona = load_persona(directory / "persona.yaml")
        meta = load_json(directory / "meta.json")
        problems = activation_errors(directory, persona, meta)
        if problems:
            _transition(directory, "unconfirmed")
            _emit({"confirmed": False, "persona_id": args.persona_id, "errors": [*problems, "rolled back to unconfirmed"]})
            return 1
        _emit({"confirmed": True, "persona_id": args.persona_id})
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name, handler in (("check", cmd_check), ("commit", cmd_commit), ("confirm", cmd_confirm)):
        sub = subparsers.add_parser(name)
        sub.add_argument("persona_id")
        sub.add_argument("--persona-dir", help="Explicit external persona directory")
        sub.set_defaults(handler=handler)

    args = parser.parse_args()
    try:
        return args.handler(args)
    except (ExecutorError, PersonaContractError, OSError, ValueError) as exc:
        _emit({"error": str(exc), "persona_id": getattr(args, "persona_id", None)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
