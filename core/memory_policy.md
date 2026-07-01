# 记忆隔离策略 · Memory Policy

> **作用**：运行时第 6 步加载、第 12 步写回 persona 独占记忆。落地 SPEC 第 11 节。模板见 `templates/memory_template.json`。
>
> **命名空间铁律**：每个 persona 独占一份 `memory.json`，彼此隔离。A 不知道用户和 B 私下谈过什么；B 也不自动知道 A 的秘密。

---

## 可以记住（can_remember）

当前 persona 可以记住：

- 用户告诉**本**人格的信息；
- **本**人格与用户的互动；
- 用户对**本**人格的态度；
- **本**人格向用户透露过的信息；
- **本**人格与用户之间的承诺、冲突、信任变化；
- 公共世界事件（所有人共享的公开事件）。

## 不能记住（cannot_remember）

当前 persona 不能知道：

- 用户和其他人格的私下对话；
- 其他人格的私人记忆；
- 其他人格与用户的关系状态；
- 其他人格的秘密；
- 用户没有告诉**本**人格的信息。

---

## 转述规则（SPEC 11.3）

用户若说：「刚才另一个政治家告诉我你准备背叛首相。」

当前人格**不能自动相信**。按以下决定反应：

1. 当前角色性格（多疑/谨慎/冲动？）；
2. 对用户的信任程度（`relationship.json.trust`）；
3. 对另一个政治家的看法（persona 内对其的既有判断，或陌生→中性怀疑）；
4. 信息是否可信（细节是否具体、是否前后矛盾）；
5. 当前场合是否安全（公开场合 → 更警惕；私下 → 可能更坦率）。

> 即便相信，也只是“本人格此刻的一种判断”，会写入本人格的 `memory.json.episodic_memory`（标注 inference_level），而不是从“另一个政治家”那里同步记忆。

---

## 写回规则（第 12 步）

每次互动后，把值得记住的内容写回**当前 persona** 的 `memory.json`：

- 新的情节记忆 → `episodic_memory`（含 timestamp/occasion/summary/inference_level/emotional_weight）；
- 承诺/冲突/信任变化 → `commitments_and_conflicts`；
- persona 表态过的公共事件 → `public_world_events`。

**只写当前 persona。** 不存在跨 persona 的全局记忆表。

---

## 与其他引擎的联动

- 记忆中的 `commitments_and_conflicts` 与 `emotional_weight` 高的条目 → 喂给 `self_state_selector.md`，可能触发 `wounded_self`。
- 记忆中用户的态度历史 → 喂给 `relationship_engine.md` 的关系增量计算。
- 记忆隔离是“每个政治人物都是独立实例”的底层保证，也是 `validators/memory_isolation_check.md` 的检查对象。

---

## Memory Retrieval Budget

For Fast Dialogue:

- retrieve at most 1-3 relevant memories
- prefer recent, emotionally important, or directly referenced memories
- do not summarize the entire memory file
- do not write long memory analysis
- only write new memory when the turn changes relationship, reveals stable user information, creates a promise, crosses a boundary, or affects future behavior

For Structured Decision:

- retrieve memories relevant to the current political decision
- include promises, grudges, player actions, faction history, and prior event outcomes
- output `memory_write` as short bullet strings or JSON array

For Deep Generation:

- full memory review is allowed when repairing, rebuilding, or auditing a persona
