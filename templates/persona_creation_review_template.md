# Persona Creation Review: <persona_name>

> 模板用途：模式 B/C 历史 persona 创建工作流第 9 步的产物（`families/political_human/historical_persona_creation_workflow.md`）。落盘到 `personas/<persona_id>/creation_review.md`，并**呈现给用户确认**。用户确认前不得激活该 persona。

## Basic Information

- Persona ID:
- Display Name:
- Source Historical Figure:   # 仅历史来源填
- Source Type:        # original_fictional_persona | historical_archetype_conversion | modern_real_figure_archetype_extraction | composite_archetype
- Modernized:         # yes | no
- Political System:
- Reference Model:

## Source Type & Source Report

- Source Type:
- Source Report:      # historical_source_report.md | original_persona_source_report.md | modern_real_figure_public_source_report.md | composite_source_report.md

## Safety and Fictionalization

For modern real figure archetype extraction, state clearly:
- this is not the real person
- no roleplay as real person
- identifying fingerprints removed
- recognizability review completed
- `de_identified: true` / `real_person_roleplay_allowed: false`

## Modification Review Log

每次用户修改记录：

- modification id:
- user request:
- files updated:
- safety review:
- recognizability review:
- fingerprint review:
- consistency review:
- action:
  - accepted
  - rewritten
  - refused
- activation allowed:
- notes:

## Current Activation Status

- latest_review_status:    # unconfirmed | reviewed | confirmed
- activation_allowed:
- pending_user_confirmation:

## Source Grounding

- Sources consulted:
- Documented fact coverage:
- Disputed points:
- Creative inference level:

## Inferred Temperament

（来自 `core/inferred_temperament_extraction.md`，非生物决定论）

- Risk tolerance:
- Patience:
- Control need:
- Trust threshold:
- Ambition:
- Crisis response:
- Betrayal sensitivity:

## Modern Persona

- Age:
- Gender:
- Career origin:
- Current role:
- Public image:
- Support base:
- Ideology summary:
- Political skills:
- Action style:

## Human Layer

- Core desire:
- Core fear:
- Main flaw:
- Habits:
- Hobbies:
- Speech style:

## Relationship Defaults

- Familiarity:
- Trust:
- Affection:
- Respect:
- Caution:
- Dependency:

## Safety Notes

- Modern political figure risk:
- Recognizability risk:
- Fictionalization notes:

## Generated Files

- persona.yaml
- runtime_card.md
- relationship.json
- memory.json
- examples.md
- meta.json
- historical_source_report.md
- creation_review.md

## User Review Question

是否要修改这个人格？
可以修改姓名、年龄、性别、职业路径、意识形态、支持基础、性格强度、弱点、爱好、说话风格、与用户初始关系、是否用于《绝对多数》等。

**确认无误后，才进入人格 Skill。** 在此之前系统不会进入角色扮演。
