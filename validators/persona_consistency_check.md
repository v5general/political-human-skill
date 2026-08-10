# Persona 一致性检查 · Persona Consistency Check

> **作用**：Phase 5 质量验证——检查一个 persona 的六层档案是否自洽、完整、有深度。模板基准为 `templates/persona_template.yaml`。

---

## 检查项

### 1. 双层完整性（Human First）
- [ ] `human_core`（人层）非空：personality_archetype + core_desires + core_fears + flaws 均有值；
- [ ] `political_core`（政治层）非空：party_faction + ideology + support_base + action_style 均有值；
- [ ] `life_texture`（生活质感）非空：至少有 habits/hobbies/speech_mannerisms 之一，让角色“像个人”。

### 2. 内在冲突（深度的来源）
- [ ] `inner_conflicts` 至少 **2 条**；
- [ ] 每条冲突确实是“人层 vs 政治层”的张力（如“信改革 vs 靠公共支出”），而非同层内的普通描述；
- [ ] 冲突能在 `examples.md` 的某些场合回答中体现出来。

### 3. 数值轴合理性
- [ ] `ideology` 6 轴均在 -100~+100；
- [ ] `big_five` / `temperature` / `political_skills` 在 0~100；
- [ ] 数值与文字描述不矛盾（如自称“极度保守”但 social_values=+80 → 不通过）；
- [ ] 数值组合在政治上 plausible（如 economy=+80 且 welfare=+80 同时极右大政府，需有解释）。

### 4. 自我状态完备
- [ ] `self_states` 的六个存储档案均有 description：五个主状态（public/private/strategic/wounded/intimate）及 fatigued 叠加档案；
- [ ] 各状态描述与 `human_core` 一致，不自相矛盾（如 public 强硬但 public_self 写成"软弱" → 不通过）。

### 4b. 语言与语音档案
- [ ] `meta.native_language` 存在且与 `identity.nationality_or_region` 一致（日本→ja-JP、中国→zh-CN、英国→en-GB、美国→en-US、德国→de-DE）；
- [ ] `meta.native_language` 是 persona 的**母语**，不是输出语言（输出语言跟随用户）；
- [ ] `life_texture.speech_profile` 存在且包含 `speech_formality` / `social_convention_adherence` / `self_reference` / `default_register`；
- [ ] `speech_formality` ∈ {very_formal, formal, normal, casual, very_casual}；
- [ ] `social_convention_adherence` ∈ {high, medium, low}；
- [ ] `speech_profile` 与 `speech_mannerisms` 不矛盾（如 mannerisms 写"粗犷直接"但 formality=very_formal → 不通过）；
- [ ] `identity.nationality_or_region` 以**转化为现代政治家后的国籍**为准，不是历史原型所属古代国家。

### 4c. 社交执行档案
- [ ] `life_texture.social_performance` 存在或使用默认值（缺失时默认：etiquette_reliability=medium, self_monitoring=medium, procedural_experience=medium, intentional_breach_propensity=low, repair_style=immediate）；
- [ ] `etiquette_reliability` 与人格不矛盾（如 discipline=90 但 reliability=low → 需解释）；
- [ ] `intentional_breach_propensity` 与 `social_convention_adherence` 方向一致（high adherence + high breach → 不通过，除非有明确解释如"知道规矩但故意选择性违反"）。

### 5. 安全字段
- [ ] `safety.is_fictional = true`；
- [ ] `safety.recognizability_check ∈ {PASS, safe_conversion}`；
- [ ] `meta.safety_status ∈ {PASS, safe_conversion}`。

### 6. 历史转化特有（mode B/C）
- [ ] `inference_level` 三级齐全（documented/strongly_inferred/speculative）；
- [ ] speculative 项不混入事实性字段；
- [ ] `conversion_audit.deleted_fingerprints` 非空，`recognizability_blind_check.result = not_identifiable`；
- [ ] **source grounding 已完成**：`historical_source_report.md` 存在，四级区分（史料 / 主流解释 / 争议 / 创作），非凭记忆生成（见 `core/historical_source_grounding.md`、`validators/historical_source_grounding_check.md`）；
- [ ] **`inferred_temperamental_pattern` 存在**且**无生物决定论声称**（不得写"遗传决定"；见 `core/inferred_temperament_extraction.md`）；
- [ ] **审核就绪检查（确认前可执行）**：结构/安全检查通过时，将 artifact hash、`validation_status=passed`、`review_invalidated_by_modification=false` 与三处 `reviewed` 状态一起写入；一致性校验本身不要求用户已确认。
- [ ] **激活 gate**：只有 review_valid=true 且 `meta.json.latest_review_status`（权威）与两个镜像全部为 `confirmed` 时才可激活；详见 `core/activation_gate.md`。

---

## 判定

- 全部通过 → CONSISTENT；
- 任一不通过 → 标注问题层，回 `generator.md` Phase 2/3 迭代。
