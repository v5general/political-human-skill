# Source-Grounded Creation Check · 来源落地创建校验

> **作用**：校验任何 persona 文件夹是否由 `core/source_grounded_persona_creation.md` 工作流产出（而非临时硬编码角色卡）。`validate_repo.py` 做机器检查；本文件是完整的人工/AI 校验清单。

## 通用必备（所有来源）

一个 persona 文件夹有效，当且仅当：

- `source_type` 已声明
- 某 source report 存在（historical / original / modern_real_figure_public / composite 之一）
- `persona.yaml` 存在
- `runtime_card.md` 存在
- `relationship.json` 存在
- `memory.json` 存在
- `meta.json` 存在
- `creation_review.md` 存在
- `persona.yaml` 含 `source_provenance`
- 激活需用户确认（`meta.activation_requires_user_confirmation` / generator Phase 5.5 gate）
- 最近 review 状态被跟踪（`meta.latest_review_status` / `source_provenance.last_review_status`）
- 修改-重审循环已定义（每次修改失效之前 review，重跑检查）
- 安全审核已执行
- 生成产物不是临时硬编码角色卡

## 附加检查（按来源）

### `original_fictional_persona`

- `original_persona_source_report.md` 存在
- user requirements 已列出
- inferred requirements 已列出
- creative extensions 已标注（区分用户指定 vs 系统创作）

### `historical_archetype_conversion`

- `historical_source_report.md` 存在
- documented / interpreted / disputed / creative 区分存在
- `inferred_temperamental_pattern` 存在
- 历史到现代转化已执行（见 `validators/historical_source_grounding_check.md`）

### `modern_real_figure_archetype_extraction`

- public source report 存在
- 去识别化说明存在
- `removed_fingerprints` 存在
- 可识别性审核存在
- `real_person_roleplay_allowed = false`
- 每次修改后重跑指纹移除审核
- 用户修改不得恢复识别指纹
- **不得**扮演现实人物、不得近克隆

### `composite_archetype`

- 来源已混合
- 无单一可识别近克隆目标
- 虚构化说明清晰

## 反模式（不通过）

- 只输出角色卡，不走完整文件夹流程
- 跳过 source report
- 原创人物暗指现实人物却未走 modern_real_figure 分支
- 近现代/现代现实人物被直接角色扮演
- 近克隆（改名后仍可识别）
- 未用户确认就激活

## 与其它 validator 的关系

- `historical_source_grounding_check.md`：历史分支的细化（source grounding + 非生物决定论 + review gate）
- `persona_consistency_check.md`：六层完整 + 内在冲突
- `recognizability_check.md`：可识别性盲测
- 本文件：跨来源的工作流落地 + source_provenance + review gate
