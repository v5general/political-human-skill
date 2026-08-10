"""Run test-prompts.json through external generator and judge adapters.

Both commands receive one JSON object on stdin. The generator may write
arbitrary text. The judge must write JSON with pass, score, and findings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_PATH = ROOT / "test-prompts.json"
HASH_SKIP_DIRS = {".git", "__pycache__", ".python-packages", "semantic-runs"}


def parse_command(value: str) -> list[str]:
    try:
        command = json.loads(value)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(f"command must be a JSON array: {exc}") from exc
    if not isinstance(command, list) or not command or not all(isinstance(item, str) and item for item in command):
        raise argparse.ArgumentTypeError("command must be a non-empty JSON array of strings")
    return command


def load_prompts() -> list[dict[str, Any]]:
    with PROMPTS_PATH.open("r", encoding="utf-8") as handle:
        prompts = json.load(handle)
    if not isinstance(prompts, list):
        raise ValueError("test-prompts.json must contain an array")
    return [item for item in prompts if isinstance(item, dict)]


def as_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value


def run_adapter(command: list[str], payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    started = datetime.now(UTC)
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return {
            "started_at": started.isoformat(),
            "duration_seconds": (datetime.now(UTC) - started).total_seconds(),
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "started_at": started.isoformat(),
            "duration_seconds": (datetime.now(UTC) - started).total_seconds(),
            "returncode": None,
            "stdout": as_text(exc.stdout),
            "stderr": as_text(exc.stderr),
            "timed_out": True,
        }


def git_revision() -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def git_worktree_status() -> str | None:
    completed = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    return completed.stdout if completed.returncode == 0 else None


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repository_content_hash() -> str:
    digest = hashlib.sha256()
    paths = [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not any(part in HASH_SKIP_DIRS for part in path.relative_to(ROOT).parts)
    ]
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def parse_judgment(stdout: str) -> dict[str, Any]:
    try:
        judgment = json.loads(stdout)
    except json.JSONDecodeError as exc:
        return {"pass": False, "score": 0, "findings": [f"judge output was not JSON: {exc}"]}
    valid = (
        isinstance(judgment, dict)
        and isinstance(judgment.get("pass"), bool)
        and isinstance(judgment.get("score"), (int, float))
        and 0 <= judgment["score"] <= 100
        and isinstance(judgment.get("findings"), list)
        and all(isinstance(item, str) for item in judgment["findings"])
    )
    if not valid:
        return {"pass": False, "score": 0, "findings": ["judge JSON violated the required schema"]}
    return judgment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generator-command", type=parse_command, help="JSON array command; reads request JSON on stdin")
    parser.add_argument("--judge-command", type=parse_command, help="JSON array command; reads grading JSON on stdin")
    parser.add_argument("--model-id", help="Exact generator model identifier recorded in results")
    parser.add_argument("--judge-model-id", help="Exact judge model identifier recorded in results")
    parser.add_argument("--runtime-id", help="Host/runtime version recorded in results")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--id", action="append", dest="ids", help="Run only this test id; repeatable")
    parser.add_argument("--category", action="append", dest="categories", help="Run only this category; repeatable")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--list", action="store_true", help="List selected tests without invoking adapters")
    args = parser.parse_args()

    prompts = load_prompts()
    if args.ids:
        requested = set(args.ids)
        prompts = [item for item in prompts if item.get("id") in requested]
        missing = requested - {str(item.get("id")) for item in prompts}
        if missing:
            parser.error(f"unknown test ids: {', '.join(sorted(missing))}")
    if args.categories:
        categories = set(args.categories)
        prompts = [item for item in prompts if item.get("category") in categories]

    if not prompts:
        parser.error("no tests selected")

    if args.list:
        for item in prompts:
            print(f"{item.get('id')}\t{item.get('category', 'uncategorized')}")
        return 0

    required = {
        "--generator-command": args.generator_command,
        "--judge-command": args.judge_command,
        "--model-id": args.model_id,
        "--judge-model-id": args.judge_model_id,
        "--runtime-id": args.runtime_id,
    }
    missing_args = [name for name, value in required.items() if value is None]
    if missing_args:
        parser.error(f"semantic execution requires: {', '.join(missing_args)}")

    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_path = args.output or ROOT / "quality" / "semantic-runs" / f"{run_id}.jsonl"
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    metadata = {
        "run_id": run_id,
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "git_revision": git_revision(),
        "git_worktree_status": git_worktree_status(),
        "repository_content_hash": repository_content_hash(),
        "prompt_suite_sha256": file_sha256(PROMPTS_PATH),
        "python": sys.version,
        "platform": platform.platform(),
        "model_id": args.model_id,
        "judge_model_id": args.judge_model_id,
        "runtime_id": args.runtime_id,
        "seed": args.seed,
        "generator_command": args.generator_command,
        "judge_command": args.judge_command,
    }
    failures = 0

    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps({"type": "run_metadata", **metadata}, ensure_ascii=False) + "\n")
        for test in prompts:
            test_id = str(test.get("id"))
            inputs = test.get("prompt_sequence") or [test.get("prompt")]
            outputs: list[str] = []
            generator_calls: list[dict[str, Any]] = []
            for step, prompt in enumerate(inputs):
                request = {
                    "test_id": test_id,
                    "step": step,
                    "seed": args.seed,
                    "prompt": prompt,
                    "prior_outputs": outputs,
                }
                call = run_adapter(args.generator_command, request, args.timeout)
                generator_calls.append(call)
                outputs.append(str(call["stdout"]))
                if call["returncode"] != 0 or call["timed_out"]:
                    break

            judge_payload = {
                "test": test,
                "raw_outputs": outputs,
                "generator_calls": generator_calls,
                "validator_documents": {
                    name: (ROOT / name).read_text(encoding="utf-8")
                    for name in test.get("validators", [])
                    if isinstance(name, str) and (ROOT / name).is_file()
                },
                "grading_contract": {
                    "required_output": {"pass": "boolean", "score": "0-100", "findings": ["string"]},
                    "instruction": "Grade only against expected behavior, must_not, hard_gates, and referenced validators.",
                },
            }
            judge_call = run_adapter(args.judge_command, judge_payload, args.timeout)
            judgment = parse_judgment(str(judge_call["stdout"]))
            case_passed = (
                all(call["returncode"] == 0 and not call["timed_out"] for call in generator_calls)
                and judge_call["returncode"] == 0
                and not judge_call["timed_out"]
                and judgment["pass"]
            )
            if not case_passed:
                failures += 1
            handle.write(
                json.dumps(
                    {
                        "type": "test_result",
                        "run_id": run_id,
                        "test_id": test_id,
                        "category": test.get("category"),
                        "input": inputs,
                        "raw_outputs": outputs,
                        "generator_calls": generator_calls,
                        "judge_call": judge_call,
                        "judgment": judgment,
                        "passed": case_passed,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            print(f"{'PASS' if case_passed else 'FAIL'} {test_id} score={judgment['score']}")

        handle.write(
            json.dumps(
                {"type": "run_summary", "run_id": run_id, "total": len(prompts), "failures": failures},
                ensure_ascii=False,
            )
            + "\n"
        )

    print(f"Results: {output_path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
