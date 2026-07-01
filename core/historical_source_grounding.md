# 历史资料落地 · Historical Source Grounding

> **作用**：模式 B/C 历史 persona 创建的**强制前置**——AI 必须先检索/浏览可靠资料、整理史实、区分史料 / 主流解释 / 争议 / 创作推断，才能进入人格提炼与转化。落地 `families/political_human/generator.md` Phase 1（mode B/C），是 `safety/historical_figure_policy.md` 史料纪律的**执行层**。
>
> **不可凭记忆、不可套用示例。** 与 `core/inferred_temperament_extraction.md` 配套使用。

## Global Application Rule

当用户请求基于一个**允许的历史人物 / 历史原型**创建 persona 时，系统**不得**直接凭训练记忆、也不得套用 `personas/examples/` 里的示例来生成 persona。

它必须先完成 source grounding（资料落地），否则不得进入人格提炼与转化。

## 与现有方法论的关系（extend，不 replace）

本规则**不取代**：

- `safety/historical_figure_policy.md` 的三级推断（documented / strongly_inferred / speculative）与六条史料纪律
- `safety/archetype_conversion_protocol.md` 的转化 10 步流程与可保留 / 必须删除清单
- 历史语境转译原则（先剥离时代、提炼性格底子、再放入现代社会重新推演立场）
- 可识别性审核、示例不可照搬规则、近现代现实政治人物安全边界

它**新增**的是：在这一切之前，先**主动检索 / 浏览资料**，产出结构化的 historical source report，作为后续提炼的事实底座。

## Source Grounding Workflow

1. **Eligibility check**：确认该人物在其地区近现代分界之前（见 `safety/modern_political_figure_policy.md` 第 4 节）。分界及以后 → 不进入本流程。
2. **Search / browse reliable sources**：主动检索可靠资料（不要只凭记忆）。优先 primary_source / academic_summary / encyclopedia / museum_or_archive / historical_database / reputable_secondary_source。排除信源黑名单（知乎、公众号、百度百科、内容农场、AI 生成的虚构传记）。区分史书 / 文学演义 / 后世评价。
3. **Summarize documented facts**：整理史料直接支持的事实（落盘 `references/research/`，沿用 `historical_figure_policy.md` 第 3 节的分轨建议）。
4. **Separate levels**：
   - documented（史料直接支持）
   - mainstream interpretation（主流史学解释）
   - disputed / uncertain（争议或证据弱）
   - later myth / literature / popular image（小说、演义、戏剧、宣传、后世想象）
   - creative inference boundary（可用于 persona 创作、但不得当史实）
5. **Produce `historical_source_report.md`**（用 `templates/historical_source_report_template.md`），写入 `personas/{slug}/`。
6. 完成后，才进入 `core/inferred_temperament_extraction.md`（气质提取）与 `safety/archetype_conversion_protocol.md`（转化）。

## Hard Rules

- **不得跳过资料落地**。即使 AI 训练数据里已有该人物，也必须检索核实，避免记忆偏差与脸谱化。
- **不得套用示例**。同名人物（织田信长 / 曹操 / 凯撒）须基于当前资料重新推算。
- **不得把文学演义当史实**。演义 / 小说可作"风格 / 气质"参考，不得进入事实性字段。
- **不得声称还原真实内心、不得编造私密丑闻**。
- **冷门 / 史料稀少人物**：降低推断密度、扩大 speculative 与诚实边界（见 `historical_figure_policy.md` 第 5 节），并在 source report 标注资料稀少。

## 输出与下游

source grounding 的产物是 `personas/{slug}/historical_source_report.md`，它喂给：

- `core/inferred_temperament_extraction.md`：从 documented / repeated 行为推断 `inferred_temperamental_pattern`
- `safety/archetype_conversion_protocol.md`：提炼人格结构 → 转化现代议会制

完成 source grounding 后，才进入 generator.md Phase 1.5（提炼质量检查点）。在用户确认 creation_review 之前，不得激活该 persona 进入扮演（见 `families/political_human/historical_persona_creation_workflow.md` 的 review-before-activation gate）。
