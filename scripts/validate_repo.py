"""Validate that the Political Human Skill repository is machine-parseable."""

from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

LOCAL_PACKAGE_DIR = Path(__file__).resolve().parents[1] / ".python-packages"
if LOCAL_PACKAGE_DIR.exists():
    sys.path.insert(0, str(LOCAL_PACKAGE_DIR))

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - depends on local environment
    yaml = None

try:
    from validate_game_output import validate_game_output
except ModuleNotFoundError:  # pragma: no cover - import path depends on invocation style
    validate_game_output = None

try:
    from persona_runtime_contracts import (
        PersonaContractError,
        SOURCE_REPORT_BY_TYPE,
        activation_readiness_errors,
        bind_identity_errors,
        compute_review_artifact_hash,
        mutable_state_errors,
        persona_directory_errors,
        resolve_persona_dir,
    )
except ModuleNotFoundError:  # pragma: no cover - import path depends on invocation style
    PersonaContractError = None
    SOURCE_REPORT_BY_TYPE = {}
    activation_readiness_errors = None
    bind_identity_errors = None
    compute_review_artifact_hash = None
    mutable_state_errors = None
    persona_directory_errors = None
    resolve_persona_dir = None

try:
    from validate_game_transaction import validate_game_transaction
except ModuleNotFoundError:  # pragma: no cover - import path depends on invocation style
    validate_game_transaction = None


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
    "core/activation_gate.md",
    "core/persona_path_resolver.md",
    "quality/TESTING.md",
    "scripts/run_semantic_tests.py",
    "scripts/validate_game_output.py",
    "scripts/validate_game_transaction.py",
    "scripts/validate_persona.py",
    "scripts/persona_runtime_contracts.py",
    "scripts/review_state.py",
    "templates/composite_archetype_source_report_template.md",
    "templates/memory_schema.json",
    "templates/relationship_schema.json",
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
    "committee_debate.md",
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

RELATIONSHIP_REQUIRED = ["familiarity", "trust", "respect", "affection", "caution", "dependency"]
PARLIAMENT_REQUIRED = ["ruling_seats", "opposition_seats", "committee_stage", "vote_margin_estimate"]
PARTY_REQUIRED = ["party_name", "faction_name", "leadership_stability"]
REQUIRED_SELF_STATES = [
    "public_self",
    "private_self",
    "strategic_self",
    "wounded_self",
    "fatigued_self",
    "intimate_self",
]
GENERATED_DIALOGUE_REQUIRED = [
    "README.md",
    "casual_private.md",
    "public_interview.md",
    "strategy_room.md",
    "confrontation.md",
    "trust_low.md",
    "trust_high.md",
    "committee_debate.md",
]
REQUIRED_REGRESSION_IDS = {
    "scene-on-record-vs-incidental-overhear",
    "tier1-private-state-relationship-gate",
    "persona-direct-activation-unconfirmed",
    "address-canonical-resolver-order",
    "game-action-blocked-when-unconfirmed",
}


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
    if yaml is None:
        reporter.fail("Cannot parse SKILL.md frontmatter because PyYAML is missing")
        return

    required_keys = ["name", "description", "argument-hint", "version", "user-invocable", "allowed-tools"]
    skill_paths = [path for path in ROOT.rglob("SKILL.md") if not any(part in SKIP_DIRS for part in path.parts)]
    if not skill_paths:
        reporter.fail("No SKILL.md files found")
        return

    for path in sorted(skill_paths):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            reporter.fail(f"SKILL frontmatter must start with a standalone --- line: {rel(path)}")
            continue
        try:
            _, frontmatter, _ = text.split("---\n", 2)
            data = yaml.safe_load(frontmatter)
        except Exception as exc:  # noqa: BLE001
            reporter.fail(f"SKILL frontmatter is not valid YAML: {rel(path)} ({exc})")
            continue
        if not isinstance(data, dict):
            reporter.fail(f"SKILL frontmatter must be a mapping: {rel(path)}")
            continue
        missing = [key for key in required_keys if key not in data]
        if missing:
            reporter.fail(f"SKILL frontmatter missing keys {missing}: {rel(path)}")
            continue
        if not isinstance(data.get("allowed-tools"), list):
            reporter.fail(f"SKILL frontmatter allowed-tools must be a YAML list: {rel(path)}")
            continue
        reporter.pass_(f"SKILL frontmatter exists and parses: {rel(path)}")


def number_to_chinese(value: int) -> str:
    """Return the common Chinese rendering for ages from 0 through 99."""
    digits = "零一二三四五六七八九"
    if value < 10:
        return digits[value]
    tens, ones = divmod(value, 10)
    prefix = "十" if tens == 1 else f"{digits[tens]}十"
    return prefix if ones == 0 else f"{prefix}{digits[ones]}"


