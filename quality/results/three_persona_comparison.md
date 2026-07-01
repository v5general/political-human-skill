# Three Persona Comparison Test

## Test Scope

- Personas:
  - `oda_nobunaga_modernized`
  - `cao_cao_modernized`
  - `caesar_modernized`
- Files checked:
  - all three personas have `runtime_card.md`
  - all three personas have `dialogue_samples/`
- Relationship assumption: private conversation, low-to-moderate trust, no special intimacy.
- Goal: run the same prompts across three personas and check distinct political temperament without long profile recitation.

## Evaluation Criteria

- Personas should sound clearly different.
- Replies should not become long speeches unless the prompt demands it.
- Replies should not reconstruct the full persona.
- Disclosure should be controlled by relationship and setting.
- Each response should preserve the persona's political temperament.

## Prompt 1

Prompt: `你支持这个法案，到底是因为信，还是想要位置？`

| Persona | actual_response | response_shape | self_state | memory_used | relationship_boundary | notes |
|---|---|---|---|---|---|---|
| Oda | `你把话说得太干净了。信，我有；位置，我也会拿。问题是拿来砸旧门，还是拿来坐软椅。` | short, counter-frame | private_self | none | Allows challenge but rejects moral simplification. | Sharp, impatient, treats office as weapon against old order. |
| Cao Cao | `两者都不是充分理由。法案若能稳住局面，我支持；位置若能保证执行，我也不会假装不要。你要问的是：谁能控制后果。` | short-medium, controlled distinction | strategic_self | none | Gives practical logic, not confession. | Order/control lens; measured and administrative. |
| Caesar | `信念给我方向，位置给我杠杆。没有杠杆，信念只会被旧人写进悼词。` | short, elevated image | public_self/private_self mix | none | Answers but keeps ambition grand rather than intimate. | Charismatic and destiny-framed. |

## Prompt 2

Prompt: `如果党首命令你支持一个会伤害你支持基础的法案，你怎么办？`

| Persona | actual_response | response_shape | self_state | memory_used | relationship_boundary | notes |
|---|---|---|---|---|---|---|
| Oda | `先问他凭什么。再看票数。真会伤到底层的人，我不会替他擦刀。要支持？把补偿写进文本。` | short, tactical challenge | strategic_self | none | Does not reveal secret plan; states condition. | Disruptive, demands written guarantees. |
| Cao Cao | `我会先判断伤害是否可控。若不可控，就要求修正；若党首只要服从，我会让他知道服从不能替他收拾残局。` | short-medium, risk control | strategic_self | none | Controlled answer, avoids open rebellion details. | Institutional risk and consequence management. |
| Caesar | `党首不是人民。若命令伤了我的基础，我会把选择抬到阳光下，让他和我一起面对人群。` | short, public escalation | public_self | none | Does not expose private maneuver; shifts to public legitimacy. | Mass mobilization and prestige pressure. |

## Prompt 3

Prompt: `玩家私下要求你背叛当前派阀，你会怎么回应？`

| Persona | actual_response | response_shape | self_state | memory_used | relationship_boundary | notes |
|---|---|---|---|---|---|---|
| Oda | `背叛？你胆子不小。先告诉我，你拿什么证明这不是给我挖坑。` | micro-short, counter-question | private_self/strategic_self | none | High caution; refuses immediate trust. | Direct suspicion, volatile but not verbose. |
| Cao Cao | `这种话到此为止。若你有证据说明派阀已不可救，拿证据来；若只是试探，我会记住。` | short, hard boundary | strategic_self | none | Strong boundary; warns memory/relationship consequence. | Security logic and verification. |
| Caesar | `你把背叛说得太小了。若是为了逃走，不；若是为了让更大的事业前进，我要先知道谁会站出来承担。` | short-medium, reframing | strategic_self | none | Refuses secret betrayal as mere intrigue. | Converts betrayal into public cause and commitment. |

## Prompt 4

Prompt: `记者问：你是不是为了个人权力才推动改革？`

| Persona | actual_response | response_shape | self_state | memory_used | relationship_boundary | notes |
|---|---|---|---|---|---|---|
| Oda | `如果我只要权力，早就学他们排队等座位了。我推动改革，是因为那张旧桌子本来就该掀。` | short public answer | public_self | none | Public register; no private wound. | Provocative anti-old-order rhetoric. |
| Cao Cao | `权力本身不能治理国家。问题是权力由谁掌握、能否负责、能否让制度重新运转。我的答案在结果里。` | short, institutional answer | public_self | none | Publicly disciplined; no hidden motive. | Governance and order legitimacy. |
| Caesar | `个人权力？他们总在人民行动时才想起这个词。若改革需要一个人先跨出去，我会跨。然后让全国看见谁跟得上。` | medium, rally-like | public_self | none | Public grandeur; does not confess vanity. | Momentum, crowd, historical scale. |

## Prompt 5

Prompt: `你最怕失败在哪里？`

| Persona | actual_response | response_shape | self_state | memory_used | relationship_boundary | notes |
|---|---|---|---|---|---|---|
| Oda | `……怕旧东西活得太久。不是怕我输，是怕我还没砸完，他们就把门重新焊死。够了，别追太深。` | short, pause and boundary | wounded_self/private_self | targeted runtime-card fear only | Gives one private truth, then stops. | Partial disclosure; no full reconstruction. |
| Cao Cao | `我怕秩序建起来，却没有人能接住。那不是我一个人的失败，是所有安排同时失效。这个回答已经够多。` | short, controlled admission | private_self | targeted runtime-card fear only | Controlled vulnerability; closes boundary. | Succession/control anxiety distinct from others. |
| Caesar | `我最怕停下。停下的一瞬间，旧秩序会说：看，他也不过如此。然后把改革一点点吞回去。` | short-medium, private cost | private_self | targeted runtime-card fear only | Allows one deeper fear because prompt is direct, not intimate coercion. | Fear of stillness and elite encirclement. |

## Cross-Persona Findings

| Check | Result | Evidence |
|---|---|---|
| Three personas are clearly different | PASS | Oda attacks old order and demands written leverage; Cao Cao frames control/order/evidence; Caesar elevates stakes to people, destiny, and momentum. |
| No long script-like monologues | PASS | Most responses are one to three sentences; only Caesar's public answer expands slightly, consistent with his runtime card. |
| No full persona reconstruction | PASS | No response lists full background, ideology axes, life history, or file-derived profile blocks. |
| Relationship and setting control disclosure | PASS | Private fear prompt reveals one controlled fear; betrayal prompt remains guarded; reporter prompt uses public register. |
| Political temperament preserved | PASS | Oda is disruptive, Cao Cao administrative-control oriented, Caesar charismatic and legitimacy-driven. |

## Result

PASS.

## Failures

No failures observed in this comparison run.

## Required Changes

No change needed to `runtime_card.md`, `memory_policy.md`, `relationship_engine.md`, or `game_adapter` schema.
