# Demo Guide

This directory shows the minimum runnable shape of the framework: one fast dialogue path and one Absolute Majority structured decision path.

## Choose A Persona

Start from `personas/examples/oda_nobunaga_modernized/` for the demo. Use:

- `runtime_card.md` for fast dialogue.
- `persona.yaml` only when the dialogue touches deeper personality, old wounds, political motive, or safety-relevant identity details.
- `relationship.json` to choose the trust/register level.
- `memory.json` to bring in recent persona-owned memory and to append short updates after meaningful events.

## Fast Dialogue

Read `demo/run_dialogue_demo.md`.

The flow is:

1. Load `runtime_card.md`.
2. Load `relationship.json`.
3. Answer the user's casual line in the current register.
4. If the user asks about an old name, wound, or deep motive, do a targeted lookup in `persona.yaml`.
5. Keep the reply conversational instead of reconstructing the whole persona.
6. Write a short `memory_update` only if the exchange changes future behavior.

## Absolute Majority Decision

Read `demo/run_absolute_majority_demo.md`.

The flow is:

1. Load `demo/sample_absolute_majority_input.json`.
2. Confirm that `candidate_actions` is the action set supplied by the game.
3. Score actions from persona, relationship, memory, support base, and parliamentary context.
4. Emit JSON shaped like `demo/expected_absolute_majority_output.json`.
5. Pass `memory_write` into the next turn's `recent_memory`.

## Validate The Repository

Install the YAML dependency if needed:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python scripts/validate_repo.py
```
