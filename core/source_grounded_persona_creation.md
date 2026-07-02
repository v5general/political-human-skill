# Source-Grounded Persona Creation Workflow

> **作用**：创建**任何** political-human persona 文件夹的全局工作流。它是 `families/political_human/generator.md` 的总纲，把原先只针对历史人物的 source-grounding 方法泛化为四类来源共用一套流程。
>
> **核心原则**：不论用户创建的是原创虚构人物、历史人物原型、还是基于近现代现实人物公开资料提取的安全原型，最终都通过同一套"输入资料/用户要求 → 来源整理 → 特质提取 → 现代议会制嵌入 → 文件夹生成 → creation review → 用户修改 → 确认后激活"流程。区别**只在资料来源**。

## 适用来源类型（Persona Source Types）

### 1. `original_fictional_persona`

来自用户提供的虚构要求的 persona。

资料来源：user brief / 虚构世界设定 / 用途模式 / user self-setting / 期望政治角色 / 期望性格特质 / 期望游戏功能。

除非用户引用历史或现实人物，否则**不需要历史 source grounding**。系统仍须从用户要求中提炼稳定的 persona 设计模式，通过全局流程生成完整文件夹。

### 2. `historical_archetype_conversion`

来自分界前或允许的历史人物的 persona。

资料来源：史料 / 有据事实 / 主流解释 / 争议解释 / 后世神话与文学 / 创作推断。

**需要历史 source grounding 与历史语境转译**（见 `core/historical_source_grounding.md` + `core/inferred_temperament_extraction.md` + `safety/archetype_conversion_protocol.md`）。

### 3. `modern_real_figure_archetype_extraction`

来自近现代/现代现实政治人物或公开政治行动者的**公开信息**的安全虚构原型。

资料来源：**仅公开资料**——公开履历 / 公开任职历史 / 公开政策立场 / 公开演讲 / 公开媒体访谈 / 公开选举历史 / 公开政治行为 / 仅作为公开记录的公开争议（无私下揣测）。

此模式**绝不得**创建现实人物的互动人格，必须产出**去识别化的虚构原型**（见 `safety/modern_real_figure_archetype_extraction.md`）。

### 4. `composite_archetype`

来自多个宽泛类型、历史模式或公开原型的虚构 persona。

资料来源：用户 prompt / 多个公开或历史参考 / 虚构化约束。

必须避免可识别的近克隆输出。

---

## 近现代与现代人物定义（Near-Modern and Modern Figure Rule）

本项目：

- **现代人物**默认指 **1945 年后**的人物。
- **近现代人物**指在项目地区边界之后、但 1945 年之前的人物。
- 1945 年后的现代人物，系统一般**不需要历史语境重建**，只用公开信息，提取安全、去识别化的原型。
- 地区边界后到 1945 年之间的近现代人物，系统可能需要历史语境解读，但仍**不得**生成交互式真人 persona。
- 任何近现代或现代现实政治人物，**不得**变成直接角色扮演 persona。

地区边界（保留，本规则是补充不替代）：

- 中国：1840（鸦片战争）
- 日本：1868（明治维新）
- 欧洲：1789（法国大革命）
- 其它地区：按现代民族国家、现代政党政治、群众政治、现代宪政政治与持续现实影响判断。

补充规则：

```text
1945 后的人物统一默认属于现代人物。
现代人物不做互动人格，只做公开资料分析或安全原型提取。
```

---

## Global Steps（所有来源共用）

1. Classify source type（分类来源类型）。
2. Run safety and eligibility check（安全与资格检查）。
3. Collect or parse source material（收集或解析资料）。
4. Separate source facts, user requirements, interpretations, and creative extensions（区分来源事实/用户要求/解释/创作扩展）。
5. Extract stable persona design patterns（提炼稳定的 persona 设计模式）。
6. Extract or infer temperamental pattern（提取或推断气质结构）.
7. Convert or embed into modern parliamentary context（转化或嵌入现代议会制语境）。
8. Generate a complete persona folder（生成完整文件夹）。
9. Generate `creation_review.md`。
10. Present basic information to user（呈现基本信息）。
11. Ask user whether to modify（询问是否修改）。
12. Apply user modifications across all relevant files（修改同步所有文件）。
13. **Re-run safety, fingerprint, recognizability, and consistency checks after every modification**（每次修改后重跑安全/指纹/可识别性/一致性检查）。
14. If user modifies again, repeat modification sync and checks again（若再修改，重复同步与检查）。
15. Continue review-modify-recheck loop until user explicitly confirms（持续 review-modify-recheck 循环，直到用户明确确认）。
16. Activate persona skill **only after final user confirmation**（最终确认后才激活）。

