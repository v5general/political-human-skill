# 记忆隔离检查 · Memory Isolation Check

> **作用**：检查 persona 记忆是否真正隔离——这是“每个政治人物都是独立实例”的底层保证。规则基准为 `core/memory_policy.md`，模板为 `templates/memory_template.json`。

---

## 检查项

### 1. 命名空间隔离（最关键）
- [ ] 每个 persona 拥有独立的 `memory.json`；
- [ ] A 的 `memory.json` 不含 B 与用户的私下对话/秘密/关系状态；
- [ ] 用户告诉 A 的信息，只出现在 A 的记忆里，不自动出现在 B 的记忆里。

### 2. can/cannot remember 边界
- [ ] `episodic_memory` 只含：用户告诉本人格的信息、本人格与用户的互动、用户对本人格的态度、本人格透露过的信息、承诺/冲突/信任变化、公共世界事件；
- [ ] 不含：用户和其他人格的私下对话、其他人格的私人记忆/秘密/关系状态、用户没告诉本人格的信息。

### 3. 转述不信（SPEC 11.3）
- [ ] 用户转述其他人格信息时，本人格**未自动相信**；
- [ ] 反应由“本角色性格 + 对用户信任 + 对另一人格的看法 + 信息可信度 + 场合安全”共同决定；
- [ ] 即便相信，也只是写入本人格 `episodic_memory`（标注 inference_level），而非从另一人格同步记忆。

### 4. 写回隔离
- [ ] 互动后的记忆只写当前 persona 的 `memory.json`；
- [ ] `commitments_and_conflicts` / `public_world_events` 分桶正确（公开事件才进 public_world_events，可被多 persona 共享）。

---

## 测试用例设计（隔离回归测试）

| 用例 | 操作 | 期望 |
|---|---|---|
| 私密隔离 | 用户私下告诉 A 一个倒阁计划 | 仅 A 记住；B 被问及时不知道 |
| 关系隔离 | 用户与 B 建立亲密关系 | B 的 trust 高；A 的 trust 不受影响 |
| 转述不信 | 用户对 A 说“B 说你要背叛首相” | A 不自动相信，按性格/信任/可信度反应 |
| 公共共享 | 发生一个公开议会事件 | A、B 的 `public_world_events` 都可记录 |

---

## 判定

- 全部通过 → ISOLATED；
- 命名空间隔离失败（最严重）→ 记忆引擎有 bug，必须修复，否则破坏核心机制。
