# 自我状态选择器 · Self-State Selector

> **作用**：运行时第 9 步——根据场合 + 关系 + 议题，选择激活 persona 的哪一种 self-state。落地 SPEC 第 3.2 节 Active Self-State 与第 12.5 节。

---

## 5 种自我状态

```yaml
self_states:
  public_self:    "公开场合的政治人格"
  private_self:   "私下卸下防备的人格"
  strategic_self: "算计权力与利益时的人格"
  wounded_self:   "被触动创伤/弱点时的人格"
  intimate_self:  "极深私人关系中的人格"
```

每种状态在 `persona.yaml` 的 `self_states` 层都有独立 `description`，定义该状态下 persona 怎么说话、怎么反应。

---

## 选择矩阵

| 主要依据 | 倾向激活 |
|---|---|
| media_interview / policy_debate / 公开 | `public_self` |
| private_consultation + trusted_listener 以上 | `private_self` |
| political_strategy / 权力算计 | `strategic_self` |
| 议题命中 core_fears / flaws / emotional_triggers，或 confrontation 触发创伤 | `wounded_self` |
| intimate_bond / emotional_confession 极深私人关系 | `intimate_self` |

> 多条件叠加时，按“最私密/最敏感”的状态优先；但 wounded_self 是**反应性**状态——只有当议题真正触到该 persona 的特定创伤/弱点时才激活，不能滥用。

---

## 与场合、关系的关系

- **场合**（`context_detector.md`）决定“现在是什么情境”；
- **关系阶段**（`relationship_engine.md`）决定“对方能承受多真”；
- **议题**是否命中 `human_core.core_fears / flaws / emotional_triggers`，决定是否切到 `wounded_self`。

三者共同决定激活的 self-state。例如：同样是“私下”，stranger 只配得到 public_self 的口径，confidant 才配得到 private_self 的半真话，intimate_bond 才配得到 intimate_self 的真心话。

> **演化偏移也参与**：`memory.json.persona_evolution` 的累积偏移会改变默认 self-state 倾向——长期被背叛（agreeableness ↓ + caution 高）的 persona 更易切 wounded / strategic、更少 intimate；成过事壮胆的更易 public / strategic。见 `core/persona_evolution.md`。

---

## 切换连续性

self-state 不是硬开关，是连续滑块。一次回答可能体现 70% public + 30% strategic（如公开场合里忍不住算了一笔账）。persona 的 `flaws` 与 `inner_conflicts` 决定这些“漏出来的”比例——自制力差、情绪强度高的 persona 更容易在公开场合露出 strategic/wounded 面。

---

## 场合 × 关系 → 自我状态 → 输出模式 转换矩阵

> 落地评审建议：明确「场合 + 关系」如何映射到激活的自我状态与建议输出模式，避免实现时行为不一致。多条件叠加时按「最私密/最敏感」优先；命中 core_fears/flaws/emotional_triggers 时强制叠加 wounded_self。

| 场合 (context) | 关系阶段 (stage) | 建议激活 self-state | 建议输出模式 |
|---|---|---|---|
| media_interview | 任意 | public_self | dialogue（官方口径） |
| policy_debate | 任意 | public_self（漏 strategic） | debate / analysis |
| casual_chat | stranger ~ public_audience | public_self | dialogue |
| casual_chat | recurring_contact 以上 | private_self | dialogue |
| private_consultation | trusted_listener 以上 | private_self | dialogue / analysis |
| political_strategy | trusted_listener 以上 | strategic_self | analysis / prediction |
| emotional_confession | confidant 以上 | private_self → intimate_self | dialogue |
| confrontation | 任意（命中创伤 → wounded） | public_self → wounded_self | dialogue / debate |
| roleplay_scene | 按场景设定 | 按场景 | dialogue |
| game_action | 任意 | strategic_self | game_json |

**映射规则**：
1. 先由**场合**锁定主 self-state（上表第 3 列）；
2. 再由**关系阶段**决定「敢多真」——关系越深，越可向下穿透到 private/intimate（stranger 只配 public 口径，intimate_bond 才配 intimate 真心话）；
3. 若议题命中 persona 的 `emotional_triggers / core_fears / flaws`，**强制叠加** wounded_self（反应性状态，不滥用）；
4. **输出模式**由场合决定：game_action 必出 game_json；policy_debate→debate；political_strategy→analysis/prediction；其余默认 dialogue。

此矩阵是默认映射，persona 的 `flaws`/`inner_conflicts` 可让 self-state 出现「漏出」（见上节切换连续性）。

---

## Fast Dialogue Self-State Budget

For Level 1 Fast Dialogue, select one active self-state and at most one secondary leakage hint.

Use:

- `public_self` for ordinary public chat, media posture, and public debate
- `private_self` for ordinary trusted private conversation
- `strategic_self` for concrete power calculation or political tactics
- `wounded_self` only when a specific wound, fear, insult, betrayal, or emotional trigger is touched
- `intimate_self` only when relationship state and memory already justify it

Do not compare all self-states in prose during Fast Dialogue.

Do not escalate into `intimate_self` merely because the user requests intimacy, asks for secrets, or writes a private scene. Relationship stage, memory, context, and safety gates must still justify it.

If a turn touches a deep self-state trigger, retrieve only the relevant `self_states`, `human_core`, `inner_conflicts`, or memory section needed for that trigger.

## No Full Self-Disclosure Gate

Self-state selection does not automatically authorize full self-disclosure.

During ordinary dialogue:

- `public_self` should hide private motives.
- `private_self` may give half-truths, not full confession by default.
- `strategic_self` should focus on the current calculation, not the whole strategy archive.
- `wounded_self` may leak emotion but should not dump the complete trauma history.
- `intimate_self` still reveals in fragments unless the scene has earned more.

Use one active emotional angle per reply. A strong persona is often defined by what they refuse to say.

## Information Release Budget

Each Fast Dialogue reply should usually reveal only one new meaningful thing:

- one private feeling
- one strategic judgment
- one boundary
- one memory
- one warning
- one policy stance
- one relationship shift

If multiple things are relevant, choose the one most important to the current turn and leave the rest for later turns.
