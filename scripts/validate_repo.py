"""Validate that the Political Human Skill repository is machine-parseable."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

LOCAL_PACKAGE_DIR = Path(__file__).resolve().parents[1] / ".python-packages"
if LOCAL_PACKAGE_DIR.exists():
    sys.path.insert(0, str(LOCAL_PACKAGE_DIR))

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - depends on local environment
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".python-packages"}

REQUIRED_FILES = [
    "README.md",
    "SPEC.md",
    "SKILL.md",
    "test-prompts.json",
    "templates/persona_template.yaml",
    "templates/historical_archetype_conversion.yaml",
    "templates/relationship_template.json",
    "templates/memory_template.json",
    "game_adapter/absolute_majority_schema.json",
    "game_adapter/absolute_majority_input_schema.json",
    "game_adapter/sample_input.json",
    "game_adapter/expected_output.json",
    "demo/README.md",
    "demo/run_dialogue_demo.md",
    "demo/run_absolute_majority_demo.md",
    "demo/sample_dialogue_input.md",
    "demo/sample_absolute_majority_input.json",
    "demo/expected_absolute_majority_output.json",
]

EXAMPLE_REQUIRED_FILES = [
    "persona.yaml",
    "runtime_card.md",
    "memory.json",
    "relationship.json",
]

ODA_DIALOGUE_SAMPLE_FILES = [
    "casual_private.md",
    "public_interview.md",
    "strategy_room.md",
    "confrontation.md",
    "trust_low.md",
    "trust_high.md",
    "game_action.json",
]

ABSOLUTE_MAJORITY_INPUT_REQUIRED = [
    "persona_id",
    "event_id",
    "event_type",
    "policy_issue",
    "public_support_rate",
    "party_order",
    "faction_order",
    "district_pressure",
    "media_pressure",
    "player_instruction",
    "candidate_actions",
    "current_relationship",
    "recent_memory",
    "parliament_context",
    "party_context",
]

RELATIONSHIP_REQUIRED = ["trust", "respect", "affection", "caution", "dependency"]
PARLIAMENT_REQUIRED = ["ruling_seats", "opposition_seats", "committee_stage", "vote_margin_estimate"]
PARTY_REQUIRED = ["party_name", "faction_name", "leadership_stability"]


class Reporter:
    def __init__(self) -> None:
        self.failures: list[str] = []

    def pass_(self, message: str) -> None:
        print(f"PASS {message}")

    def fail(self, message: str) -> None:
        print(f"FAIL {message}")
        self.failures.append(message)


def iter_files(*suffixes: str) -> list[Path]:
    found: list[Path] = []
    suffix_set = set(suffixes)
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in suffix_set:
            found.append(path)
    return sorted(found)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_yaml(path: Path) -> Any:
    if yaml is None:
        raise RuntimeError("PyYAML is not installed. Run: pip install -r requirements.txt")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_json_files(reporter: Reporter) -> None:
    for path in iter_files(".json"):
        try:
            parse_json(path)
            reporter.pass_(f"JSON parses: {rel(path)}")
        except Exception as exc:  # noqa: BLE001 - validation should report any parse error
            reporter.fail(f"JSON parse failed: {rel(path)} ({exc})")


def validate_yaml_files(reporter: Reporter) -> None:
    if yaml is None:
        reporter.fail("PyYAML is missing; install dependencies with: pip install -r requirements.txt")
        return
    for path in iter_files(".yaml", ".yml"):
        try:
            parse_yaml(path)
            reporter.pass_(f"YAML parses: {rel(path)}")
        except Exception as exc:  # noqa: BLE001
            reporter.fail(f"YAML parse failed: {rel(path)} ({exc})")


def validate_skill_frontmatter(reporter: Reporter) -> None:
    path = ROOT / "SKILL.md"
    if not path.exists():
        reporter.fail("SKILL.md is missing")
        return

    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        reporter.fail("SKILL.md frontmatter must start with a standalone --- line")
        return

    try:
        _, frontmatter, _ = text.split("---\n", 2)
    except ValueError:
        reporter.fail("SKILL.md frontmatter closing --- line is missing")
        return

    try:
        data = yaml.safe_load(frontmatter) if yaml is not None else None
    except Exception as exc:  # noqa: BLE001
        reporter.fail(f"SKILL.md frontmatter is not valid YAML ({exc})")
        return

    if yaml is None:
        reporter.fail("Cannot parse SKILL.md frontmatter because PyYAML is missing")
        return

    required_keys = ["name", "description", "argument-hint", "version", "user-invocable", "allowed-tools"]
    missing = [key for key in required_keys if key not in data]
    if missing:
        reporter.fail(f"SKILL.md frontmatter missing keys: {', '.join(missing)}")
        return
    if not isinstance(data.get("allowed-tools"), list):
        reporter.fail("SKILL.md frontmatter allowed-tools must be a YAML list")
        return
    reporter.pass_("SKILL.md frontmatter exists and parses")


def validate_required_files(reporter: Reporter) -> None:
    for name in REQUIRED_FILES:
        path = ROOT / name
        if path.exists():
            reporter.pass_(f"Required file exists: {name}")
        else:
            reporter.fail(f"Required file missing: {name}")


def validate_example_personas(reporter: Reporter) -> None:
    examples_root = ROOT / "personas" / "examples"
    if not examples_root.exists():
        reporter.fail("personas/examples directory is missing")
        return

    example_dirs = sorted(path for path in examples_root.iterdir() if path.is_dir())
    if not example_dirs:
        reporter.fail("personas/examples contains no example persona directories")
        return

    for example_dir in example_dirs:
        for required in EXAMPLE_REQUIRED_FILES:
            path = example_dir / required
            if path.exists():
                reporter.pass_(f"Example file exists: {rel(path)}")
            else:
                reporter.fail(f"Example file missing: {rel(path)}")

        explanation_files = [example_dir / "examples.md", example_dir / "README.md"]
        if any(path.exists() for path in explanation_files):
            reporter.pass_(f"Example explanation exists: {rel(example_dir)}")
        else:
            reporter.fail(f"Example explanation missing: {rel(example_dir)}")

        dialogue_dir = example_dir / "dialogue_samples"
        if dialogue_dir.exists() and dialogue_dir.is_dir():
            reporter.pass_(f"Dialogue samples directory exists: {rel(dialogue_dir)}")
        else:
            reporter.fail(f"Dialogue samples directory missing: {rel(dialogue_dir)}")


def validate_oda_dialogue_samples(reporter: Reporter) -> None:
    dialogue_dir = ROOT / "personas" / "examples" / "oda_nobunaga_modernized" / "dialogue_samples"
    for name in ODA_DIALOGUE_SAMPLE_FILES:
        path = dialogue_dir / name
        if path.exists():
            reporter.pass_(f"Oda dialogue sample exists: {rel(path)}")
        else:
            reporter.fail(f"Oda dialogue sample missing: {rel(path)}")


def validate_runtime_cards_testing_behavior(reporter: Reporter) -> None:
    """Machine-check that every runtime_card.md in the repo carries a Testing Behavior section.

    This turns the 'Testing Behavior is a required field' rule from a natural-language
    self-check into a schema-level assertion: validate_repo.py FAILs if any shipped
    runtime_card is missing it. Generated personas dropped into personas/examples/
    (or anywhere under the repo) are held to the same bar.
    """
    found = False
    for path in sorted(ROOT.rglob("runtime_card.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        found = True
        text = path.read_text(encoding="utf-8")
        if "## Testing Behavior" in text:
            reporter.pass_(f"Testing Behavior section present: {rel(path)}")
        else:
            reporter.fail(f"runtime_card.md missing '## Testing Behavior' section: {rel(path)}")
    if not found:
        reporter.fail("No runtime_card.md found anywhere in the repo to validate Testing Behavior")


def validate_generated_historical_personas(reporter: Reporter) -> None:
    """If personas/generated/ exists, check each mode B/C persona carries source-grounding
    and creation-review artifacts. Does NOT touch personas/examples/ (those are built-in
    structural demos, not full generated outputs — see SPEC §18)."""
    gen_root = ROOT / "personas" / "generated"
    if not gen_root.exists():
        return  # no generated personas yet; nothing to check
    checked = False
    for d in sorted(p for p in gen_root.iterdir() if p.is_dir()):
        is_historical = False
        meta = d / "meta.json"
        if meta.exists():
            try:
                m = json.loads(meta.read_text(encoding="utf-8"))
                src = m.get("source_type") or ""
                mode = m.get("mode") or ""
                is_historical = src.startswith("historical") or mode in ("B", "C")
            except Exception:  # noqa: BLE001
                pass
        if not is_historical:
            continue
        checked = True
        for art in ("historical_source_report.md", "creation_review.md"):
            p = d / art
            if p.exists():
                reporter.pass_(f"historical artifact present: {rel(p)}")
            else:
                reporter.fail(f"historical persona missing {art}: {rel(p)}")
    if not checked:
        reporter.pass_("personas/generated/ has no historical persona to check yet")


def validate_input_payload(name: str, payload: Any, reporter: Reporter) -> None:
    if not isinstance(payload, dict):
        reporter.fail(f"{name} must be a JSON object")
        return

    missing = [field for field in ABSOLUTE_MAJORITY_INPUT_REQUIRED if field not in payload]
    if missing:
        reporter.fail(f"{name} missing required input fields: {', '.join(missing)}")
        return

    support = payload.get("public_support_rate")
    if not isinstance(support, (int, float)) or not 0 <= support <= 100:
        reporter.fail(f"{name} public_support_rate must be a number from 0 to 100")
        return

    actions = payload.get("candidate_actions")
    if not isinstance(actions, list) or not actions or not all(isinstance(item, str) and item for item in actions):
        reporter.fail(f"{name} candidate_actions must be a non-empty array of strings")
        return

    relationship = payload.get("current_relationship")
    if not isinstance(relationship, dict):
        reporter.fail(f"{name} current_relationship must be an object")
        return
    missing_relationship = [field for field in RELATIONSHIP_REQUIRED if field not in relationship]
    if missing_relationship:
        reporter.fail(f"{name} current_relationship missing: {', '.join(missing_relationship)}")
        return

    recent_memory = payload.get("recent_memory")
    if not isinstance(recent_memory, list) or not all(isinstance(item, str) for item in recent_memory):
        reporter.fail(f"{name} recent_memory must be an array of strings")
        return

    parliament = payload.get("parliament_context")
    if not isinstance(parliament, dict) or any(field not in parliament for field in PARLIAMENT_REQUIRED):
        reporter.fail(f"{name} parliament_context missing required fields")
        return

    party = payload.get("party_context")
    if not isinstance(party, dict) or any(field not in party for field in PARTY_REQUIRED):
        reporter.fail(f"{name} party_context missing required fields")
        return

    reporter.pass_(f"Absolute Majority input payload shape is valid: {name}")


def validate_output_payload(name: str, payload: Any, candidate_actions: list[str], reporter: Reporter) -> None:
    if not isinstance(payload, dict):
        reporter.fail(f"{name} must be a JSON object")
        return

    selected = payload.get("selected_action")
    if selected not in candidate_actions:
        reporter.fail(f"{name} selected_action must be one of candidate_actions")
        return

    memory_write = payload.get("memory_write")
    if not isinstance(memory_write, list) or not all(isinstance(item, str) for item in memory_write):
        reporter.fail(f"{name} memory_write must be an array of strings")
        return

    if "action_scores" in payload:
        scores = payload["action_scores"]
        if not isinstance(scores, dict):
            reporter.fail(f"{name} action_scores must be an object when present")
            return
        invalid_scores = [
            action
            for action, score in scores.items()
            if action not in candidate_actions or not isinstance(score, int) or not 0 <= score <= 100
        ]
        if invalid_scores:
            reporter.fail(f"{name} action_scores contain invalid actions or scores: {', '.join(invalid_scores)}")
            return

    reporter.pass_(f"Absolute Majority output payload shape is valid: {name}")


def validate_prompt_files(reporter: Reporter) -> None:
    candidates = [ROOT / "test-prompts.json", ROOT / "quality" / "test-prompts.json"]
    existing = [path for path in candidates if path.exists()]
    if not existing:
        reporter.fail("No test-prompts.json found at root or quality/")
        return

    for path in existing:
        try:
            parse_json(path)
            reporter.pass_(f"Test prompts parse: {rel(path)}")
        except Exception as exc:  # noqa: BLE001
            reporter.fail(f"Test prompts invalid: {rel(path)} ({exc})")


def validate_absolute_majority_files(reporter: Reporter) -> None:
    for name in [
        "game_adapter/absolute_majority_schema.json",
        "game_adapter/absolute_majority_input_schema.json",
        "game_adapter/sample_input.json",
        "game_adapter/expected_output.json",
    ]:
        path = ROOT / name
        if not path.exists():
            reporter.fail(f"Absolute Majority file missing: {name}")
            continue
        try:
            parse_json(path)
            reporter.pass_(f"Absolute Majority JSON parses: {name}")
        except Exception as exc:  # noqa: BLE001
            reporter.fail(f"Absolute Majority JSON invalid: {name} ({exc})")

    sample_input = ROOT / "game_adapter" / "sample_input.json"
    expected_output = ROOT / "game_adapter" / "expected_output.json"
    demo_input = ROOT / "demo" / "sample_absolute_majority_input.json"
    demo_output = ROOT / "demo" / "expected_absolute_majority_output.json"
    dialogue_action = (
        ROOT
        / "personas"
        / "examples"
        / "oda_nobunaga_modernized"
        / "dialogue_samples"
        / "game_action.json"
    )

    for name, path in [
        ("game_adapter/sample_input.json", sample_input),
        ("demo/sample_absolute_majority_input.json", demo_input),
    ]:
        if path.exists():
            validate_input_payload(name, parse_json(path), reporter)

    if sample_input.exists() and expected_output.exists():
        input_payload = parse_json(sample_input)
        output_payload = parse_json(expected_output)
        if isinstance(input_payload, dict) and isinstance(input_payload.get("candidate_actions"), list):
            validate_output_payload(
                "game_adapter/expected_output.json",
                output_payload,
                input_payload["candidate_actions"],
                reporter,
            )

    if demo_input.exists() and demo_output.exists():
        input_payload = parse_json(demo_input)
        output_payload = parse_json(demo_output)
        if isinstance(input_payload, dict) and isinstance(input_payload.get("candidate_actions"), list):
            validate_output_payload(
                "demo/expected_absolute_majority_output.json",
                output_payload,
                input_payload["candidate_actions"],
                reporter,
            )

    if dialogue_action.exists():
        payload = parse_json(dialogue_action)
        if not isinstance(payload, dict):
            reporter.fail("personas/examples/oda_nobunaga_modernized/dialogue_samples/game_action.json must be an object")
        else:
            input_payload = payload.get("input")
            output_payload = payload.get("expected_output")
            validate_input_payload("Oda dialogue game_action.input", input_payload, reporter)
            if isinstance(input_payload, dict) and isinstance(input_payload.get("candidate_actions"), list):
                validate_output_payload(
                    "Oda dialogue game_action.expected_output",
                    output_payload,
                    input_payload["candidate_actions"],
                    reporter,
                )


def main() -> int:
    reporter = Reporter()

    validate_required_files(reporter)
    validate_json_files(reporter)
    validate_yaml_files(reporter)
    validate_skill_frontmatter(reporter)
    validate_example_personas(reporter)
    validate_oda_dialogue_samples(reporter)
    validate_runtime_cards_testing_behavior(reporter)
    validate_generated_historical_personas(reporter)
    validate_prompt_files(reporter)
    validate_absolute_majority_files(reporter)

    if reporter.failures:
        print(f"\nFAIL repository validation failed with {len(reporter.failures)} issue(s).")
        return 1

    print("\nPASS repository validation completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
