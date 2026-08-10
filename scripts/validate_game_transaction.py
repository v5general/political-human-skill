"""Fail-closed validation for one Absolute Majority persona transaction."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from persona_runtime_contracts import (
    ROOT,
    PersonaContractError,
    activation_errors,
    load_json,
    load_persona,
    mutable_state_errors,
    resolve_persona_dir,
    schema_errors,
)
from validate_game_output import validate_game_output

AXES = ("familiarity", "trust", "affection", "respect", "caution", "dependency")


def clamp(value: float) -> float:
    return max(0, min(100, value))


def validate_game_transaction(
    input_payload: Any,
    output_payload: Any,
    explicit_persona_dir: Path | None = None,
) -> dict[str, Any]:
    """Validate activation, immutable input/output, and projected mutable writes."""
    errors = schema_errors(input_payload, ROOT / "game_adapter" / "absolute_majority_input_schema.json")
    if errors or not isinstance(input_payload, dict):
        return {"valid": False, "errors": [f"input {error}" for error in errors]}

    persona_id = input_payload["persona_id"]
    try:
        persona_dir = resolve_persona_dir(persona_id, explicit_persona_dir)
        persona = load_persona(persona_dir / "persona.yaml")
        meta = load_json(persona_dir / "meta.json")
    except (OSError, ValueError, PersonaContractError) as exc:
        return {"valid": False, "errors": [f"persona resolution failed: {exc}"]}

    errors = activation_errors(persona_dir, persona, meta)
    if errors:
        return {"valid": False, "errors": [f"activation {error}" for error in errors]}

    try:
        state_errors, memory, relationship = mutable_state_errors(persona_dir, persona_id)
    except (OSError, ValueError) as exc:
        return {"valid": False, "errors": [f"mutable state load failed: {exc}"]}
    errors.extend(state_errors)
    errors.extend(validate_game_output(input_payload, output_payload))
    if errors:
        return {"valid": False, "errors": errors}

    assert isinstance(memory, dict) and isinstance(relationship, dict) and isinstance(output_payload, dict)
    input_relationship = input_payload["current_relationship"]
    stored_axes = relationship["relationship_axes"]
    for axis in AXES:
        if input_relationship[axis] != stored_axes[axis]:
            errors.append(f"input current_relationship/{axis} does not match stored relationship state")
    if errors:
        return {"valid": False, "errors": errors}

    relationship_after = json.loads(json.dumps(relationship, ensure_ascii=False))
    delta = output_payload["relationship_delta"]
    for axis in AXES:
        relationship_after["relationship_axes"][axis] = clamp(stored_axes[axis] + delta.get(axis, 0))
    relationship_after["relationship_history"].append(
        {
            "event_id": input_payload["event_id"],
            "timestamp": "",
            "summary": f"Selected {output_payload['selected_action']} for {input_payload['event_type']}",
            "delta": delta,
        }
    )

    memory_after = json.loads(json.dumps(memory, ensure_ascii=False))
    for index, summary in enumerate(output_payload["memory_write"]):
        memory_after["episodic_memory"].append(
            {
                "id": f"{input_payload['event_id']}:game:{index}",
                "timestamp": "",
                "occasion": input_payload["event_type"],
                "summary": summary,
                "user_attitude_observed": input_payload["player_instruction"],
                "persona_disclosed": "",
                "inference_level": "documented",
                "emotional_weight": 0,
            }
        )

    errors.extend(
        f"projected memory.json {error}"
        for error in schema_errors(memory_after, ROOT / "templates" / "memory_schema.json")
    )
    errors.extend(
        f"projected relationship.json {error}"
        for error in schema_errors(relationship_after, ROOT / "templates" / "relationship_schema.json")
    )
    return {
        "valid": not errors,
        "errors": errors,
        "persona_dir": str(persona_dir),
        "state_patch": {"memory.json": memory_after, "relationship.json": relationship_after} if not errors else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--persona-dir", type=Path, help="Explicit external persona directory; omit for managed resolution")
    args = parser.parse_args()
    if bool(args.input) != bool(args.output):
        parser.error("--input and --output must be supplied together")
    if args.input:
        input_payload = load_json(args.input)
        output_payload = load_json(args.output)
    else:
        envelope = json.load(sys.stdin)
        if not isinstance(envelope, dict):
            parser.error("stdin must be an object with input and output")
        input_payload = envelope.get("input")
        output_payload = envelope.get("output")
    result = validate_game_transaction(input_payload, output_payload, args.persona_dir)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