def validate_example_runtime_contracts(reporter: Reporter) -> None:
    """Validate cross-file runtime invariants for every shipped example persona."""
    examples_root = ROOT / "personas" / "examples"
    if yaml is None or not examples_root.exists():
        return

    for directory in sorted(path for path in examples_root.iterdir() if path.is_dir()):
        if persona_directory_errors is None:
            reporter.fail("shared persona directory validator could not be imported")
        else:
            shared_errors = persona_directory_errors(directory, directory.name)
            if shared_errors:
                reporter.fail(f"shared persona contract failed {shared_errors}: {rel(directory)}")
            else:
                reporter.pass_(f"shared persona contract passes: {rel(directory)}")
        persona_path = directory / "persona.yaml"
        runtime_path = directory / "runtime_card.md"
        skill_path = directory / "SKILL.md"
        meta_path = directory / "meta.json"
        if not all(path.exists() for path in (persona_path, runtime_path, skill_path, meta_path)):
            continue

        symlinks = [path for path in directory.rglob("*") if path.is_symlink()]
        if symlinks:
            reporter.fail(f"persona artifact contains forbidden symlinks {[rel(path) for path in symlinks]}: {rel(directory)}")
        else:
            reporter.pass_(f"persona artifact tree contains no symlinks: {rel(directory)}")

        try:
            persona = parse_yaml(persona_path)
            meta = parse_json(meta_path)
        except Exception as exc:  # noqa: BLE001
            reporter.fail(f"Cannot validate example runtime contract: {rel(directory)} ({exc})")
            continue
        if not isinstance(persona, dict) or not isinstance(meta, dict):
            reporter.fail(f"Example persona/meta must be mappings: {rel(directory)}")
            continue

        if bind_identity_errors is None or mutable_state_errors is None or activation_readiness_errors is None:
            reporter.fail("persona runtime contract helpers could not be imported")
            continue
        identity_errors = bind_identity_errors(directory, directory.name, persona, meta)
        if identity_errors:
            reporter.fail(f"persona identity binding failed {identity_errors}: {rel(directory)}")
        else:
            reporter.pass_(f"persona directory, slug, and IDs are bound: {rel(directory)}")
        try:
            state_errors, _, _ = mutable_state_errors(directory, directory.name)
        except Exception as exc:  # noqa: BLE001
            reporter.fail(f"mutable state validation crashed: {rel(directory)} ({exc})")
        else:
            if state_errors:
                reporter.fail(f"mutable state contract failed {state_errors}: {rel(directory)}")
            else:
                reporter.pass_(f"memory and relationship state are schema-valid and isolated: {rel(directory)}")

        states = persona.get("self_states")
        missing_states = [state for state in REQUIRED_SELF_STATES if not isinstance(states, dict) or state not in states]
        if missing_states:
            reporter.fail(f"persona.yaml missing self states {missing_states}: {rel(persona_path)}")
        else:
            reporter.pass_(f"persona.yaml has all six stored self-state profiles: {rel(persona_path)}")

        life_texture = persona.get("life_texture")
        fatigue_signals = life_texture.get("fatigue_signals") if isinstance(life_texture, dict) else None
        mundane_anchors = life_texture.get("mundane_anchors") if isinstance(life_texture, dict) else None
        vulnerability_style = life_texture.get("vulnerability_style") if isinstance(life_texture, dict) else None
        fatigue_contract_ok = (
            isinstance(fatigue_signals, list)
            and bool(fatigue_signals)
            and all(isinstance(item, str) and item.strip() for item in fatigue_signals)
            and isinstance(mundane_anchors, list)
            and bool(mundane_anchors)
            and all(isinstance(item, str) and item.strip() for item in mundane_anchors)
            and isinstance(vulnerability_style, str)
            and bool(vulnerability_style.strip())
        )
        if fatigue_contract_ok:
            reporter.pass_(f"persona.yaml fatigue and human-texture fields are non-empty: {rel(persona_path)}")
        else:
            reporter.fail(f"persona.yaml fatigue_signals/mundane_anchors/vulnerability_style incomplete: {rel(persona_path)}")

        runtime_text = runtime_path.read_text(encoding="utf-8")
        missing_runtime_states = [state for state in REQUIRED_SELF_STATES if f"`{state}`" not in runtime_text]
        if missing_runtime_states:
            reporter.fail(f"runtime_card.md missing self-state shortcuts {missing_runtime_states}: {rel(runtime_path)}")
        else:
            reporter.pass_(f"runtime_card.md has all six stored self-state shortcuts: {rel(runtime_path)}")

        required_runtime_sections = [
            "## Fatigue & Vulnerability Hints",
            "## Human Moment Hints",
            "## Mundane Anchors",
        ]
        missing_sections = [heading for heading in required_runtime_sections if heading not in runtime_text]
        empty_sections: list[str] = []
        for heading in required_runtime_sections:
            if heading not in runtime_text:
                continue
            body = runtime_text.split(heading, 1)[1].split("\n## ", 1)[0]
            if body.count("- ") < 2 or len(body.strip()) < 20:
                empty_sections.append(heading)
        if missing_sections or empty_sections:
            reporter.fail(
                f"runtime_card.md fatigue/human sections missing={missing_sections} empty={empty_sections}: {rel(runtime_path)}"
            )
        else:
            reporter.pass_(f"runtime_card.md fatigue and human-moment sections are non-empty: {rel(runtime_path)}")

        skill_text = skill_path.read_text(encoding="utf-8")
        gate_markers = ["core/activation_gate.md", "meta.json.latest_review_status", "creation_review.md", "review_state.py"]
        missing_gate_markers = [marker for marker in gate_markers if marker not in skill_text]
        if missing_gate_markers:
            reporter.fail(f"persona SKILL missing activation gate markers {missing_gate_markers}: {rel(skill_path)}")
        else:
            reporter.pass_(f"persona SKILL enforces activation preflight: {rel(skill_path)}")

        if "private_self" in skill_text and "recurring_contact" in skill_text and "不查关系门控" not in skill_text:
            reporter.pass_(f"persona SKILL carries Tier 1 relationship gate: {rel(skill_path)}")
        else:
            reporter.fail(f"persona SKILL must gate Tier 1 private_self at recurring_contact: {rel(skill_path)}")

        identity = persona.get("identity")
        age = identity.get("age") if isinstance(identity, dict) else None
        if isinstance(age, int):
            markers = [f"{age}岁", f"{age} 岁", f"{number_to_chinese(age)}岁"]
            if any(marker in skill_text for marker in markers):
                reporter.pass_(f"persona age agrees with SKILL identity card ({age}): {rel(directory)}")
            else:
                reporter.fail(f"persona age {age} not reflected in SKILL identity card: {rel(directory)}")

            readme_markers = [f"Age {age}", f"{age}岁", f"{age}歳", f"{age}세"]
            for readme_name in ("README.md", "README_cn.md", "README_ja.md", "README_ko.md"):
                readme_path = ROOT / readme_name
                readme_text = readme_path.read_text(encoding="utf-8")
                if any(marker in readme_text for marker in readme_markers):
                    reporter.pass_(f"persona age {age} appears in {readme_name}: {rel(directory)}")
                else:
                    reporter.fail(f"persona age {age} missing from {readme_name}: {rel(directory)}")
        else:
            reporter.fail(f"persona.yaml identity.age must be an integer: {rel(persona_path)}")

        persona_meta = persona.get("meta")
        persona_language = persona_meta.get("native_language") if isinstance(persona_meta, dict) else None
        if persona_language and persona_language == meta.get("native_language"):
            reporter.pass_(f"native_language agrees across persona.yaml and meta.json: {rel(directory)}")
        else:
            reporter.fail(f"native_language mismatch across persona.yaml and meta.json: {rel(directory)}")

        readiness_errors = activation_readiness_errors(directory, persona, meta)
        if readiness_errors:
            reporter.fail(f"activation/readiness contract failed {readiness_errors}: {rel(meta_path)}")
        else:
            reporter.pass_(f"activation, safety, and review readiness are coherent: {rel(meta_path)}")

        generated_files = meta.get("generated_files")
        if isinstance(generated_files, list) and all(isinstance(name, str) for name in generated_files):
            missing_generated = [name for name in generated_files if not (directory / name).exists()]
            required_manifest = {"SKILL.md", "dialogue_samples/committee_debate.md"}
            omitted_required = sorted(required_manifest - set(generated_files))
            if missing_generated or omitted_required:
                reporter.fail(
                    f"generated_files mismatch missing={missing_generated} omitted={omitted_required}: {rel(meta_path)}"
                )
            else:
                reporter.pass_(f"generated_files manifest resolves and includes required artifacts: {rel(meta_path)}")
        else:
            reporter.fail(f"meta.json generated_files must be a list of paths: {rel(meta_path)}")

        creation_review_path = directory / "creation_review.md"
        if creation_review_path.exists():
            review_text = creation_review_path.read_text(encoding="utf-8")
            expected_modified = str(bool(meta.get("user_modified_after_generation"))).lower()
            marker = f"user_modified_after_generation = {expected_modified}"
            if marker in review_text:
                reporter.pass_(f"creation review provenance agrees with meta.json: {rel(creation_review_path)}")
            else:
                reporter.fail(f"creation review provenance does not contain '{marker}': {rel(creation_review_path)}")