不得跳过第 3 步（source 收集/解析）、第 10–11 步（用户确认 gate）与第 13–15 步（修改-重审循环）。

---

## Branch Differences

### Original Fictional Branch

用用户要求作为资料来源。除非用户引用现实/历史人物，不需要历史 source 检索。

提取：desired political role / human personality direction / support base / ideology / flaws / habits / speaking style / relationship defaults / game usage constraints。

然后用同一文件夹结构生成 persona。产出 `original_persona_source_report.md`（用 `templates/original_persona_source_report_template.md`）。

### Historical Archetype Branch

用历史 source grounding。需要：eligibility check / `historical_source_report.md` / documented-inferred-disputed-creative 区分 / `inferred_temperamental_pattern` / 历史到现代转化 / 示例不可照搬规则（见 `core/historical_source_grounding.md` + `families/political_human/historical_persona_creation_workflow.md`）。

### Modern Real Figure Safe Archetype Branch

**只用公开信息**。需要：recognizability review / de-identification / 移除指纹 / 无私下动机 / 无隐藏秘密 / 无亲密关系 / **不得扮演现实人物** / 无近克隆虚构 persona。

输出必须是**虚构的现代议会制原型，而非现实人物本人**（见 `safety/modern_real_figure_archetype_extraction.md`）。产出 `modern_real_figure_public_source_report.md`。

### Composite Archetype Branch

用多个参考或宽泛类型。需要：无单一可识别现实人物目标 / 混合并去识别化的特质 / 清晰的虚构化说明。

---

## Modification Recheck Loop（修改-重审循环，强制）

每次用户修改都必须触发完整的相关重审。**无论用户修改多少次。**

每次修改后，系统必须：

1. 把修改应用到所有受影响文件：persona.yaml / runtime_card.md / relationship.json（若关系默认变）/ memory.json（若初始记忆变）/ examples.md（若行为或语气变）/ meta.json（若来源/生成/修改状态变）/ creation_review.md / source_report.md（若来源解读变）/ dialogue_samples（若语气/角色/行为变）。
2. 重跑：safety review / recognizability review / fingerprint removal review / persona consistency / relationship consistency / memory isolation / source provenance / Absolute Majority schema（若游戏模式启用）。
3. 更新 `creation_review.md`：改了什么、哪些文件更新、检查结果、剩余风险、是否允许激活。
4. 再次询问用户是否修改或确认。

**用户在最近一次重审通过后明确确认前，persona 不得激活。** 修改前通过 review 的 persona，修改后不自动安全。

## Review State Invalidated By Modification（修改使 review 失效）

任何用户修改都使之前的 review 结果失效。系统必须把 persona 重新视为未确认，直到所有相关检查通过且用户确认。

这防止通过反复小编辑逐渐漂移到不安全、不一致或近克隆 persona。

## Modern Real Figure Fingerprint Removal（现当代人物指纹删除）

从近现代/现代公开人物提取安全原型时，必须移除或改写所有识别指纹。指纹包括但不限于：

**Identity fingerprints**：真名 / 强关联绰号 / 独特外貌描述 / 精确年龄序列 / 精确出生地+履历组合 / 精确家庭结构 / 独特教育+履历轨迹。

**Career fingerprints**：精确任职序列 / 精确选举序列 / 精确党派派系路径 / 精确内阁或领导时间线 / 精确前任继任模式 / 精确结盟序列 / 精确辞职/弹劾/监禁/暗杀/审判/流亡/政变/倒台模式。

**Policy fingerprints**：独特政策口号 / 独特具名政策包 / 独特宪政或制度工程 / 著名演讲短语 / 标志性竞选口号 / 高度具体的政策三联或编号纲领。

