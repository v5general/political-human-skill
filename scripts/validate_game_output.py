"""Fail-closed validator for live Absolute Majority action output."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "game_adapter" / "absolute_majority_schema.json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_game_output(input_payload: Any, output_payload: Any) -> list[str]:
    """Validate generated output pairing only; success does not authorize execution."""
    if not isinstance(input_payload, dict):
        return ["input must be a JSON object"]
    if not isinstance(output_payload, dict):
        return ["output must be a JSON object"]

    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    errors = [
        f"{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in sorted(Draft202012Validator(schema).iter_errors(output_payload), key=lambda item: list(item.path))
    ]

    for field in ("persona_id", "event_id"):
        if output_payload.get(field) != input_payload.get(field):
            errors.append(f"output {field} must exactly match input {field}")

    input_actions = input_payload.get("candidate_actions")
    output_actions = output_payload.get("candidate_actions")
    if output_actions != input_actions:
        errors.append("output candidate_actions must exactly match input candidate_actions in order")
    if isinstance(input_actions, list):
        scores = output_payload.get("action_scores")
        if not isinstance(scores, dict) or set(scores) != set(input_actions):
            errors.append("action_scores keys must exactly cover input candidate_actions")
        if output_payload.get("selected_action") not in input_actions:
            errors.append("selected_action must be one of input candidate_actions")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Input event JSON")
    parser.add_argument("--output", type=Path, help="Generated action JSON")
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

    errors = validate_game_output(input_payload, output_payload)
    result = {"valid": not errors, "scope": "output_only", "execution_authorized": False, "errors": errors}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
