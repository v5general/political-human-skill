# Absolute Majority Demo

This demo uses a fiscal reform budget event.

## 1. Input

Load:

- `demo/sample_absolute_majority_input.json`
- `game_adapter/absolute_majority_input_schema.json`
- `game_adapter/absolute_majority_schema.json`

The game supplies this action set:

```json
[
  "support_bill",
  "oppose_bill",
  "demand_revision",
  "negotiate_budget",
  "stay_silent"
]
```

## 2. Decision Pass

Score each action from:

- Persona action style: fast, disruptive, anti-empty-compromise.
- Relationship: low trust, moderate respect, high caution.
- Memory: the player recently acted through the press without warning him.
- Support base: district supporters want material guarantees.
- Parliament context: narrow vote margin creates leverage.

## 3. Output

Emit JSON shaped like:

- `demo/expected_absolute_majority_output.json`

The selected action is `demand_revision` because it attacks the weak budget design without wasting the vote on pure opposition.

## 4. Memory Write

The output includes:

```json
{
  "memory_write": [
    "In budget_reform_001, the player asked for a bolder amendment without collapsing the coalition; he chose to demand written revisions instead of symbolic support."
  ]
}
```

## 5. Next Turn Use

On the next game event, pass that line into `recent_memory`. It should make the NPC slightly more willing to treat the player as tactically useful, while still cautious about press handling and vague compromise.
