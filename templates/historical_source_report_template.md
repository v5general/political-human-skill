# Historical Source Report: <historical_figure_name>

> 模板用途：模式 B/C 历史 persona 创建时，`core/historical_source_grounding.md` 的产物。落盘到 `personas/<persona_id>/historical_source_report.md`。是后续 `inferred_temperamental_pattern` 提取与现代转化的**事实底座**。
>
> 填写纪律：区分史料 / 主流解释 / 争议 / 后世想象 / 创作边界；不把文学演义当史实；不声称还原真实内心。

## 1. Eligibility Check

- Figure:
- Region:
- Era:
- Historical boundary:   # 该地区近现代分界（中国 1840 / 日本 1868 / 欧洲 1789 / 其它见 SPEC §4.4）
- Allowed mode:          # historical_inference (B) | historical_archetype_conversion (C)
- Notes:

## 2. Sources Consulted

列出每条来源：title、URL 或引用说明、source type。

Source types:

- `primary_source`（正史 / 文书 / 信件 / 同时代记载）
- `academic_summary`（学术综述 / 论文）
- `encyclopedia`（权威百科）
- `museum_or_archive`（博物馆 / 档案）
- `historical_database`（历史数据库）
- `reputable_secondary_source`（可靠二手来源）
- `weak_or_popular_source`（弱来源 / 大众来源，仅作参考，须标注）

> 信源黑名单（永远排除）：知乎、微信公众号、百度百科、内容农场、AI 生成的虚构传记。

| # | Title | URL / Citation | Source Type | Confidence |
|---|---|---|---|---|
| 1 |  |  |  |  |

## 3. Documented Facts

史料直接支持的事实。每条尽量注明来源编号。

-

## 4. Mainstream Historical Interpretations

主流史学解释 / 被多个可靠来源支持的评价。保留共识，但注明这是"解释"而非"史实"。

-

## 5. Disputed or Uncertain Points

来源之间存在分歧、或证据薄弱之点。列出争议双方观点。

-

## 6. Later Myth / Literature / Popular Image

来自小说、演义、戏剧、宣传或后世大众想象的条目。**仅可作风格 / 气质参考，不得进入事实性字段。**

-

## 7. Creative Inference Boundary

明确：哪些可用于 persona 创作、哪些不得表述为史实。

- May use for persona:
- Must not state as fact:

## 8. Inferred Temperamental Pattern

来自 `core/inferred_temperament_extraction.md`。从上述 documented / repeated 行为推断（**非生物决定论**）。

```yaml
inferred_temperamental_pattern:
  risk_tolerance:
    value: ""
    confidence: low|medium|high
    evidence_basis: [documented_behavior | repeated_pattern | strong_historical_inference | disputed_but_useful_for_fiction | creative_interpretation]
    note: ""
  patience:
    value: ""
    confidence: ""
    evidence_basis: []
    note: ""
  control_need:
    value: ""
    confidence: ""
    evidence_basis: []
    note: ""
  # 其余维度（emotional_intensity / dominance_drive / trust_threshold / ambition_level /
  # crisis_response_style / coalition_style / talent_recognition_style / betrayal_sensitivity 等）
  # 按 core/inferred_temperament_extraction.md 的 Extraction Targets 填；证据不足标 low 或省略并 note。
```

## 9. Cold / Sparse-Source Note（若适用）

若该人物史料稀少，在此标注：哪些维度信息不足、扩大 speculative 与诚实边界的范围（见 `safety/historical_figure_policy.md` 第 5 节）。
