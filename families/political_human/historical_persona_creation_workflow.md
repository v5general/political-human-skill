# 历史 persona 创建工作流 · Historical Persona Creation Workflow

> **作用**：模式 B/C 历史 persona 创建的**端到端强制工作流**。它是 `families/political_human/generator.md` 历史分支的展开，串联 source grounding → temperament extraction → 转化 → 文件夹生成 → **用户确认 gate** → 激活。
>
> **核心约束**：不得跳过资料落地；不得套用示例；**用户确认前不得进入人格扮演**。

## 适用触发

用户请求基于一个允许的历史人物 / 历史原型创建 persona（"把 X 转成现代政治家""做一个曹操式的议员"等），且该人物通过 eligibility check（地区近现代分界之前）。

## 13 步强制工作流

1. **Check historical eligibility and safety boundary** — 确认在地区近现代分界之前（`safety/modern_political_figure_policy.md` 第 4 节）；近现代 / 被禁 → 拒绝互动人格，提供安全虚构原型转化。
2. **Search or browse reliable sources** — 主动检索资料，不凭记忆（`core/historical_source_grounding.md`）。
3. **Summarize historical facts** — 整理史料事实。
4. **Separate documented facts, mainstream interpretations, disputed interpretations, creative inferences** — 四级区分。
5. **Extract stable behavioral patterns** — 提炼稳定行为模式。
6. **Infer temperamental patterns from repeated cross-context behavior** — 推断 `inferred_temperamental_pattern`（`core/inferred_temperament_extraction.md`），非生物决定论。
7. **Convert the historical archetype into a modern parliamentary fictional politician** — 历史语境转译转化（`safety/archetype_conversion_protocol.md`，SPEC §5.3.1）。
8. **Generate a complete persona folder** — 与 `personas/examples/<persona_id>/` 同构。
9. **Present a concise basic information summary to the user** — 用 `templates/persona_creation_review_template.md` 呈现 creation_review。
10. **Ask the user whether they want to modify the persona** — 等待用户确认 / 修改。
11. **Apply user modifications across all relevant persona files** — 修改同步所有文件。
12. **Re-run safety and consistency checks** — 修改后重跑 validator。
13. **Only after user confirmation, enter active persona skill mode** — 确认后才激活。

**不得跳过第 2 步（source grounding）与第 9–10 步（用户确认 gate）。**

## 完整 persona 文件夹结构

```text
personas/generated/<persona_id>/
├── persona.yaml
├── runtime_card.md
├── relationship.json
├── memory.json
├── examples.md
├── meta.json
├── historical_source_report.md      # 第 2–4 步产物
├── creation_review.md               # 第 9 步产物（用户确认 gate）
└── dialogue_samples/
    ├── casual_private.md
    ├── public_interview.md
    ├── strategy_room.md
    └── game_action.json
```

> `personas/generated/` 是本地生成的建议输出位置。是否提交由项目配置决定（可在 `.gitignore` 忽略）。仓库内置示例仍在 `personas/examples/`，**不得**作为生成产物的固定模板。

## Creation Review Before Activation（强制 gate）

生成 persona 文件夹后，系统**不得**立即进入角色扮演。它必须先用 `templates/persona_creation_review_template.md` 呈现基本信息摘要，并询问用户是否修改。

摘要须含：persona_id / display_name / 源历史人物 / source grounding 状态 / 现代议会角色 / career origin / public image / 核心气质 / main desire / main fear / main flaw / ideology summary / support base / action style / relationship default / safety notes / files generated。

然后问：

> 是否要修改这个人格？可以修改姓名、年龄、性别、职业路径、意识形态、支持基础、性格强度、弱点、爱好、说话风格、与用户初始关系、是否用于《绝对多数》等。确认无误后，我再进入该人格 Skill。

**只有用户确认后，才激活该 persona skill。** 在此之前，即使用户说"直接让他和我说话"，也必须先呈现 creation_review 并等待确认。

## User Modification Sync（修改同步）

用户修改时，必须**同步更新所有受影响的 persona 文件**，不得只改摘要：

- `persona.yaml`（identity / human_core / political_core / self_states / inner_conflicts）
- `runtime_card.md`（voice / conversational style / self-state shortcuts 等）
- `relationship.json`（若涉及初始关系）
- `examples.md`（若涉及场合示例）
- `creation_review.md`（摘要本身）
- `meta.json`（若涉及 source_type / integration_target）

修改后**重跑** `validators/`（persona_consistency / recognizability / historical_source_grounding_check 等）与 `safety/modification_review.md`（每次修改必审）。

## Compatibility With Existing Methodology（extend，不 replace）

本工作流**扩展**而非取代现有历史转化方法论。它**不取消**：

- 历史推断三级（documented / strongly_inferred / speculative）
- 现代议会制转化与历史语境转译原则
- 可识别性审核
- 示例不可照搬规则
- 近现代现实政治人物安全边界

它**新增**：

- 创建前主动检索资料（source grounding）
- historical source report
- inferred temperamental pattern extraction（非生物决定论）
- 完整 persona 文件夹生成
- 用户确认前不激活（review-before-activation gate）
- 修改跨文件同步
