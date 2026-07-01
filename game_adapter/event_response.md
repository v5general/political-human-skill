# 事件响应 · Event Response

> **作用**：定义《绝对多数》与 persona 协作的**端到端事件响应流程**。落地 SPEC 第 14.2 节流程图。评分规则见 `action_scoring.md`，输出结构见 `absolute_majority_schema.json`。

---

## 端到端流程

```text
[1] 游戏状态
      │  游戏向 persona 传入：事件 + 当前游戏状态 + 候选行动 candidate_actions
      ▼
[2] 游戏规则生成候选行动
      │  candidate_actions（如 support_bill / oppose_bill / abstain /
      │   demand_revision / negotiate_budget / leak_to_media /
      │   join_rebellion / stay_silent）
      ▼
[3] Political Human Skill 评分
      │  按 action_scoring.md：人格 + 关系 + 记忆 + 政治处境 + 五力驱动
      │  → 每个 candidate_action 得分（0~100）
      ▼
[4] 输出 JSON（absolute_majority_schema.json）
      │  selected_action + action_scores + public_statement
      │  + private_reason + emotional_state
      │  + relationship_delta + memory_write + score_drivers
      ▼
[5] 游戏执行结果
      │  按 selected_action 推进剧情/数值
      ▼
[6] 写入 NPC 记忆 + 反作用于社会（仅本命名空间）
      │  memory_write → personas/{slug}/memory.json
      │  relationship_delta → personas/{slug}/relationship.json
      │  重大事件 → persona_evolution 偏移（core/persona_evolution.md）
      │  selected_action + public_statement → social_impact_hint（反作用于社会：舆论/选区/派阀）
      │  （core/memory_policy.md：只写当前 NPC；社会状态由游戏侧执行）
```

---

## 关键约束

### persona 不自由生成行动

本框架的 NPC **不**脱离候选行动自由发挥。`selected_action` 必须是 `candidate_actions` 之一。这保证了游戏的可控性与可调试性，persona 的“自由意志”体现在**评分与选择**，而非无中生有。

### 公开/私下分离

同一事件产出两层话语：

- `public_statement`：公开口径（public_self）；
- `private_reason`：私下真实理由（strategic/private self）。

游戏可据此呈现“台面上/台面下”的双层叙事——这正是政治游戏的核心张力。

### 记忆写回隔离

第 6 步只写当前 NPC 的 `memory.json` / `relationship.json`。A 议员在此事件中与玩家的交锋，不进入 B 议员的记忆（`core/memory_policy.md`）。

---

## 多 NPC 同事件

同一事件可能触发多个 NPC 的响应。每个 NPC **独立**走一遍 [1]→[6]，各自加载自己的 persona/关系/记忆，互不串扰。玩家与 A 的私下交易，B 不知道——除非事件本身是公开的（写入 `public_world_events`）。

---

## 失败兜底

| 情形 | 兜底 |
|---|---|
| 候选行动集为空 | persona 不输出行动，回报“无可选行动”，等游戏补充 |
| 评分最高行动明显违背 persona 核心设定 | 走 trauma_trigger 非理性偏离逻辑，并在 private_reason 解释；否则回 `action_scoring.md` 复查权重 |
| 事件触及红线（如要求冒充现实人物） | 拒绝（`core/safety_boundaries.md`），不输出行动 |
| 记忆/关系文件缺失 | 用 templates 初始化为 stranger + 空记忆后继续 |