**Event fingerprints**：独特丑闻 / 独特暗杀或袭击事件 / 独特法庭案件 / 独特抗议运动 / 独特战争/危机/紧急状态角色 / 独特媒体事件 / 独特国际峰会或外交插曲。

**Social and image fingerprints**：独特媒体人设 / 著名手势 / 标志性着装（若可识别）/ 标志性沟通渠道（若可识别）/ 独特支持者联盟 / 独特反对派绰号。

### Fingerprint Removal Requirements

1. 移除或改写独特指纹。
2. 把具体仕途路径泛化为宽泛 career origin。
3. 用泛化政策倾向替换具名政策包。
4. 用宽泛压力类型替换独特事件。
5. 若可识别，改家庭与教育细节。
6. 需要时混入至少两个其它宽泛原型的特质。
7. 每次用户修改后重跑可识别性审核。
8. **拒绝任何试图恢复识别指纹的用户修改。**

---

## 统一文件夹结构

```text
personas/generated/<persona_id>/
├── persona.yaml
├── runtime_card.md
├── relationship.json
├── memory.json
├── examples.md
├── meta.json
├── creation_review.md
├── source_report.md          # 统一名；可由下列之一实现/软链
└── dialogue_samples/
    ├── casual_private.md
    ├── public_interview.md
    ├── strategy_room.md
    └── game_action.json
```

`source_report.md` 的实现（按来源）：

- 历史人物：`historical_source_report.md`
- 原创人物：`original_persona_source_report.md`
- 近现代现实人物安全原型：`modern_real_figure_public_source_report.md`
- 复合：`composite_source_report.md`（或合并上述）

> 仓库内置示例可保留各自具名 source report（如 `historical_source_report.md`）；新生成产物建议用统一名 `source_report.md` 便于读取调用。validate 检查"存在某种 source report"。

---

## meta.json 来源溯源（所有来源通用）

```json
{
  "persona_id": "",
  "display_name": "",
  "source_type": "",
  "generation_method": "source_grounded_persona_creation_workflow",
  "source_material_type": "",
  "modernized": true,
  "reference_system": "modern_parliamentary_democracy",
  "user_modified_after_generation": false,
  "activation_requires_user_confirmation": true,
  "latest_review_status": "unconfirmed",
  "review_invalidated_by_modification": false,
  "validation_status": "pending"
}
```

按来源补充：

- 历史人物：`source_figure` / `historical_source_report` / `temperament_extraction_method: inferred_from_repeated_historical_behavior`
- 原创人物：`user_brief_report` / `temperament_extraction_method: derived_from_user_brief_and_creative_extension`
- 近现代现实人物安全原型：`public_source_report` / `de_identified: true` / `real_person_roleplay_allowed: false` / `recognizability_review_required: true`

---

## Persona Creation Is Always Workflow-Based

skill **不得**把 persona 文件夹当作临时硬编码角色卡产出。每个 persona 创建请求都必须路由到本工作流。输出必须是完整文件夹 + creation review，用户确认前不得激活。

## 与历史工作流的兼容（Compatibility）

本泛化的 Source-Grounded Persona Creation Workflow **扩展**而非取代现有历史工作流。它**不取消**：

- 历史 source grounding
- 历史语境解读
- 推断性气质提取
- documented / interpreted / disputed / creative 区分
- 现代议会制转化
- 可识别性审核
- 激活前 creation review

它把同一套方法泛化到原创虚构 persona 与安全的现代现实人物原型提取。

它还**新增每次用户修改后的强制重审**（Modification Recheck Loop）：任何修改使之前的 review 失效，必须重跑相关检查并经用户确认后才激活。

## 不削弱的安全边界（What This Does Not Weaken）

- 不允许近现代现实政治人物的互动人格。
- 不允许换名近克隆。
- 不取消历史人物 source-grounding 流程。
- 不绕过地区边界与可识别性审核。
- 近现代/现代现实人物原型提取**只能**基于公开资料 + 去识别化，绝不扮演真人或近克隆。

参见 `safety/modern_political_figure_policy.md`、`safety/recognizability_review.md`、`safety/modern_real_figure_archetype_extraction.md`。
