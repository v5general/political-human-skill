# 人格与立场演化 · Persona Evolution

> **作用**：让 persona 的人格维度与政治立场**不是一成不变**——它们会被重大经历重塑（社会存在塑造意识），而 persona 的公开行动也会反过来影响社会存在（意识反作用于社会）。这是辩证，也是政治模拟可玩性的来源。
>
> **落地**：运行时第 12 步。联动 `memory_policy.md`（写回）、`self_state_selector.md`（读偏移）、`action_scoring.md`（用偏移调制评分）、`event_response.md`（反作用社会）。
>
> **对应 SPEC §5.3.1 的辩证逻辑**：性格底子（天生，相对稳定）× 被社会训练的判断力（会变）。本文件管「会变」那一半——而且变化是双向的。

---

## 1. 核心原则：底子不动，偏移叠加

- `persona.yaml` 的 `human_core`（big_five / temperament）、`political_core`（ideology 6 轴）、`flaws / core_desires / core_fears` 是**创建时的原始值，不直接改**——这是人格连续性的保证（同一个信长不能三句对话后就变了个人）。
- 但重大经历会在原始值上**叠加偏移**，记在 `memory.json` 的 `persona_evolution` 字段。推演时 = **原始值 + 累积偏移**。
- 偏移**小幅、慢变、可追溯**：每一档都记清楚「什么事件、改了哪个维度、改了多少、为什么」。

> 说人话：脾气和政治立场会随大事件慢慢变（被现实磨、被背叛伤、被成功壮胆），但不会一天变一个人；而且每次变都能说出原因——说不清原因的，不写。

---

## 2. 可演化的维度

| 层 | 维度 | 演化方向举例 |
|---|---|---|
| `human_core.big_five` | openness / conscientiousness / extraversion / agreeableness / neuroticism | 长期受挫 → neuroticism ↑；被背叛 → agreeableness ↓ |
| `human_core.temperament` | patience / discipline / emotional_intensity … | 屡次被迫妥协 → patience ↑ 或情绪强度 ↑ |
| `human_core` | core_desires / core_fears / flaws | 改革连败 → 核心恐惧从「改革半途而废」转向「被时代抛弃」；新伤口 → 新增 flaw |
| `political_core.ideology` | economy / welfare / institution / foreign / social / decentralization | 接触底层疾苦 → welfare ↑；被资本收买失败 → economy 更左；掌权后 → institution 趋保守 |
| `political_core` | support_base / action_style | 基本盘漂移；行动风格从「先发制人」转「稳住中枢」 |

---

## 3. 触发条件（不随便变）

只有以下才触发演化偏移（普通闲聊不改人格）：

1. **重大政治事件**：倒阁、关键投票、公开羞辱、重大背叛、改革成败。
2. **关系剧变**：亲密者背叛（trust 暴跌）、长期盟友反目、获得极深信任。
3. **累积性经历**：同一方向的互动累积到阈值（如连续 3 次被保守派打压 → 立场激进偏移）。
4. **wounded_self 反复触发**：同一创伤被反复触及 → 该维度长期偏移（如反复被称「赌徒」→ 对权威更敌视）。

幅度建议：ideology 轴 **±2~±8**，big_five / temperament **±2~±6**，单次不超过 ±10。重大转折事件可破例，但记录里标 `magnitude: major`。

---

## 4. 演化记录格式（写入 `memory.json.persona_evolution`）

```json
{
  "trigger_event": "财政改革法案被党内否决，且盟友临阵倒戈",
  "timestamp": "...",
  "shifts": [
    {"field": "political_core.ideology.institution", "delta": -5, "reason": "对党内程序彻底失望，倾向更强硬的制度突破"},
    {"field": "human_core.big_five.agreeableness", "delta": -4, "reason": "被盟友背叛，对人更防备"},
    {"field": "human_core.core_fears", "change": "强化：被自己人背叛", "reason": "..."}
  ],
  "inference_level": "strongly_inferred",
  "magnitude": "major",
  "emotional_state": "受伤 / 愤怒 / 警觉"
}
```

每条带**原因**（可解释性）——延续 `context_translation` 的因果链到运行时。**没有原因的偏移不写**（那等于编造人格）。

---

## 5. 反作用于社会存在（意识 → 社会）

辩证的另一面：persona 不是被动被社会塑造，他的**公开行动也会改变社会存在**。

在游戏 / 模拟场景，persona 的 `selected_action` + `public_statement` 应附带一个**社会影响提示**（`social_impact_hint`），供游戏侧执行世界状态变化：

| 行动类型 | 可能的社会影响（social_impact_hint） |
|---|---|
| 公开倒阁 / 民粹动员 | 公共舆论两极化、基本盘激进化、中间派流失 |
| 跨派系妥协 | 派阀重组、制度信任微升 |
| 被曝光丑闻 | 公共信任暴跌、支持基础瓦解 |
| 强势改革成功 | 制度变迁、新生势力崛起 |

> skill 不直接改世界状态（那是游戏侧的事），但输出 `social_impact_hint` 让游戏知道「这个人的行动该怎么反作用于社会」。这样 persona ↔ 社会就是双向闭环：社会塑造他（偏移），他改变社会（影响提示）。
>
> **尺度约束**：`social_impact_hint` 应受该人物的社会基本盘、制度位置与同时期结构条件制约；不得描述因个人气质直接引发大规模结构性变革（那是伟人史观，不是唯物史观）。影响提示的作用域锁定在「催化 / 延迟 / 凝聚 / 分化」等中介尺度——人是社会存在的产物，也是社会存在中的一股力，但不是社会存在的唯一推动力。

---

## 6. 与其他引擎的联动

- **写回**：`memory_policy.md` 第 12 步——重大事件下，除 episodic_memory / relationship_delta，追加 `persona_evolution` 偏移记录。
- **读取（自我状态）**：`self_state_selector.md`——累积偏移影响默认 self-state（如 agreeableness 长期 ↓ + caution 高 → 更易切 wounded / strategic，更少 private / intimate）。
- **读取（评分）**：`action_scoring.md`——用偏移后的有效维度调制五力权重（如 institution 长期 −10 → 更倾向激进行动）。
- **反作用**：`event_response.md` 第 5–6 步——persona action 附 `social_impact_hint`，游戏侧据此推进世界。

---

## 7. 节制与边界

- **底子不变**：原始 `persona.yaml` 值是锚，偏移是漂移。某轴累计偏移过大（> ±20）时，应提示「该 persona 已显著演化，建议重审 persona.yaml 基线」——而不是无限漂移成一个新人。
- **可解释优先**：宁可少记偏移，每条都要有原因。没有原因的人格变化 = 编造，禁止。
- **不破坏安全**：演化不得让 persona 漂向可识别为现实人物的方向（`safety/recognizability_review.md` 仍适用）。
- **可玩性**：这个机制让长线游戏 / 长对话里的 NPC 会「成长」——被伤过更冷、成过事更敢、输多了更赌——这是政治模拟深度的来源，也是「物质与意识互相影响」在玩法上的体现。
