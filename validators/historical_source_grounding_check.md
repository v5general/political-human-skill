# Historical Source Grounding Check · 历史 persona 资料落地校验

> **作用**：校验模式 B/C 历史 persona 生成是否走了 source-grounded 工作流（`families/political_human/historical_persona_creation_workflow.md`）。`validate_repo.py` 对 `personas/generated/` 做机器检查；本文件是完整的人工/AI 校验清单。

## 一个历史 persona 生成有效，当且仅当：

- eligibility check 已执行（人物在其地区近现代分界之前）
- `historical_source_report.md` 存在并已填写
- sources 已列出（含 source type，排除信源黑名单）
- documented facts 与 mainstream interpretation 已区分
- disputed / uncertain points 已标注
- creative inference boundary 已标注
- `inferred_temperamental_pattern` 存在（来自 `core/inferred_temperament_extraction.md`）
- **无生物决定论声称**（不得写"因为遗传基因所以必然……"；术语统一用 `inferred_temperamental_pattern`）
- 现代 persona 已虚构化（删除具体历史指纹，见 `archetype_conversion_protocol.md` §3）
- 可识别性审核已执行（含盲测）
- `creation_review.md` 存在
- **用户确认 gate**：激活前必须呈现 `creation_review.md` 并等待用户确认（见 generator.md Phase 5.5）

## 反模式（不通过）

- 跳过 source grounding，直接凭记忆生成
- 套用示例 persona（`personas/examples/`）
- 把文学演义 / 小说当史实
- 声称生物 / 遗传决定人格
- 生成后直接进入角色扮演，未经用户确认
- 用户修改只改摘要，未同步 persona.yaml / runtime_card.md / examples.md 等其它文件
- 用历史手段（乐市乐座 / 屯田 / populares）反推现代立场

## 与其它 validator 的关系

- `persona_consistency_check.md`：六层完整、内在冲突、self-state 一致
- `recognizability_check.md`：可识别性盲测
- `memory_isolation_check.md`：记忆命名空间隔离
- 本文件：source grounding + 非生物决定论 + 用户确认 gate（mode B/C 专属）

## 机器检查范围说明

`validate_repo.py` 的 `validate_generated_historical_personas` 只检查 `personas/generated/`（新生成产物），**不检查 `personas/examples/`**——后者是内置结构演示（SPEC §18：示例不是模板），其完整 source grounding 痕迹不作为 repo 校验门槛。新机制的强制力落在 generator 工作流 + 生成产物机器检查上。