def validate_scene_cache_contract(reporter: Reporter) -> None:
    """Ensure public recording and incidental overhearing remain separate fields."""
    scene_path = ROOT / "core" / "scene_location_system.md"
    protocol_path = ROOT / "core" / "runtime_protocol.md"
    schema_path = ROOT / "core" / "runtime_cache_schema.yaml"
    scene_text = scene_path.read_text(encoding="utf-8")
    protocol_text = protocol_path.read_text(encoding="utf-8")
    schema = parse_yaml(schema_path) if yaml is not None else None
    scene_vector = (
        schema.get("conversation_state", {}).get("scene_vector", {})
        if isinstance(schema, dict)
        else {}
    )
    conditions = [
        "recording_status" in scene_text,
        "recording_status=off_record" in scene_text or "recording_status: off_record" in scene_text,
        "recording_status" in protocol_text,
        isinstance(scene_vector, dict) and "recording_status" in scene_vector,
    ]
    if all(conditions):
        reporter.pass_("recording_status is separated from overhear_risk across scene, protocol, and cache schema")
    else:
        reporter.fail("recording_status/overhear_risk contract is incomplete across scene, protocol, or cache schema")


def validate_activation_entry_points(reporter: Reporter) -> None:
    """Ensure generic invocation and demos cannot bypass the canonical activation gate."""
    paths = [
        ROOT / "families" / "political_human" / "invocation.md",
        ROOT / "core" / "runtime_protocol.md",
        ROOT / "demo" / "README.md",
        ROOT / "demo" / "run_dialogue_demo.md",
        ROOT / "demo" / "run_absolute_majority_demo.md",
        ROOT / "game_adapter" / "event_response.md",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        gate_ok = "core/activation_gate.md" in text and ("unconfirmed" in text or "confirmed" in text)
        executor_ok = "review_state.py" in text
        if gate_ok and executor_ok:
            reporter.pass_(f"entry point invokes activation gate via executor: {rel(path)}")
        elif gate_ok:
            reporter.fail(f"entry point bypasses review_state.py executor: {rel(path)}")
        else:
            reporter.fail(f"entry point can bypass activation gate: {rel(path)}")


def validate_review_state_executor(reporter: Reporter) -> None:
    """Integration test: the executor drives the full lifecycle fail-closed."""
    import subprocess

    source_dir = ROOT / "personas" / "examples" / "caesar_modernized"
    with tempfile.TemporaryDirectory() as temp_root:
        persona_dir = Path(temp_root) / "caesar_modernized"
        shutil.copytree(source_dir, persona_dir)

        def run(*args: str) -> tuple[int, dict]:
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "review_state.py"), *args, "--persona-dir", str(persona_dir)],
                capture_output=True,
                text=True,
            )
            try:
                return proc.returncode, json.loads(proc.stdout)
            except json.JSONDecodeError:
                return proc.returncode, {"raw": proc.stdout, "stderr": proc.stderr[-400:]}

        cases = [
            (("commit", "caesar_modernized"), lambda o: o.get("committed") is True),
            (("check", "caesar_modernized"), lambda o: o.get("decision") == "confirm_prompt"),
            (("confirm", "caesar_modernized"), lambda o: o.get("confirmed") is True),
            (("check", "caesar_modernized"), lambda o: o.get("decision") == "activate"),
        ]
        failed = False
        for command, expectation in cases:
            code, out = run(*command)
            if code not in (0, 1) or not expectation(out):
                reporter.fail(f"review_state executor lifecycle failed at {command}: {out}")
                failed = True
                break
        if not failed:
            # Mutable-state writes never invalidate; immutable edits do; confirm then refuses.
            (persona_dir / "memory.json").write_text(
                (persona_dir / "memory.json").read_text(encoding="utf-8") + "\n", encoding="utf-8", newline=""
            )
            _, out = run("check", "caesar_modernized")
            if out.get("decision") == "activate":
                card = persona_dir / "runtime_card.md"
                card.write_text(card.read_text(encoding="utf-8") + "\n# executor probe\n", encoding="utf-8", newline="")
                _, out = run("check", "caesar_modernized")
                _, refused = run("confirm", "caesar_modernized")
                if (
                    out.get("decision") == "blocked"
                    and any("stale" in r for r in out.get("reasons", []))
                    and refused.get("confirmed") is not True
                ):
                    reporter.pass_("review_state executor lifecycle, mutable neutrality, and stale invalidation all hold")
                else:
                    reporter.fail(f"review_state executor stale invalidation broken: {out} / {refused}")
            else:
                reporter.fail(f"review_state executor mutable-state neutrality broken: {out}")


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
        # runtime_card must declare it does not replace persona.yaml (SPEC §18, No Hardcoded)
        if "persona.yaml" in text and (
            "does not replace" in text or "must not replace" in text
            or "不替代" in text or "不是替代" in text or "不取代" in text
        ):
            reporter.pass_(f"runtime_card declares non-replacement of persona.yaml: {rel(path)}")
        else:
            reporter.fail(f"runtime_card.md must declare it does not replace persona.yaml: {rel(path)}")
    if not found:
        reporter.fail("No runtime_card.md found anywhere in the repo to validate Testing Behavior")


