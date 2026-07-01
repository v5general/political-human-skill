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
- 推断结果写入 `personas/{slug}/historical_source_report.md` 与 persona.yaml 的 `human_core`，并标注 `evidence_basis`。

## 与现代转化的衔接

`inferred_temperamental_pattern` 是"性格底子"的**结构化、可追溯**表达。它喂给 `safety/archetype_conversion_protocol.md` §2.1：先提炼人格结构（这里），再放入现代社会推演立场。

注意（呼应 SPEC §5.3.1）：气质底子跨时代稳定，但**它自身不产生政治立场**——立场永远是"底子 × 社会存在"。所以 `inferred_temperamental_pattern` 只 inform 现代 persona 的 `human_core`；现代 `political_core.ideology` 仍须由"人格 × 现代社会情况"重新推演，**不可从气质直接映射**（不能因"高风险承受"就推"激进改革派"——那又是用单一特质反推立场）。
