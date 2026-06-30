# 行动评分 · Action Scoring

> **作用**：定义 persona 如何对游戏候选行动**评分**。落地 SPEC 第 14.2 节、SKILL.md 第 7 节。输出结构见 `absolute_majority_schema.json`，事件响应流程见 `event_response.md`。
>
> **核心理念**：NPC 不是按数值机械投票，而是按“一个完整的人 + 政治职业”在候选行动中做判断。评分要可解释、可调试。

---

## 评分输入

```text
action_scores = f(
    persona.yaml            人格档案（人性核心 + 政治职业 + 自我状态 + 内在冲突）
  , relationship.json       该 NPC 对玩家的关系（trust/respect/caution…）
  , memory.json             该 NPC 独占记忆（承诺/冲突/恩怨/创伤）
  , event_context           当前事件 + 游戏状态（选区压力/派阀命令/权力格局）
  , candidate_actions       游戏规则本次提供的候选行动集
)
```

---

## 五大评分驱动力（score_drivers）

每个候选行动的分数，由以下五力共同作用（见 schema 的 `score_drivers`）：

| 驱动力 | 来自 | 作用方向 |
|---|---|---|
| **support_base_pressure**（支持基础压力） | `political_core.support_base` + 选区处境 | 维护支持基础的行动 ↑，损害的 ↓ |
| **faction_pressure**（派阀压力） | `party_faction` + 派阀命令 | 符合派阀利益的 ↑ |
| **personal_ambition**（个人野心） | `human_core.core_desires` + `current_role` | 有利于晋升/权力的 ↑ |
| **personal_grudge**（政治恩怨） | `memory.json` 承诺冲突 + 对玩家/他者的既有态度 | 报复/抵制的 ↑，报恩的合作 ↑ |
| **trauma_trigger**（创伤触发） | `human_core.core_fears/flaws/emotional_triggers` + `wounded_self` | 命中创伤时可能**非理性偏离最高分** |

> 五力并非等权——由 persona 的性格决定权重。例如 high discipline 的角色给 ambition 打折；high neuroticism 的角色在 trauma_trigger 下权重大增。

---

## 评分流程

1. **初始化**：每个候选行动给一个基准分（如 50）。
2. **五力加减**：按各驱动力对每个行动加减分（0~100 区间）。
3. **人格调制**：用 `human_core`（big_five/temperament）与 `inner_conflicts` 调制权重。内在冲突被触及时，分数会体现“纠结”——两个相近的高分。
4. **关系调制**：玩家在此事件中的行为（施压/利诱/背信）通过 `relationship_delta` 反向影响评分。
5. **非理性偏离**：若命中 `trauma_trigger`，`selected_action` 可不取最高分——模拟真实政治人因愤怒/恐惧/自尊做出的次优选择。这必须在 `private_reason` 中说明。

---

## 评分示例（落实 SPEC 14.2）

事件：财政改革法案，玩家（首相）要求该 NPC 公开支持。

```json
{
  "selected_action": "negotiate_budget",
  "action_scores": {
    "support_bill": 58, "oppose_bill": 41, "abstain": 35,
    "demand_revision": 72, "negotiate_budget": 86,
    "leak_to_media": 49, "join_rebellion": 27, "stay_silent": 31
  },
  "score_drivers": {
    "support_base_pressure": "选区依赖地方公共支出，直接支持损害选区关系",
    "faction_pressure": "派阀要求换取预算补偿再表态",
    "personal_ambition": "希望借机向首相索取地方预算承诺，累积政绩",
    "personal_grudge": "玩家此前未兑现承诺，有怨气",
    "trauma_trigger": "无"
  }
}
```

解读：`negotiate_budget` 最高（86）——既不公开对抗首相，又为选区争取筹码，符合该 NPC 的现实主义 + 内在冲突（想改革但靠公共支出）。

---

## 与运行时引擎的关系

- 评分用到的关系状态 → `core/relationship_engine.md`；
- 评分用到的记忆/恩怨 → `core/memory_policy.md`；
- emotional_state 与创伤触发 → `core/self_state_selector.md`（可能激活 wounded_self）；
- 评分结果中的 `relationship_delta` / `memory_write` → 只写回该 NPC 命名空间。

---

## 评分伪代码（处境 + 自我状态 → 行动评分）

> 落地评审建议：给出「处境变量 + 激活的自我状态」如何换算成候选行动评分的具体映射，避免实现时行为不一致。

```python
def score_actions(persona, relationship, memory, event, candidates):
    # 1. 每个候选行动给基准分
    scores = {a: 50 for a in candidates}
    # 2. 由场合+关系锁定主自我状态（见 core/self_state_selector.md 转换矩阵）
    active_state = select_self_state(persona, event.context, relationship.stage)

    for a in candidates:
        # 五大评分驱动力（对应 schema 的 score_drivers）
        scores[a] += W["support"]  * support_base_pressure(persona, a, event)  # 选区 / support_base
        scores[a] += W["faction"]  * faction_alignment(persona, a, event)      # 派阀利益
        scores[a] += W["ambition"] * ambition_gain(persona, a, event)          # core_desires / current_role
        scores[a] += W["grudge"]   * grudge_bias(persona, memory, a)           # 承诺冲突 / 恩怨
        # 创伤触发：命中 core_fears/emotional_triggers → 激活 wounded_self
        if triggers_trauma(persona, event):
            active_state = "wounded_self"
            scores[a] += W["trauma"] * trauma_override(persona, a, event)

        # 人格调制（big_five / temperament / inner_conflicts 决定权重倾向）
        scores[a] = modulate(scores[a], persona.human_core, persona.inner_conflicts)
        # 关系调制（玩家施压 / 利诱 / 背信反向影响）
        scores[a] += relationship_modifier(relationship, event.player_action)

    scores = {a: clip(s, 0, 100) for a, s in scores.items()}
    # 选择：wounded_self 下允许非理性偏离最高分（须在 private_reason 说明）
    selected = wounded_choice(persona, scores) if active_state == "wounded_self" else argmax(scores)
    return selected, scores, active_state
```

**权重 W 由 persona 性格决定**：`discipline` 高 → `ambition` 权重打折；`neuroticism` / `emotional_intensity` 高 → `trauma` 权重放大；`inner_conflicts` 被触及 → 产生两个相近高分（纠结）。`wounded_self` 是唯一允许 `selected_action ≠ argmax` 的状态，模拟真实政治人因愤怒/恐惧做出的次优选择。