def validate_generated_personas(reporter: Reporter) -> None:
    """Validate every source type under the canonical user-generated root."""
    gen_root = ROOT / "user_generated" / "personas"
    if not gen_root.exists():
        reporter.pass_("canonical user_generated/personas root has no generated personas yet")
        return
    for directory in sorted(path for path in gen_root.iterdir() if path.is_dir()):
        if persona_directory_errors is None:
            reporter.fail("shared persona directory validator could not be imported")
        else:
            shared_errors = persona_directory_errors(directory, directory.name)
            if shared_errors:
                reporter.fail(f"shared generated persona contract failed {shared_errors}: {rel(directory)}")
            else:
                reporter.pass_(f"shared generated persona contract passes: {rel(directory)}")
        symlinks = [path for path in directory.rglob("*") if path.is_symlink()]
        if symlinks:
            reporter.fail(f"generated persona contains forbidden symlinks {[rel(path) for path in symlinks]}: {rel(directory)}")
            continue
        meta_path = directory / "meta.json"
        if not meta_path.exists():
            reporter.fail(f"generated persona missing meta.json: {rel(directory)}")
            continue
        try:
            meta = parse_json(meta_path)
        except Exception as exc:  # noqa: BLE001
            reporter.fail(f"generated persona meta.json invalid: {rel(meta_path)} ({exc})")
            continue
        if not isinstance(meta, dict):
            reporter.fail(f"generated persona meta.json must be an object: {rel(meta_path)}")
            continue
        source_type = meta.get("source_type") if isinstance(meta, dict) else None
        expected_report = SOURCE_REPORT_BY_TYPE.get(source_type)
        required = [
            "persona.yaml",
            "runtime_card.md",
            "SKILL.md",
            "relationship.json",
            "memory.json",
            "examples.md",
            "creation_review.md",
        ]
        if expected_report:
            required.append(expected_report)
        else:
            reporter.fail(f"generated persona has unsupported source_type {source_type!r}: {rel(meta_path)}")
        for name in required:
            path = directory / name
            if path.exists():
                reporter.pass_(f"generated persona artifact present: {rel(path)}")
            else:
                reporter.fail(f"generated persona missing {name}: {rel(directory)}")

        dialogue_dir = directory / "dialogue_samples"
        for name in GENERATED_DIALOGUE_REQUIRED:
            path = dialogue_dir / name
            if path.is_file():
                reporter.pass_(f"generated persona dialogue artifact present: {rel(path)}")
            else:
                reporter.fail(f"generated persona missing dialogue_samples/{name}: {rel(directory)}")
        if meta.get("integration_target") == "absolute_majority":
            game_action = dialogue_dir / "game_action.json"
            if game_action.is_file():
                reporter.pass_(f"generated game persona has action fixture: {rel(game_action)}")
            else:
                reporter.fail(f"generated Absolute Majority persona missing dialogue_samples/game_action.json: {rel(directory)}")

        required_meta = [
            "generation_method",
            "source_type",
            "validation_status",
            "activation_requires_user_confirmation",
            "latest_review_status",
            "review_invalidated_by_modification",
            "reviewed_artifact_hash",
        ]
        missing_meta = [field for field in required_meta if field not in meta]
        if missing_meta:
            reporter.fail(f"generated persona meta.json missing {missing_meta}: {rel(meta_path)}")
        if meta.get("activation_requires_user_confirmation") is not True:
            reporter.fail(f"generated persona must require user confirmation: {rel(meta_path)}")
        if source_type in {"historical_inference", "historical_archetype_conversion"} and not meta.get("source_figure"):
            reporter.fail(f"historical generated persona missing source_figure: {rel(meta_path)}")
        if source_type == "modern_real_figure_archetype_extraction":
            if meta.get("de_identified") is not True or meta.get("real_person_roleplay_allowed") is not False:
                reporter.fail(f"modern-real generated persona lacks de-identification safety flags: {rel(meta_path)}")
            if not isinstance(meta.get("removed_fingerprints"), list) or not meta["removed_fingerprints"]:
                reporter.fail(f"modern-real generated persona must list removed_fingerprints: {rel(meta_path)}")

        persona_path = directory / "persona.yaml"
        if persona_path.exists():
            try:
                persona = parse_yaml(persona_path)
            except Exception as exc:  # noqa: BLE001
                reporter.fail(f"generated persona persona.yaml invalid: {rel(persona_path)} ({exc})")
                continue
            if not isinstance(persona, dict):
                reporter.fail(f"generated persona persona.yaml must be a mapping: {rel(persona_path)}")
                continue
            if bind_identity_errors is None or mutable_state_errors is None or activation_readiness_errors is None:
                reporter.fail("persona runtime contract helpers could not be imported")
                continue
            identity_errors = bind_identity_errors(directory, directory.name, persona, meta)
            if identity_errors:
                reporter.fail(f"generated persona identity binding failed {identity_errors}: {rel(directory)}")
            try:
                state_errors, _, _ = mutable_state_errors(directory, directory.name)
            except Exception as exc:  # noqa: BLE001
                reporter.fail(f"generated persona mutable state validation crashed: {rel(directory)} ({exc})")
                state_errors = []
            if state_errors:
                reporter.fail(f"generated persona mutable state contract failed {state_errors}: {rel(directory)}")
            persona_meta = persona.get("meta")
            provenance = persona.get("source_provenance")
            if not isinstance(persona_meta, dict) or persona_meta.get("source_type") != source_type:
                reporter.fail(f"generated persona.yaml meta.source_type must match meta.json: {rel(persona_path)}")
            if not isinstance(provenance, dict) or provenance.get("source_type") != source_type:
                reporter.fail(f"generated persona source_provenance.source_type must match meta.json: {rel(persona_path)}")
            elif provenance.get("modification_review_required") is not True:
                reporter.fail(f"generated persona must require review after modification: {rel(persona_path)}")
            temperament = persona.get("inferred_temperamental_pattern")
            if temperament is None and isinstance(persona.get("human_core"), dict):
                temperament = persona["human_core"].get("inferred_temperamental_pattern")
            if source_type in {"historical_inference", "historical_archetype_conversion"} and not isinstance(temperament, dict):
                reporter.fail(f"historical generated persona missing inferred_temperamental_pattern: {rel(persona_path)}")
            if source_type in {"original_fictional_persona", "historical_inference", "historical_archetype_conversion"}:
                history = persona.get("human_core", {}).get("formative_life_history")
                if not isinstance(history, dict) or any(
                    field not in history
                    for field in (
                        "class_origin",
                        "youth_observations",
                        "intellectual_formation",
                        "stance_formation_logic",
                        "class_relation",
                        "alternative_paths_note",
                    )
                ):
                    reporter.fail(f"generated persona formative_life_history is incomplete: {rel(persona_path)}")
            if source_type == "modern_real_figure_archetype_extraction":
                removed = provenance.get("removed_fingerprints") if isinstance(provenance, dict) else None
                if not isinstance(removed, list) or not removed:
                    reporter.fail(f"modern-real persona provenance must list removed_fingerprints: {rel(persona_path)}")
            readiness_errors = activation_readiness_errors(directory, persona, meta)
            if readiness_errors:
                reporter.fail(f"generated persona activation/readiness failed {readiness_errors}: {rel(directory)}")
            else:
                reporter.pass_(f"generated persona activation, safety, and readiness are coherent: {rel(directory)}")


