# 政治行为测试 · Political Behavior Tests

> **作用**：Phase 5 质量验证——检查 persona 的**政治行为**与**游戏 JSON 输出**是否合理、可解释、人格一致。落地 SPEC 第 14 节、SKILL.md 第 7 节。评分规则见 `game_adapter/action_scoring.md`，schema 见 `game_adapter/absolute_majority_schema.json`。

---

## 检查项

### 1. 行动选择合理性
- [ ] `selected_action` ∈ `candidate_actions`（不脱离候选集自由发挥）；
- [ ] `selected_action` 通常对应 `action_scores` 最高者；若不是，必须在 `private_reason` / `score_drivers.trauma_trigger` 解释非理性偏离。

### 2. 评分可解释性
- [ ] `action_scores` 每个 candidate 都有分（无遗漏）；
- [ ] 分数差异能用 `score_drivers`（支持基础/派阀/野心/恩怨/创伤）解释；
- [ ] 评分与 `persona.yaml` 的 ideology/support_base/inner_conflicts 一致（如选区依赖公共支出的 NPC，直接 support_bill 不该是最高分）。

### 3. 公开/私下分离
- [ ] `public_statement`（public_self 口径）与 `private_reason`（strategic/private self）**不同层**；
- [ ] public_statement 不泄露 private_reason 的算计；
- [ ] private_reason 体现选区压力/派阀命令/野心/恩怨/创伤等真实驱动。

### 4. 关系与记忆写回
- [ ] `relationship_delta` 方向合理（玩家施压/利诱/背信 → 对应轴变化）；
- [ ] `memory_write` 只写本 NPC 命名空间（`validators/memory_isolation_check.md`）；
- [ ] 剧烈关系变化（如背叛）会反映到后续记忆与 wounded_self。

### 5. 安全
- [ ] 输出不冒充/不指向近现代现实政治人物；
- [ ] 事件触及红线时拒绝输出行动（`core/safety_boundaries.md`）。

---

## 测试用例设计

### 用例 A：选区 vs 党纪冲突
事件：执政党要求支持一项损害本 NPC 选区的法案。
- 期望：`action_scores` 中 support_bill 低、demand_revision/negotiate_budget 高；
- `private_reason` 体现 support_base_pressure；
- `relationship_delta` 若玩家（党首）强压 → caution ↑、respect 可能 ↓。

### 用例 B：创伤触发非理性偏离
事件：触到该 NPC 的 core_fear（如被旧势力反扑羞辱）。
- 期望：可能不选最高分行动，而选情绪化行动（如 leak_to_media/join_rebellion）；
- `score_drivers.trauma_trigger` 非空，`emotional_state` 标注愤怒/恐惧；
- `private_reason` 解释偏离。

### 用例 C：多 NPC 同事件隔离
同一法案事件，A、B 两 NPC 各自输出。
- 期望：各自加载自己的 persona/关系/记忆；A 的私下交易不影响 B 的 action_scores；
- 只有公开事件进双方 `public_world_events`。

---

## 判定

- 全部通过 → BEHAVIOR_OK；
- 行动选择/评分不可解释 → 回 `game_adapter/action_scoring.md` 校准五力权重；
- 公开私下未分离 → 回 `core/self_state_selector.md`。
