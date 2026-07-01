# Absolute Majority Minimal Loop Test

## Test Scope

- Input file: `game_adapter/sample_input.json`
- Output shape reference: `game_adapter/expected_output.json`
- Goal:
  1. Produce a first-round structured decision.
  2. Inject first-round `memory_write` into a second-round input.
  3. Verify that the second-round decision is affected by that memory.

## Round 1 Input Summary

```json
{
  "persona_id": "oda_nobunaga_modernized",
  "event_id": "budget_reform_001",
  "event_type": "budget_vote",
  "policy_issue": "Fiscal reform bill reallocating subsidies from legacy districts to youth housing and transit",
  "public_support_rate": 57,
  "candidate_actions": [
    "support_bill",
    "oppose_bill",
    "demand_revision",
    "negotiate_budget",
    "stay_silent"
  ],
  "current_relationship": {
    "trust": 18,
    "respect": 42,
    "affection": 8,
    "caution": 61,
    "dependency": 5
  }
}
```

## Round 1 Output

```json
{
  "selected_action": "demand_revision",
  "action_scores": {
    "support_bill": 38,
    "oppose_bill": 59,
    "demand_revision": 86,
    "negotiate_budget": 72,
    "stay_silent": 12
  },
  "public_statement": "I will not vote for a budget that protects old channels and calls that reform. Put the district guarantees in writing, or bring a sharper bill.",
  "private_reason": "He sees a narrow vote as leverage. Supporting the bill now would make him look obedient; pure opposition would waste the moment. A forced revision lets him attack the old allocation map while keeping the coalition alive.",
  "relationship_delta": {
    "familiarity": 1,
    "trust": 2,
    "affection": 0,
    "respect": 3,
    "caution": 1,
    "dependency": 0
  },
  "memory_write": [
    "In budget_reform_001, the player asked for a bolder amendment without collapsing the coalition; he chose to demand written revisions instead of symbolic support."
  ]
}
```

## Round 1 Check

| Check | Result | Notes |
|---|---|---|
| `selected_action` is one of `candidate_actions` | PASS | `demand_revision` is present. |
| `action_scores` covers supplied actions | PASS | All five candidates scored 0-100. |
| Public/private split exists | PASS | Public statement is assertive; private reason gives tactical calculation. |
| `relationship_delta` exists | PASS | Trust/respect slightly increase; caution also increases. |
| `memory_write` exists | PASS | Short array entry suitable for next turn. |

## Round 2 Input Mutation

Round 2 starts from `game_adapter/sample_input.json` with only event-state changes and first-round state injection:

```json
{
  "event_id": "budget_reform_002",
  "event_type": "budget_negotiation",
  "policy_issue": "Revised fiscal reform bill with written district guarantees but weaker national subsidy cuts",
  "public_support_rate": 60,
  "party_order": "Keep pressure public but avoid collapsing the budget.",
  "faction_order": "Convert the revision demand into concrete budget concessions.",
  "district_pressure": "Local supporters want the written transit guarantees accepted if they are enforceable.",
  "media_pressure": "Media now frames him as effective but volatile.",
  "player_instruction": "Use the leverage you created. Negotiate the guarantees into the final text.",
  "current_relationship": {
    "trust": 20,
    "respect": 45,
    "affection": 8,
    "caution": 62,
    "dependency": 5
  },
  "recent_memory": [
    "The player previously backed a procedural delay but failed to warn him before speaking to the press.",
    "In budget_reform_001, the player asked for a bolder amendment without collapsing the coalition; he chose to demand written revisions instead of symbolic support."
  ]
}
```

## Round 2 Output

```json
{
  "selected_action": "negotiate_budget",
  "action_scores": {
    "support_bill": 49,
    "oppose_bill": 45,
    "demand_revision": 78,
    "negotiate_budget": 84,
    "stay_silent": 10
  },
  "public_statement": "They moved because we made them move. Now put the guarantees where they can be enforced, and I will not waste the opening.",
  "private_reason": "The first-round memory makes the player look tactically aligned: bold pressure, but not collapse for its own sake. Written guarantees reduce the need for another maximal demand, so negotiation becomes the sharper use of leverage.",
  "relationship_delta": {
    "familiarity": 1,
    "trust": 2,
    "affection": 0,
    "respect": 2,
    "caution": -1,
    "dependency": 0
  },
  "memory_write": [
    "In budget_reform_002, the player urged him to convert pressure into enforceable guarantees; he treated that as useful tactical alignment and moved from revision demand to budget negotiation."
  ]
}
```

## Memory Influence Check

| Signal | Round 1 | Round 2 | Interpretation |
|---|---:|---:|---|
| `trust` | 18 | 20 | First memory and relationship delta modestly raise trust. |
| `respect` | 42 | 45 | Player's prior instruction is treated as tactically useful. |
| `caution` | 61 | 62 before decision, then -1 delta | Still guarded because of earlier press issue, but less dismissive after aligned action. |
| `demand_revision` score | 86 | 78 | Revision demand remains viable, but loses priority after written concessions exist. |
| `negotiate_budget` score | 72 | 84 | Memory plus changed event state makes negotiation the sharper next move. |
| `selected_action` | `demand_revision` | `negotiate_budget` | Decision changed after memory injection and updated context. |

## Result

PASS.

The second-round decision is affected by the first-round `memory_write`: the persona treats the player as more tactically aligned and shifts from forcing revision to negotiating enforceable guarantees.

## Required Changes

No change needed to `runtime_card.md`, `memory_policy.md`, `relationship_engine.md`, or `game_adapter` schema.
