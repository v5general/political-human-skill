"""Executable persona resolution, integrity, activation, and state contracts."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANAGED_ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9_-]*")
MUTABLE_FILES = {"memory.json", "relationship.json"}
ACTIVATION_STATUSES = {"unconfirmed", "reviewed", "confirmed"}
SAFETY_STATUSES = {"PASS", "safe_conversion"}
SOURCE_REPORT_BY_TYPE = {
    "original_fictional_persona": "original_persona_source_report.md",
    "historical_inference": "historical_source_report.md",
    "historical_archetype_conversion": "historical_source_report.md",
    "modern_real_figure_archetype_extraction": "modern_real_figure_public_source_report.md",
    "composite_archetype": "composite_archetype_source_report.md",
}
BASE_PERSONA_FILES = {
    "persona.yaml",
    "runtime_card.md",
    "SKILL.md",
    "relationship.json",
    "memory.json",
    "examples.md",
    "creation_review.md",
    "meta.json",
}
BASE_DIALOGUE_FILES = {
    "README.md",
    "casual_private.md",
    "public_interview.md",
    "strategy_room.md",
    "confrontation.md",
    "trust_low.md",
    "trust_high.md",
    "committee_debate.md",
}


class PersonaContractError(ValueError):
    """Raised when a persona path or identity violates a fail-closed contract."""


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_persona(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def bind_identity_errors(directory: Path, requested_id: str, persona: Any, meta: Any) -> list[str]:
    errors: list[str] = []
    persona_meta = persona.get("meta") if isinstance(persona, dict) else None
    identities = {
        "directory name": directory.name,
        "meta.json.persona_id": meta.get("persona_id") if isinstance(meta, dict) else None,
        "meta.json.slug": meta.get("slug") if isinstance(meta, dict) else None,
        "persona.yaml.meta.persona_id": persona_meta.get("persona_id") if isinstance(persona_meta, dict) else None,
        "persona.yaml.meta.slug": persona_meta.get("slug") if isinstance(persona_meta, dict) else None,
    }
    for label, value in identities.items():
        if value != requested_id:
            errors.append(f"{label} must equal requested persona_id {requested_id!r}, got {value!r}")
    return errors


def resolve_persona_dir(persona_id: str, persona_dir: Path | None = None, root: Path = ROOT) -> Path:
    """Resolve one direct managed child or one explicit external directory."""
    if not isinstance(persona_id, str) or MANAGED_ID_PATTERN.fullmatch(persona_id) is None:
        raise PersonaContractError("persona_id must match [a-z0-9][a-z0-9_-]*")

    if persona_dir is not None:
        candidate = persona_dir.expanduser()
        if candidate.is_symlink():
            raise PersonaContractError("explicit persona_dir cannot be a symlink")
        try:
            resolved = candidate.resolve(strict=True)
        except OSError as exc:
            raise PersonaContractError(f"explicit persona_dir is unavailable: {exc}") from exc
        if not resolved.is_dir():
            raise PersonaContractError("explicit persona_dir must be a directory")
        candidates = [resolved]
    else:
        candidates = []
        for managed_root in (root / "user_generated" / "personas", root / "personas" / "examples"):
            if not managed_root.exists():
                continue
            resolved_root = managed_root.resolve(strict=True)
            candidate = managed_root / persona_id
            if not candidate.exists():
                continue
            if candidate.is_symlink():
                raise PersonaContractError(f"managed persona directory cannot be a symlink: {candidate}")
            resolved = candidate.resolve(strict=True)
            if resolved.parent != resolved_root:
                raise PersonaContractError(f"managed persona must be a direct child of {managed_root}")
            candidates.append(resolved)
        if not candidates:
            raise PersonaContractError(f"persona not found: {persona_id}")
        if len(candidates) > 1:
            raise PersonaContractError(f"persona_id is ambiguous across managed roots: {persona_id}")

    resolved = candidates[0]
    persona_path = resolved / "persona.yaml"
    meta_path = resolved / "meta.json"
    if not persona_path.is_file() or not meta_path.is_file():
        raise PersonaContractError("persona_dir must contain regular persona.yaml and meta.json files")
    if persona_path.is_symlink() or meta_path.is_symlink():
        raise PersonaContractError("persona.yaml and meta.json cannot be symlinks")
    persona = load_persona(persona_path)
    meta = load_json(meta_path)
    errors = bind_identity_errors(resolved, persona_id, persona, meta)
    if errors:
        raise PersonaContractError("; ".join(errors))
    return resolved


def compute_review_artifact_hash(directory: Path, persona: dict[str, Any], meta: dict[str, Any]) -> str:
    """Hash immutable persona artifacts using the activation-gate byte contract."""
    normalized_persona = json.loads(json.dumps(persona, ensure_ascii=False))
    persona_meta = normalized_persona.get("meta")
    if isinstance(persona_meta, dict):
        persona_meta["creation_review_status"] = "unconfirmed"
    provenance = normalized_persona.get("source_provenance")
    if isinstance(provenance, dict):
        provenance["last_review_status"] = "unconfirmed"

    normalized_meta = json.loads(json.dumps(meta, ensure_ascii=False))
    normalized_meta.update(
        {
            "latest_review_status": "unconfirmed",
            "validation_status": "pending",
            "review_invalidated_by_modification": True,
            "reviewed_artifact_hash": "",
        }
    )
    normalized_content = {
        "meta.json": canonical_json_bytes(normalized_meta),
        "persona.yaml": canonical_json_bytes(normalized_persona),
    }

    if directory.is_symlink():
        raise PersonaContractError(f"persona_dir cannot be a symlink: {directory}")
    resolved_root = directory.resolve(strict=True)
    artifact_paths: list[Path] = []
    for path in directory.rglob("*"):
        if path.is_symlink():
            raise PersonaContractError(f"symlink is not allowed in persona artifact: {path}")
        resolved = path.resolve(strict=True)
        if not resolved.is_relative_to(resolved_root):
            raise PersonaContractError(f"persona artifact resolves outside persona_dir: {path}")
        relative = path.relative_to(directory).as_posix()
        if path.is_file() and relative not in MUTABLE_FILES:
            artifact_paths.append(path)

    digest = hashlib.sha256()
    for path in sorted(artifact_paths, key=lambda item: item.relative_to(directory).as_posix()):
        relative = path.relative_to(directory).as_posix()
        content = normalized_content[relative] if relative in normalized_content else path.read_bytes()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(content)
        digest.update(b"\0")
    return digest.hexdigest()


def activation_readiness_errors(directory: Path, persona: dict[str, Any], meta: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    persona_meta = persona.get("meta")
    provenance = persona.get("source_provenance")
    canonical_status = meta.get("latest_review_status")
    mirrors = [
        persona_meta.get("creation_review_status") if isinstance(persona_meta, dict) else None,
        provenance.get("last_review_status") if isinstance(provenance, dict) else None,
    ]
    if canonical_status not in ACTIVATION_STATUSES or any(status != canonical_status for status in mirrors):
        errors.append(f"activation status mismatch canonical={canonical_status!r} mirrors={mirrors!r}")

    canonical_safety = meta.get("safety_status")
    safety_mirror = persona_meta.get("safety_status") if isinstance(persona_meta, dict) else None
    if canonical_safety not in SAFETY_STATUSES or safety_mirror != canonical_safety:
        errors.append(f"safety status mismatch canonical={canonical_safety!r} mirror={safety_mirror!r}")

    validation_status = meta.get("validation_status")
    invalidated = meta.get("review_invalidated_by_modification")
    reviewed_hash = meta.get("reviewed_artifact_hash")
    if canonical_status == "unconfirmed":
        readiness_ok = validation_status == "pending" and invalidated is True and reviewed_hash == ""
    elif canonical_status in {"reviewed", "confirmed"}:
        try:
            current_hash = compute_review_artifact_hash(directory, persona, meta)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"artifact hash computation failed: {exc}")
            current_hash = None
        readiness_ok = (
            validation_status == "passed"
            and invalidated is False
            and isinstance(reviewed_hash, str)
            and reviewed_hash == current_hash
        )
    else:
        readiness_ok = False
    if not readiness_ok:
        errors.append(
            f"review readiness incoherent status={canonical_status!r} validation={validation_status!r} "
            f"invalidated={invalidated!r} hash={reviewed_hash!r}"
        )
    return errors


def activation_errors(directory: Path, persona: dict[str, Any], meta: dict[str, Any]) -> list[str]:
    errors = activation_readiness_errors(directory, persona, meta)
    if meta.get("latest_review_status") != "confirmed":
        errors.append("persona activation requires latest_review_status=confirmed")
    return errors


def schema_errors(payload: Any, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    return [
        f"{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda item: list(item.path))
    ]


def mutable_state_errors(directory: Path, persona_id: str) -> tuple[list[str], Any, Any]:
    errors: list[str] = []
    memory = load_json(directory / "memory.json")
    relationship = load_json(directory / "relationship.json")
    errors.extend(f"memory.json {error}" for error in schema_errors(memory, ROOT / "templates" / "memory_schema.json"))
    errors.extend(
        f"relationship.json {error}"
        for error in schema_errors(relationship, ROOT / "templates" / "relationship_schema.json")
    )
    if isinstance(memory, dict) and memory.get("persona_id") != persona_id:
        errors.append("memory.json persona_id does not match resolved persona")
    if isinstance(relationship, dict) and relationship.get("persona_id") != persona_id:
        errors.append("relationship.json persona_id does not match resolved persona")
    return errors, memory, relationship


def persona_directory_errors(directory: Path, requested_id: str) -> list[str]:
    """Validate the shared artifact contract for built-in, generated, or external personas."""
    errors: list[str] = []
    try:
        resolved = resolve_persona_dir(requested_id, directory)
        persona = load_persona(resolved / "persona.yaml")
        meta = load_json(resolved / "meta.json")
    except (OSError, ValueError) as exc:
        return [f"persona resolution failed: {exc}"]

    for name in sorted(BASE_PERSONA_FILES):
        if not (resolved / name).is_file() or (resolved / name).is_symlink():
            errors.append(f"missing regular artifact: {name}")

    source_type = meta.get("source_type") if isinstance(meta, dict) else None
    source_report = SOURCE_REPORT_BY_TYPE.get(source_type)
    if source_report is None:
        errors.append(f"unsupported source_type: {source_type!r}")
    elif not (resolved / source_report).is_file():
        errors.append(f"missing source report for {source_type}: {source_report}")

    dialogue_dir = resolved / "dialogue_samples"
    for name in sorted(BASE_DIALOGUE_FILES):
        if not (dialogue_dir / name).is_file():
            errors.append(f"missing dialogue sample: dialogue_samples/{name}")
    if isinstance(meta, dict) and meta.get("integration_target") == "absolute_majority":
        if not (dialogue_dir / "game_action.json").is_file():
            errors.append("Absolute Majority persona requires dialogue_samples/game_action.json")

    if not isinstance(persona, dict) or not isinstance(meta, dict):
        return errors + ["persona.yaml and meta.json must parse as mappings"]
    errors.extend(bind_identity_errors(resolved, requested_id, persona, meta))
    state_errors, _, _ = mutable_state_errors(resolved, requested_id)
    errors.extend(state_errors)
    errors.extend(activation_readiness_errors(resolved, persona, meta))

    persona_meta = persona.get("meta")
    provenance = persona.get("source_provenance")
    if not isinstance(persona_meta, dict) or persona_meta.get("source_type") != source_type:
        errors.append("persona.yaml meta.source_type must match meta.json source_type")
    if not isinstance(provenance, dict) or provenance.get("source_type") != source_type:
        errors.append("persona.yaml source_provenance.source_type must match meta.json source_type")
    elif provenance.get("modification_review_required") is not True:
        errors.append("source_provenance.modification_review_required must be true")
    if meta.get("activation_requires_user_confirmation") is not True:
        errors.append("activation_requires_user_confirmation must be true")

    if source_type in {"historical_inference", "historical_archetype_conversion"}:
        if not meta.get("source_figure"):
            errors.append("historical persona requires meta.json source_figure")
        temperament = persona.get("inferred_temperamental_pattern")
        if temperament is None and isinstance(persona.get("human_core"), dict):
            temperament = persona["human_core"].get("inferred_temperamental_pattern")
        if not isinstance(temperament, dict) or not temperament:
            errors.append("historical persona requires inferred_temperamental_pattern")
    if source_type in {"original_fictional_persona", "historical_inference", "historical_archetype_conversion"}:
        history = persona.get("human_core", {}).get("formative_life_history")
        history_fields = {
            "class_origin",
            "youth_observations",
            "intellectual_formation",
            "stance_formation_logic",
            "class_relation",
            "alternative_paths_note",
        }
        if not isinstance(history, dict) or not history_fields.issubset(history):
            errors.append("formative_life_history is incomplete")
    if source_type == "modern_real_figure_archetype_extraction":
        if meta.get("de_identified") is not True or meta.get("real_person_roleplay_allowed") is not False:
            errors.append("modern-real persona requires de-identification safety flags")
        removed = provenance.get("removed_fingerprints") if isinstance(provenance, dict) else None
        if not isinstance(removed, list) or not removed:
            errors.append("modern-real persona requires non-empty removed_fingerprints")
    return errors
