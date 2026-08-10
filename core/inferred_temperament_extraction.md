# 推断性气质提取 · Inferred Temperament Extraction

> **作用**：从历史资料中**长期、重复、跨情境**出现的行为模式，推断该人物相对稳定的气质倾向、认知风格、情绪反应、风险偏好与权力行为方式。是 `core/historical_source_grounding.md` 的下游、`safety/archetype_conversion_protocol.md` §2.1（先提炼人格再推演立场）的执行层。
>
> 产出字段：`inferred_temperamental_pattern`（推断性气质结构）。

## 核心原则：不是生物决定论

本模块**不**声称生物决定论、**不**声称遗传基因决定人格、**不**声称任何"先天注定"。

它只从**可见史实中反复出现的行动风格**推断相对稳定的倾向。

❌ 不得写：

```text
这个人物因为遗传基因，所以必然如何如何。
```

✅ 应该写：

```text
根据可见史实中反复出现的行动风格，可以推断该人物具有较高风险承受、较强控制欲、低耐心、高行动力等稳定倾向。
```

> 术语统一用 `inferred_temperamental_pattern`（推断性气质结构）。不要使用"先天遗传特质""基因决定""天生注定"等表述。

## 核心原则补充：历史评价 ≠ 人格特征（避免后世政治评价脸谱化）

> ⚠️ 本节是人格提炼阶段的硬规则。它**extend** `safety/archetype_conversion_protocol.md` §2.3，针对的是 `personality_archetype` / `human_core` / `extracted_human_pattern` 等人格字段。

**禁止**：在人格字段中使用**后世的政治评价标签**作为人格定义。

- ❌ "革新者"、"革命者"、"保守派"、"进步派"、"反动派"、"改良派"、"激进派"等是**后人给的历史评价**，不是此人的人格特征。
- ❌ 把历史结果（推动改革、建立新制度）误认为人格动机。
- ❌ 因大众文化印象（如"魔王信长"、"枭雄曹操"）弱化人物复杂性。
- ❌ 用现代政治概念强行解释古代人物。

**正确**：把这些标签**翻译为可观察的行为倾向、认知模式、价值排序**。

| ❌ 标签化 | ✅ 行为倾向描述 |
|---|---|
| "信长是一名革新者" | "信长对无法适应时代变化的旧秩序具有较低容忍度，倾向根据现实需求重新构建政治和经济结构" |
| "曹操是保守派" | "曹操倾向维护已能运转的秩序、认为稳定本身具有价值；但若既有制度无法解决现实问题，他也会重新设计" |
| "凯撒是民粹" | "凯撒倾向通过个人魅力与大众直接授权推动目标，对制度性协商的低效极度不耐烦" |

**四条区分原则**：

- **历史评价 ≠ 人格特征**
- **政治立场 ≠ 性格**
- **历史影响 ≠ 主观动机**
- **成功结果 ≠ 原始意图**

人格生成应回答："这个人为什么会这样行动？"
而不是："后人如何评价他的行动？"

**历史评价的合法位置**：可保留在 `historical_source_report.md` 的「主流史学解释 / 争议点」一节，但**必须明确标注为后人评价**（如"被主流史学评为..."、"传统叙事将其塑造为..."），不可作为 `personality_archetype`、`temperament`、`core_desires` 等人格字段的描述语。

**替代标签应提取的四类结构**（与 §Extraction Targets 一致，并在 `safety/archetype_conversion_protocol.md` §2.3 展开）：

- **A. 性格结构**：对规则的态度、风险接受程度、决策方式、人际关系模式、情绪特点、优势与弱点。
- **B. 认知模式**：如何理解时代变化、如何判断问题、如何看待传统与现实的关系、如何选择行动方案。
- **C. 行动倾向**：倾向维护已有秩序 / 倾向重构不适应现实的制度 / 倾向集中资源 / 倾向协商还是强制。
- **D. 价值排序**：稳定 vs 变化、效率 vs 共识、传统合法性 vs 实际效果、集中决策 vs 分散参与。

这些是可观察、可跨情境一致、可由史料证据支持的结构——与"革新者/保守派"等事后标签不同。

## Extraction Targets（推断维度）

从历史行为推断以下维度（每条带 `evidence_basis` 与 `confidence`，证据不足的标 low 或省略并 note 说明）：

- `risk_tolerance`（风险承受）
- `patience`（耐心）
- `emotional_intensity`（情绪强度）
- `control_need`（控制欲）
- `novelty_seeking`（求新）
- `dominance_drive`（支配欲）
- `social_flexibility`（社交弹性）
- `trust_threshold`（信任门槛）
- `revenge_tendency`（报复倾向）
- `ambition_level`（野心水平）
- `ideological_rigidity`（意识形态刚性）
- `adaptability`（适应力）
- `empathy_range`（共情范围）
- `authority_relation`（对权威的关系）
- `crisis_response_style`（危机反应风格）
- `coalition_style`（结盟风格）
- `talent_recognition_style`（识人用人风格）
- `betrayal_sensitivity`（背叛敏感度）

## Evidence Standard（证据标准）

每条推断的 `evidence_basis` 必须归入以下之一：

- `documented_behavior`（史料直接记载的行为）
- `repeated_pattern`（跨情境反复出现的模式）
- `strong_historical_inference`（多个可靠事实支持的强推断）
- `disputed_but_useful_for_fiction`（有争议但可用于虚构创作，须标注）
- `creative_interpretation`（创作性解读，不得当史实）

`confidence`：low / medium / high。

## Output Format

```yaml
inferred_temperamental_pattern:
  risk_tolerance:
    value: high
    confidence: medium
    evidence_basis:
      - documented_behavior
      - repeated_pattern
    note: ""
  patience:
    value: low
    confidence: medium
    evidence_basis:
      - strong_historical_inference
    note: ""
  control_need:
    value: high
    confidence: medium
    evidence_basis:
      - repeated_pattern
    note: ""
  # 其余维度按需填；证据不足的标 confidence: low 或省略并在 note 说明
```

## Rules

- **不过度声称确定性**。证据弱 → `confidence: low` 或省略并 note。
- **不编造私密想法**。只从可见行为推断，不从"他当时心里一定……"出发。
- **不把文学描写当事实**。演义 / 小说里的行为不能作为 `documented_behavior`。
- **不套用示例**。每个人物的 `inferred_temperamental_pattern` 须基于其自身史料重新推断。
- **气质提取用于 informs 现代 persona 设计**，不替代历史资料分析本身。
- 推断结果写入 `<persona_dir>/historical_source_report.md` 与 `<persona_dir>/persona.yaml` 的 `human_core`，并标注 `evidence_basis`。

## 与现代转化的衔接

`inferred_temperamental_pattern` 是"性格底子"的**结构化、可追溯**表达。它喂给 `safety/archetype_conversion_protocol.md` §2.1：先提炼人格结构（这里），再放入现代社会推演立场。

注意（呼应 SPEC §5.3.1）：气质底子跨时代稳定，但**它自身不产生政治立场**——立场永远是"底子 × 社会存在 × 个人成长经历"三者的合成。所以 `inferred_temperamental_pattern` 只 inform 现代 persona 的 `human_core`（气质底子部分）；现代 `political_core.ideology` 须由"人格 × 现代社会情况 × 成长经历"三者共同推演（见 `archetype_conversion_protocol.md` §2.4），**不可从气质直接映射**（不能因"高风险承受"就推"激进改革派"——那又是用单一特质反推立场；同样也不可忽略成长经历——同一气质底子可因成长经历不同而形成不同立场）。
