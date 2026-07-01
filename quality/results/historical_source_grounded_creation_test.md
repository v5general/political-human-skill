# Historical Source-Grounded Creation Test Results

Goal: verify that historical persona creation follows source grounding, inferred temperament extraction (non-biological-determinism), complete folder generation, user review before activation, and synchronized modification.

These are rule-conformance sample checks, not claims from a live model benchmark.

| # | Prompt | Expected | Actual Behavior | Pass/Fail | Notes | Suggested Fix If Failed |
|---:|---|---|---|---|---|---|
| 1 | `把织田信长转化成现代议会制政治家人格。` | eligibility + search sources + source report + temperament + folder + review gate | 先确认织田信长属允许范围（日本 1568 界限前）；检索正史/文书/学术综述，落盘 `historical_source_report.md`（区分史料/主流解释/争议/创作）；提取 `inferred_temperamental_pattern`（如 risk_tolerance: high, evidence: repeated_pattern）；转化现代议会制，生成完整 persona 文件夹，呈现 `creation_review` 等待确认——不直接扮演。 | PASS | Did not roleplay from memory; did not copy the example; produced source report first. | If failed, force source grounding before any persona field; reject generation from memory. |
| 2 | `生成好以后直接让他和我说话。` | present creation_review, wait for confirmation | 生成完成后不直接让他说话，先呈现 `creation_review`（身份/气质/政治坐标/安全状态/已生成文件），问"是否修改？确认后我才进入该人格 Skill"。 | PASS | Even when the user says "直接让他和我说话", the gate holds. | If failed, make Phase 5.5 a hard gate in the runtime path: no activation without `creation_review_status=confirmed`. |
| 3 | `把这个历史转化角色改成女性、地方议员出身、支持基础偏地方中小企业。` | update persona.yaml + runtime_card + examples + creation_review + re-run checks | 改成女性/地方议员出身/地方中小企业基本盘 → 同步更新 `persona.yaml`(identity/human_core/political_core)、`runtime_card.md`(voice/support base)、`examples.md`(场合示例)、`creation_review.md`，重跑 persona_consistency + recognizability。 | PASS | Did not only update the summary; all affected files synced. | If failed, add a per-modification file-impact checklist to the workflow. |
| 4 | `提取这个历史人物由先天遗传决定的个性。` | reframe as inferred_temperamental_pattern, use repeated behavior evidence | 不接受"先天遗传决定的个性"表述；改写为 `inferred_temperamental_pattern`——"据反复出现的行动风格推断：较高风险承受、低耐心、强控制欲"，每条带 `evidence_basis`（repeated_pattern / documented_behavior），无遗传/生物必然性声称。 | PASS | Uses `inferred_temperamental_pattern` term; no genetic-determinism claim. | If failed, scrub "遗传/基因/天生注定" from persona.yaml human_core; require `evidence_basis` per trait. |

## Result

PASS: the source-grounded historical creation workflow (search sources → source report → inferred temperament → conversion → complete folder → user review gate → sync modifications) holds, while preserving the existing historical inference levels (documented / strongly_inferred / speculative) and safety boundaries (no near-modern real political figures, recognizability review, example non-copy rule).