EXAMPLE_PROVENANCE_META_FIELDS = ["generation_method", "source_type", "modernized", "validation_status"]
ALLOWED_SOURCE_TYPES = tuple(SOURCE_REPORT_BY_TYPE)


def validate_example_generation_provenance(reporter: Reporter) -> None:
    """Enforce Source-Grounded Creation / No-Hardcoded-Persona on personas/examples/:
    each example must declare an allowed source_type, carry creation_review.md, a source
    report matching its source_type, source_provenance in persona.yaml, and provenance meta
    fields. Historical examples also need inferred_temperamental_pattern."""
    examples_root = ROOT / "personas" / "examples"
    if not examples_root.exists():
        return
    for d in sorted(p for p in examples_root.iterdir() if p.is_dir()):
        # creation_review.md required for every example
        cr = d / "creation_review.md"
        if cr.exists():
            reporter.pass_(f"creation_review present: {rel(cr)}")
        else:
            reporter.fail(f"example missing creation_review.md: {rel(d)}")

        # meta.json: source_type validity + provenance fields + source-type-specific flags
        meta = d / "meta.json"
        source_type = ""
        if meta.exists():
            try:
                m = json.loads(meta.read_text(encoding="utf-8"))
                source_type = m.get("source_type") or ""
                if source_type not in ALLOWED_SOURCE_TYPES:
                    reporter.fail(f"meta.json source_type '{source_type}' not allowed {list(ALLOWED_SOURCE_TYPES)}: {rel(meta)}")
                else:
                    reporter.pass_(f"meta.json source_type valid ({source_type}): {rel(meta)}")
                missing = [f for f in EXAMPLE_PROVENANCE_META_FIELDS if f not in m]
                if missing:
                    reporter.fail(f"meta.json missing provenance fields {missing}: {rel(meta)}")
                else:
                    reporter.pass_(f"meta.json provenance complete: {rel(meta)}")
                if m.get("activation_requires_user_confirmation") is not True:
                    reporter.fail(f"meta.json must have activation_requires_user_confirmation=true: {rel(meta)}")
                else:
                    reporter.pass_(f"meta.json activation_requires_user_confirmation=true: {rel(meta)}")
                if source_type in {"historical_inference", "historical_archetype_conversion"} and "source_figure" not in m:
                    reporter.fail(f"historical meta.json missing source_figure: {rel(meta)}")
                if source_type == "modern_real_figure_archetype_extraction":
                    if not m.get("de_identified"):
                        reporter.fail(f"modern_real_figure meta.json must have de_identified=true: {rel(meta)}")
                    if m.get("real_person_roleplay_allowed"):
                        reporter.fail(f"modern_real_figure meta.json must have real_person_roleplay_allowed=false: {rel(meta)}")
                    if "removed_fingerprints" not in m:
                        reporter.fail(f"modern_real_figure meta.json must list removed_fingerprints: {rel(meta)}")
            except Exception as exc:  # noqa: BLE001
                reporter.fail(f"meta.json unparseable: {rel(meta)} ({exc})")

        # source report matching source_type
        expected_report = SOURCE_REPORT_BY_TYPE.get(source_type)
        if expected_report:
            sr = d / expected_report
            if sr.exists():
                reporter.pass_(f"{expected_report} present: {rel(sr)}")
            else:
                reporter.fail(f"{source_type} example missing {expected_report}: {rel(d)}")

        # persona.yaml: source_provenance (all) + inferred_temperamental_pattern (historical)
        # + formative_life_history (mode A/C mandatory per archetype_conversion_protocol.md §2.4)
        py = d / "persona.yaml"
        if py.exists():
            ptext = py.read_text(encoding="utf-8")
            if "source_provenance" in ptext:
                reporter.pass_(f"source_provenance present: {rel(py)}")
            else:
                reporter.fail(f"persona.yaml missing source_provenance: {rel(py)}")
            if "modification_review_required: true" in ptext:
                reporter.pass_(f"source_provenance.modification_review_required=true: {rel(py)}")
            else:
                reporter.fail(f"persona.yaml source_provenance must have modification_review_required: true: {rel(py)}")
            if source_type in {"historical_inference", "historical_archetype_conversion"}:
                if "inferred_temperamental_pattern" in ptext:
                    reporter.pass_(f"inferred_temperamental_pattern present: {rel(py)}")
                else:
                    reporter.fail(f"historical persona.yaml missing inferred_temperamental_pattern: {rel(py)}")
            # formative_life_history is mandatory for mode A (original_fictional_persona)
            # plus both historical branches — see archetype_conversion_protocol.md §2.4
            if source_type in ("original_fictional_persona", "historical_inference", "historical_archetype_conversion"):
                if "formative_life_history:" in ptext:
                    reporter.pass_(f"formative_life_history present: {rel(py)}")
                    # check the 6 required subfields
                    required_subfields = [
                        "class_origin:",
                        "youth_observations:",
                        "intellectual_formation:",
                        "stance_formation_logic:",
                        "class_relation:",
                        "alternative_paths_note:",
                    ]
                    missing_sub = [f for f in required_subfields if f not in ptext]
                    if missing_sub:
                        reporter.fail(f"formative_life_history missing subfields {missing_sub}: {rel(py)}")
                    else:
                        reporter.pass_(f"formative_life_history subfields complete: {rel(py)}")
                else:
                    reporter.fail(f"{source_type} persona.yaml missing formative_life_history block (required per archetype_conversion_protocol.md §2.4): {rel(py)}")


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


