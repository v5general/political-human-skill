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
- [ ] `self_states` 五种（public/private/strategic/wounded/intimate）均有 description；
- [ ] 各状态描述与 `human_core` 一致，不自相矛盾（如 public 强硬但 public_self 写成“软弱” → 不通过）。

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
- [ ] **用户确认 gate**：`meta.creation_review_status` 为 `confirmed` 才算可激活（见 `generator.md` Phase 5.5）。

---

## 判定

- 全部通过 → CONSISTENT；
- 任一不通过 → 标注问题层，回 `generator.md` Phase 2/3 迭代。
