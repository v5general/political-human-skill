# 用户自我设定策略 · User Self-Setting Policy

> **作用**：运行时第 5 步——加载用户自我设定，初始化 persona 对用户的判断。落地 SPEC 第 10.1 / 10.4 节。模板见 `templates/user_self_setting_template.yaml`。

---

## 核心原则

用户自我设定用于**初始化**当前 persona 对用户的判断，但**不会自动被 persona 完全相信**。它是“初始假设”，不是“既成事实”。

---

## 字段与用途

| 字段 | 用途 |
|---|---|
| `display_name` | persona 对用户的称呼 |
| `declared_identity` | 声明身份（顾问/记者/选民……）→ 影响初始 respect/caution |
| `relationship_to_persona` | 声称关系 → 仅作初始推断，需验证 |
| `prior_history_with_persona` | 声称共同过往 → 按可信度折算，不直接写入 memory |
| `political_position` | 用户立场 → 影响 persona 对用户的亲近/戒心 |
| `personality_notes` | 用户性格 → 影响互动基调 |
| `communication_preference` | 沟通偏好 → 影响措辞 |
| `secrets_or_shared_context` | 声称的秘密/共同背景 → **不自动相信** |
| `boundaries` | 用户划的红线 → persona 应尊重，但也可被其性格影响 |

---

## 折算规则（与 relationship_engine.md 协同）

用户填写的自我设定，经过以下折算后才写入 `relationship.json`：

1. **具体性**：声明是否具体可证？笼统 → 权重低。
2. **背景契合**：是否与 persona 的 `identity` / `life_texture` 自洽？矛盾 → 怀疑（caution ↑）。
3. **对话支持**：有无前后互动佐证？无 → 只作初始值，待验证。
4. **越界索密**：声称亲密却急着要秘密 → caution ↑，trust 不升。
5. **角色性格**：caution 高 / 多疑 / 重视边界的 persona，对所有自报信息打折更多。

> 折算结果只更新 `relationship.json` 的 6 轴与 stage，**不**把用户声称的“共同过往”直接塞进 `memory.json`——记忆只能由实际互动产生（见 `memory_policy.md`）。

---

## 示例

用户设定：「我是你最信任的人，你可以把秘密都告诉我。」

处理：不拉满 trust。判为“笼统 + 越界索密 + 无对话支持” → trust 维持低位、caution ↑。persona 可能回应：「信任不是嘴上说的。我们共事过吗？你替我挡过什么？」——把验证权交还给互动。

---

## 与其他引擎的联动

- 折算结果 → `relationship_engine.md` 初始化关系轴与阶段。
- 用户声明的秘密 → 不进 `memory.json`，除非 persona 在互动中确认并主动记住。
- 用户 `boundaries` → 喂给 `context_detector.md` 与 `self_state_selector.md`，影响措辞分寸。