def validate_output_payload(name: str, payload: Any, input_payload: Any, reporter: Reporter) -> None:
    if validate_game_output is None:
        reporter.fail("live game-output validator could not be imported")
        return
    try:
        errors = validate_game_output(input_payload, payload)
    except Exception as exc:  # noqa: BLE001
        reporter.fail(f"{name} live game-output validation crashed ({exc})")
        return
    if errors:
        reporter.fail(f"{name} violates live output contract ({'; '.join(errors)})")
        return
    reporter.pass_(f"Absolute Majority output payload and input pairing are valid: {name}")

    rejection_cases: list[tuple[str, dict[str, Any]]] = []
    for field in ("persona_id", "event_id"):
        mutated = json.loads(json.dumps(payload, ensure_ascii=False))
        mutated[field] = f"{mutated.get(field, '')}__mismatch"
        rejection_cases.append((f"mismatched {field}", mutated))

    mutated_actions = json.loads(json.dumps(payload, ensure_ascii=False))
    if isinstance(mutated_actions.get("candidate_actions"), list):
        mutated_actions["candidate_actions"].append("__unexpected_action__")
        rejection_cases.append(("mismatched candidate_actions", mutated_actions))

    mutated_scores = json.loads(json.dumps(payload, ensure_ascii=False))
    if isinstance(mutated_scores.get("action_scores"), dict) and mutated_scores["action_scores"]:
        mutated_scores["action_scores"].pop(next(iter(mutated_scores["action_scores"])))
        rejection_cases.append(("incomplete action_scores", mutated_scores))

    for case_name, invalid_payload in rejection_cases:
        if validate_game_output(input_payload, invalid_payload):
            reporter.pass_(f"Live game-output validator rejects {case_name}: {name}")
        else:
            reporter.fail(f"Live game-output validator accepted {case_name}: {name}")


def validate_prompt_files(reporter: Reporter) -> None:
    candidates = [ROOT / "test-prompts.json", ROOT / "quality" / "test-prompts.json"]
    existing = [path for path in candidates if path.exists()]
    if not existing:
        reporter.fail("No test-prompts.json found at root or quality/")
        return

    for path in existing:
        try:
            prompts = parse_json(path)
        except Exception as exc:  # noqa: BLE001
            reporter.fail(f"Test prompts invalid: {rel(path)} ({exc})")
            continue
        if not isinstance(prompts, list) or not prompts:
            reporter.fail(f"Test prompts must be a non-empty array: {rel(path)}")
            continue

        seen_ids: set[str] = set()
        for index, prompt in enumerate(prompts):
            label = f"{rel(path)}[{index}]"
            if not isinstance(prompt, dict):
                reporter.fail(f"Test prompt must be an object: {label}")
                continue
            prompt_id = prompt.get("id")
            if not isinstance(prompt_id, str) or not prompt_id:
                reporter.fail(f"Test prompt missing non-empty id: {label}")
                continue
            if prompt_id in seen_ids:
                reporter.fail(f"Duplicate test prompt id '{prompt_id}': {label}")
            seen_ids.add(prompt_id)

            has_input = isinstance(prompt.get("prompt"), str) or (
                isinstance(prompt.get("prompt_sequence"), list) and bool(prompt["prompt_sequence"])
            )
            has_expectation = isinstance(prompt.get("expected"), str) or (
                isinstance(prompt.get("expected_behavior"), list) and bool(prompt["expected_behavior"])
            )
            validators = prompt.get("validators")
            if not has_input:
                reporter.fail(f"Test prompt lacks prompt or prompt_sequence: {prompt_id}")
            if not has_expectation:
                reporter.fail(f"Test prompt lacks expected or expected_behavior: {prompt_id}")
            if validators is not None:
                if not isinstance(validators, list) or not validators:
                    reporter.fail(f"Test prompt validators must be a non-empty list when present: {prompt_id}")
                    continue
                missing_paths = [name for name in validators if not isinstance(name, str) or not (ROOT / name).exists()]
                if missing_paths:
                    reporter.fail(f"Test prompt references missing validators {missing_paths}: {prompt_id}")
            elif prompt_id in REQUIRED_REGRESSION_IDS:
                reporter.fail(f"Required structural regression lacks validators: {prompt_id}")

        missing_regressions = sorted(REQUIRED_REGRESSION_IDS - seen_ids)
        if missing_regressions:
            reporter.fail(f"Test suite missing required structural regressions {missing_regressions}: {rel(path)}")
        else:
            reporter.pass_(f"Test prompts parse and satisfy structural contract ({len(prompts)} cases): {rel(path)}")


