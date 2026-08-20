# Demo Guide

This directory shows the minimum host flow: activation preflight, one fast dialogue path, and one Absolute Majority structured decision path. Markdown examples are illustrative; they do not bypass approval state.

The Absolute Majority JSON files intentionally mirror the canonical `game_adapter/` fixtures so this directory remains a self-contained runnable demo. `scripts/validate_repo.py` validates both copies and their exact pairings; contract changes must update both.

## Choose A Persona

Start from `personas/examples/oda_nobunaga_modernized/` for the demo. Use:

- `meta.json`, `persona.yaml`, and `creation_review.md` for the mandatory `core/activation_gate.md` preflight.
- `runtime_card.md` for fast dialogue.
- `persona.yaml` only when the dialogue touches deeper personality, old wounds, political motive, or safety-relevant identity details.
- `relationship.json` to choose the trust/register level.
- `memory.json` to bring in recent persona-owned memory and to append short updates after meaningful events.

## Fast Dialogue

Read `demo/run_dialogue_demo.md`.

The flow is:

1. Run `uv run python scripts/review_state.py check oda_nobunaga_modernized` (the gate executor). The shipped Oda fixture is unconfirmed, so an actual run stops with `decision=blocked` and a remediation `next_action`; follow it: full review, then `scripts/review_state.py commit oda_nobunaga_modernized`.
2. `check` then returns `confirm_prompt`; present the review, and on explicit user confirmation run `scripts/review_state.py confirm oda_nobunaga_modernized`. Only after `decision=activate` load `runtime_card.md` and `relationship.json`.
3. Answer the user's casual line in the current register.
4. If the user asks about an old name, wound, or deep motive, do a targeted lookup in `persona.yaml`.
5. Keep the reply conversational instead of reconstructing the whole persona.
6. Write a short `memory_update` only if the exchange changes future behavior.

## Absolute Majority Decision

Read `demo/run_absolute_majority_demo.md`.

The flow is:

1. Resolve `persona_id` and run `core/activation_gate.md`; unconfirmed personas produce no game action.
2. Load `demo/sample_absolute_majority_input.json` only after confirmation.
3. Confirm that `candidate_actions` is the action set supplied by the game.
4. Score actions from persona, relationship, memory, support base, and parliamentary context.
5. Emit JSON shaped like `demo/expected_absolute_majority_output.json`.
6. Pass `memory_write` into the next turn's `recent_memory`.

## Validate The Repository

Install the YAML dependency if needed:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python scripts/validate_repo.py
```