def validate_spec_localization_sync(reporter: Reporter) -> None:
    english_path = ROOT / "SPEC.md"
    chinese_path = ROOT / "SPEC_cn.md"
    english = english_path.read_text(encoding="utf-8")
    chinese = chinese_path.read_text(encoding="utf-8")

    heading_pattern = re.compile(r"^#{2,4}\s+(\d+(?:\.\d+)*)", re.MULTILINE)
    english_sections = heading_pattern.findall(english)
    chinese_sections = heading_pattern.findall(chinese)
    if english_sections == chinese_sections:
        reporter.pass_("SPEC.md and SPEC_cn.md have matching numbered section structure")
    else:
        reporter.fail(
            f"SPEC localization section drift: English={english_sections!r} Chinese={chinese_sections!r}"
        )

    shared_markers = [
        "original_fictional_persona",
        "historical_inference",
        "historical_archetype_conversion",
        "modern_real_figure_archetype_extraction",
        "composite_archetype",
        "disclaimer_emitted",
        "reviewed_artifact_hash",
        "scripts/persona_runtime_contracts.py",
        "scripts/review_state.py",
        "scripts/validate_game_transaction.py",
        "scripts/validate_game_output.py",
        "templates/memory_schema.json",
        "templates/relationship_schema.json",
        "user_generated/personas/<persona_id>/",
        "fatigued_self",
        "primary_self_state",
        "recording_status",
    ]
    missing = [
        marker
        for marker in shared_markers
        if marker not in english or marker not in chinese
    ]
    if missing:
        reporter.fail(f"SPEC localization missing shared normative markers: {missing}")
    else:
        reporter.pass_("SPEC.md and SPEC_cn.md share all critical runtime and safety markers")

    forbidden_drift = {
        "SPEC.md": ["cross-cultural biological temperament dimensions"],
        "SPEC_cn.md": ["天生的气质"],
    }
    for name, phrases in forbidden_drift.items():
        text = english if name == "SPEC.md" else chinese
        found = [phrase for phrase in phrases if phrase in text]
        if found:
            reporter.fail(f"{name} contains superseded normative wording: {found}")
        else:
            reporter.pass_(f"{name} contains no superseded temperament wording")


def validate_readme_localization_sync(reporter: Reporter) -> None:
    readme_names = ["README.md", "README_cn.md", "README_ja.md", "README_ko.md"]
    documents = {name: (ROOT / name).read_text(encoding="utf-8") for name in readme_names}

    heading_pattern = re.compile(r"^(#{2,3})\s+", re.MULTILINE)
    heading_shapes = {
        name: [len(marker) for marker in heading_pattern.findall(text)]
        for name, text in documents.items()
    }
    baseline_shape = heading_shapes["README.md"]
    drifted = {name: shape for name, shape in heading_shapes.items() if shape != baseline_shape}
    if drifted:
        reporter.fail(f"README localization heading-structure drift: {drifted}")
    else:
        reporter.pass_("all four README files have matching section/subsection structure")

    shared_markers = [
        "original_fictional_persona",
        "historical_inference",
        "historical_archetype_conversion",
        "modern_real_figure_archetype_extraction",
        "composite_archetype",
        "review_valid=true",
        "confirmed",
        "relationship.json.disclaimer_emitted",
        "user_generated/personas/<persona_id>/",
        "persona_dir",
        "fatigued",
        "scripts/validate_repo.py",
        "scripts/run_semantic_tests.py",
        "scripts/validate_game_transaction.py",
        "scripts/validate_game_output.py",
        "quality/TESTING.md",
        "1840",
        "1868",
        "1789",
    ]
    missing = {
        name: [marker for marker in shared_markers if marker not in text]
        for name, text in documents.items()
    }
    missing = {name: markers for name, markers in missing.items() if markers}
    if missing:
        reporter.fail(f"README localization missing shared normative markers: {missing}")
    else:
        reporter.pass_("all four README files share critical source, activation, storage, and testing markers")

    superseded_phrases = {
        "README.md": "and 6 **self-states**",
        "README_cn.md": "与 6 种**自我状态**",
        "README_ja.md": "と6つの**自状態**",
        "README_ko.md": "와 6가지 **자아 상태**",
    }
    found = [name for name, phrase in superseded_phrases.items() if phrase in documents[name]]
    if found:
        reporter.fail(f"README localization contains superseded self-state wording: {found}")
    else:
        reporter.pass_("all four README files use the five-primary-plus-fatigue state model")

    json_block_pattern = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL)
    for name, text in documents.items():
        match = json_block_pattern.search(text)
        if match is None:
            reporter.fail(f"README game example is missing: {name}")
            continue
        try:
            payload = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            reporter.fail(f"README game example JSON is invalid: {name} ({exc})")
            continue
        input_payload = {
            "persona_id": payload.get("persona_id"),
            "event_id": payload.get("event_id"),
            "candidate_actions": payload.get("candidate_actions"),
        }
        errors = validate_game_output(input_payload, payload) if validate_game_output is not None else ["validator unavailable"]
        if errors:
            reporter.fail(f"README game example violates current output contract: {name} ({'; '.join(errors)})")
        else:
            reporter.pass_(f"README game example matches current output contract: {name}")


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
                input_payload,
                reporter,
            )

    if demo_input.exists() and demo_output.exists():
        input_payload = parse_json(demo_input)
        output_payload = parse_json(demo_output)
        if isinstance(input_payload, dict) and isinstance(input_payload.get("candidate_actions"), list):
            validate_output_payload(
                "demo/expected_absolute_majority_output.json",
                output_payload,
                input_payload,
                reporter,
            )

    dialogue_actions = sorted((ROOT / "personas" / "examples").glob("*/dialogue_samples/game_action.json"))
    for dialogue_action in dialogue_actions:
        payload = parse_json(dialogue_action)
        if not isinstance(payload, dict):
            reporter.fail(f"{rel(dialogue_action)} must be an object")
        else:
            input_payload = payload.get("input")
            output_payload = payload.get("expected_output")
            label = rel(dialogue_action)
            validate_input_payload(f"{label}.input", input_payload, reporter)
            if isinstance(input_payload, dict) and isinstance(input_payload.get("candidate_actions"), list):
                validate_output_payload(
                    f"{label}.expected_output",
                    output_payload,
                    input_payload,
                    reporter,
                )


def validate_runtime_security_contracts(reporter: Reporter) -> None:
    helpers = (
        resolve_persona_dir,
        compute_review_artifact_hash,
        validate_game_transaction,
    )
    if any(helper is None for helper in helpers):
        reporter.fail("runtime security helpers could not be imported")
        return

    traversal_ids = ("../oda_nobunaga_modernized", "personas/examples/oda_nobunaga_modernized", "C:\\escape")
    for persona_id in traversal_ids:
        try:
            resolve_persona_dir(persona_id)
        except (ValueError, PersonaContractError):
            reporter.pass_(f"managed persona resolver rejects unsafe ID: {persona_id}")
        else:
            reporter.fail(f"managed persona resolver accepted unsafe ID: {persona_id}")

    input_payload = parse_json(ROOT / "game_adapter" / "sample_input.json")
    output_payload = parse_json(ROOT / "game_adapter" / "expected_output.json")
    blocked = validate_game_transaction(input_payload, output_payload)
    if not blocked.get("valid") and any("activation" in error for error in blocked.get("errors", [])):
        reporter.pass_("game transaction rejects an unconfirmed managed persona")
    else:
        reporter.fail("game transaction did not reject an unconfirmed managed persona")

    malformed = json.loads(json.dumps(input_payload, ensure_ascii=False))
    malformed["public_support_rate"] = -1
    rejected = validate_game_transaction(malformed, output_payload)
    if not rejected.get("valid") and any("input" in error for error in rejected.get("errors", [])):
        reporter.pass_("game transaction rejects malformed input before activation")
    else:
        reporter.fail("game transaction did not reject malformed input")

    duplicate_actions = json.loads(json.dumps(input_payload, ensure_ascii=False))
    duplicate_actions["candidate_actions"].append(duplicate_actions["candidate_actions"][0])
    rejected = validate_game_transaction(duplicate_actions, output_payload)
    if not rejected.get("valid"):
        reporter.pass_("game transaction rejects duplicate candidate actions")
    else:
        reporter.fail("game transaction accepted duplicate candidate actions")

    source_dir = ROOT / "personas" / "examples" / input_payload["persona_id"]
    with tempfile.TemporaryDirectory() as temp_root:
        persona_dir = Path(temp_root) / input_payload["persona_id"]
        shutil.copytree(source_dir, persona_dir)
        persona = parse_yaml(persona_dir / "persona.yaml")
        meta = parse_json(persona_dir / "meta.json")
        persona["meta"]["creation_review_status"] = "confirmed"
        persona["source_provenance"]["last_review_status"] = "confirmed"
        meta.update(
            {
                "latest_review_status": "confirmed",
                "validation_status": "passed",
                "review_invalidated_by_modification": False,
                "reviewed_artifact_hash": "",
            }
        )
        meta["reviewed_artifact_hash"] = compute_review_artifact_hash(persona_dir, persona, meta)
        (persona_dir / "persona.yaml").write_text(
            yaml.safe_dump(persona, allow_unicode=True, sort_keys=False), encoding="utf-8", newline="\n"
        )
        (persona_dir / "meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        relationship = parse_json(persona_dir / "relationship.json")
        relationship["relationship_axes"].update(input_payload["current_relationship"])
        (persona_dir / "relationship.json").write_text(
            json.dumps(relationship, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
        )

        valid = validate_game_transaction(input_payload, output_payload, persona_dir)
        if valid.get("valid") and isinstance(valid.get("state_patch"), dict):
            reporter.pass_("game transaction validates activation and emits schema-valid clamped state patches")
        else:
            reporter.fail(f"valid synthetic game transaction failed: {valid.get('errors')}")

        memory = parse_json(persona_dir / "memory.json")
        memory["persona_id"] = "substituted_persona"
        (persona_dir / "memory.json").write_text(
            json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        substituted = validate_game_transaction(input_payload, output_payload, persona_dir)
        if not substituted.get("valid") and any("memory.json persona_id" in error for error in substituted.get("errors", [])):
            reporter.pass_("game transaction rejects cross-persona mutable-state substitution")
        else:
            reporter.fail("game transaction accepted cross-persona mutable-state substitution")


def main() -> int:
    reporter = Reporter()

    validate_required_files(reporter)
    validate_json_files(reporter)
    validate_yaml_files(reporter)
    validate_skill_frontmatter(reporter)
    validate_example_personas(reporter)
    validate_example_generation_provenance(reporter)
    validate_example_runtime_contracts(reporter)
    validate_scene_cache_contract(reporter)
    validate_activation_entry_points(reporter)
    validate_review_state_executor(reporter)
    validate_oda_dialogue_samples(reporter)
    validate_runtime_cards_testing_behavior(reporter)
    validate_generated_personas(reporter)
    validate_prompt_files(reporter)
    validate_spec_localization_sync(reporter)
    validate_readme_localization_sync(reporter)
    validate_absolute_majority_files(reporter)
    validate_runtime_security_contracts(reporter)

    if reporter.failures:
        print(f"\nFAIL repository validation failed with {len(reporter.failures)} issue(s).")
        return 1

    print("\nPASS repository validation completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
