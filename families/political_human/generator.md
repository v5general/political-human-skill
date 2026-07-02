# Generator · 创建一个 political_human persona

> **作用**：创建新 persona 的生成器协议。它是 `SKILL.md` 第 5 节（Phase 0→5）在 family 层的操作手册。参考 colleague-skill 的 intake → 分析 → 生成预览 → 写入 流程。
>
> **前置**：本 family 的定义与安全契约见 `family.md`。

---

## 触发

用户表达创建意图：「造一个政治人物 / 做个议员 / 把 X 转成现代政治家 / 给《绝对多数》设计一个 NPC」等。

---

## No Hardcoded Persona Rule（总则）

persona 文件夹**不得**作为手工写死的完美样例产出。除用户在生成后明确修改的内容外，所有 persona 文件都必须由本生成器的工作流产出：

请求分类 → 安全/资格检查 →（历史则 source grounding）→ 史料/解释/争议区分 → 推断气质提取 → 现代议会制转化 → persona 文件生成 → runtime card 生成 → 关系/记忆初始化 → creation review → 用户修改同步 → 校验。

示例可以被打磨和校准，但必须**能由同一套工作流复现**。不得为单个示例编码“全局规则不支持、只有它才生效”的特殊行为（见 SPEC §18 No Hardcoded Persona Rule / Example Reproducibility Rule）。

---

## Source-Grounded Workflow（全局，所有来源）

所有 persona 创建都走 `core/source_grounded_persona_creation.md` 的全局流程（输入资料 → 来源整理 → 特质提取 → 现代议会制嵌入 → 文件夹生成 → creation review → 用户修改 → 确认后激活）。区别**只在资料来源**。

### Source Type Classifier

判定请求属于以下之一：

- `original_fictional_persona`（原创虚构）
- `historical_archetype_conversion`（历史原型转化）
- `modern_real_figure_archetype_extraction`（近现代/现代现实人物公开资料 → 安全原型）
- `composite_archetype`（复合原型）
- `unsafe_real_persona_request`（不安全：直接扮演/近克隆现实人物 → 拒绝，提供安全原型提取）

### Branch Routing

- **original_fictional_persona**：用户 brief 作资料，产 `original_persona_source_report.md`，生成完整文件夹。
- **historical_archetype_conversion**：历史 source grounding，产 `historical_source_report.md`，见 `families/political_human/historical_persona_creation_workflow.md`。
- **modern_real_figure_archetype_extraction**：**只用公开信息**，去识别化，可识别性审核，产 `modern_real_figure_public_source_report.md`，见 `safety/modern_real_figure_archetype_extraction.md`。**绝不扮演现实人物 / 近克隆**。
- **composite_archetype**：多来源安全混合，避免可识别，产完整文件夹。
- **unsafe_real_persona_request**：拒绝直接 persona 创建，提供安全虚构原型提取（走 modern_real_figure 分支）。

> 近现代/现代现实人物（1945 后默认现代；地区边界后到 1945 近现代）：不做互动人格，只做公开资料分析或安全原型提取。地区边界（中国 1840 / 日本 1868 / 欧洲 1789）保留。

### Modification Loop（修改-重审循环，强制）

每次用户修改后：

1. 更新所有受影响文件（persona.yaml / runtime_card.md / relationship.json / memory.json / examples.md / meta.json / creation_review.md / source_report.md / dialogue_samples）。
2. 标记之前的 review 为失效（`latest_review_status = unconfirmed`）。
3. 重跑相关安全 / 可识别性 / 指纹 / 一致性 / schema 检查。
4. 更新 `creation_review.md` 与 source report 的修改审查日志。
5. 再次询问用户修改或确认。
6. 用户在最近一次成功 review 后确认前，不得激活。

详见 `core/source_grounded_persona_creation.md` 的 Modification Recheck Loop。

---

## Phase 0：入口分流 + 安全初筛

1. 判定生成模式（A 原创 / B 历史推演 / C 历史转原型），或“分析近现代现实人物”/“疑似不安全近克隆”。
2. **立即安全初筛**（`core/safety_boundaries.md` + `safety/modern_political_figure_policy.md`）：指向近现代现实人物（含换皮/拼接）→ 不进入生成，走 `safety/recognizability_review.md`。
3. 记录 `integration_target`（standalone / absolute_majority）。

---

## Phase 0.5：创建 persona 目录

```text
personas/{slug}/
├── persona.yaml  runtime_card.md  relationship.json  memory.json
├── SKILL.md  examples.md  meta.json
├── historical_source_report.md  creation_review.md   # 仅 mode B/C（source grounding + 用户确认 gate）
└── references/{research/, sources/}   # 仅 mode B/C
```

`slug` 规则：原创 `original_<主题>` 或自定；历史转化 `<人物拼音/罗马名>_modernized`。

---

## Phase 1：资料采集与原型提炼

- **mode A**：以用户描述为主，必要时补宽泛政治类型画像。
- **mode B/C**：**必须先 source grounding**——主动检索/浏览可靠资料（不得只凭记忆、不得套用示例），产 `historical_source_report.md`（用 `templates/historical_source_report_template.md`），四级区分（史料事实 / 主流解释 / 争议 / 创作推断）；遵守 `core/historical_source_grounding.md` 与 `safety/historical_figure_policy.md` 六条史料纪律 + 三级推断；信源黑名单（知乎 / 公众号 / 百度百科 / 内容农场）。再按 `core/inferred_temperament_extraction.md` 推断 `inferred_temperamental_pattern`（非生物决定论）。完整端到端流程见 `families/political_human/historical_persona_creation_workflow.md`。
- **mode C 历史语境转译**：不得直接套用历史人物原时代的政治立场。**记住逻辑**：立场 = 天生的性格底子（跨时代稳定的脾气、欲望、恐惧、反应方式）× 被社会训练出来的判断力（出身、阶层、制度环境塑造他怎么看世界——即社会存在塑造意识）。先理解其原时代主要矛盾、看清当时的社会怎么造就了他的立场；再剥离不可迁移的时代条件，提炼性格底子；最后把性格底子放进现代议会制社会，让它重新判断、推出新立场。现代社会也可能慢慢重塑性格底子，人物在现代的行动也会反作用于社会——人和时代互相塑造。

> 同名历史人物任务**不得套用示例**，须基于当前资料重新推算（见 `safety/historical_figure_policy.md` 第 6 节）。

---

## Phase 1.5：提炼质量检查点

向用户展示结构化摘要（历史时代主要矛盾/不可迁移时代条件/稳定人格结构/欲望弱点/行为模式/危机反应/现代社会情况与政治约束/三级推断占比/待删指纹），确认后继续。冷门人物降低推断密度、扩大诚实边界。

---

## Phase 2：安全与可识别性审核（强制）

跑 `safety/recognizability_review.md` 全流程（指纹扫描 → 不通过则提炼 → 删除指纹 → 转化 → 再扫）。mode C 额外核对 `safety/archetype_conversion_protocol.md` 的必须删除清单。

结果：`PASS` 或 `safe_conversion`。`real_figure_clone` 不允许存在。

---

## Phase 3：persona 构建（六层）

读取 `templates/persona_template.yaml`（mode A/C）或叠加 `templates/historical_archetype_conversion.yaml`（mode B/C），按层填入：

1. 身份层 identity
2. 人性核心层 human_core（先填）
3. 生活质感层 life_texture（含新增：`fatigue_signals`、`mundane_anchors`、`vulnerability_style`——从 persona 人格结构推断其疲惫表现、日常锚点和脆弱回收风格）
4. 政治职业层 political_core
5. 自我状态层 self_states（含新增：`fatigued_self`——政治疲惫/职业倦怠时的状态，与 wounded_self 的创伤触发区分）
6. 内在冲突层 inner_conflicts（至少 2 条，人层 vs 政治层张力；新增 `human_vs_political` 维度：个人情感与政治计算之间的实时拉扯）

> Human First：先人层后政治层，最后写冲突。

> Mode C 额外规则：`political_core.ideology` 必须由”稳定人格结构 × 现代社会情况/制度条件/政治约束”推演而来。不要把历史立场、历史敌友、古代制度选择或时代口号直接映射成现代左右翼标签。

### dialogue_samples 生成（Phase 3 子步骤，在 persona 构建完成后）

在 Phase 3.5 预览确认之前，必须先生成 `dialogue_samples/` 目录下的 6 个对话文件（casual_private / public_interview / strategy_room / confrontation / trust_low / trust_high）和 README.md。每个样本必须遵守：
- `core/human_fragility.md` 的人性元素要求（身体状态、日常锚点、非功能性话语、脆弱展示与回收）
- `core/no_constant_testing.md` 的测试频率限制
- `core/anti_manifesto_dialogue.md` 的具体优先规则
- Phase 3.6 的多样性检查将在生成后立即执行

---

## Phase 3.5：构建预览确认

向用户展示 5–8 行摘要（身份/人性底色/政治坐标/内在冲突/自我状态/输出模式/安全状态），确认后写入。

---

## Phase 3.6：对话多样性检查（防模式收敛，强制）

**在写入 dialogue_samples 之前执行**。本阶段防止不同 persona 产出结构雷同的对话——这不是 example 编辑能解决的问题，是生成机制必须内置的硬性检查。

### 3.6a：跨 Persona 去重

如果 repo 中已有其他 persona 的 `dialogue_samples/`，扫描以下维度：

1. **Verbatim 共享行**：新生成的 dialogue_samples 中不得出现与已有 persona 完全相同的句子（连续 8 个汉字/单词以上匹配即标记，回退重写）。
2. **结构弧线雷同**：同一场景类型（如 trust_low）在不同 persona 间必须使用不同的对话弧线——不能两个人都用 "No." → 反问 → "I trust that you are useful, sometimes." 的结构。
3. **结尾公式雷同**：不得出现相同的结尾修辞模式（如 "If compromise means a number, yes. If it means a speech, no." 的变体不能跨 persona 共享）。

### 3.6b：Persona 内多样性

新生成的 persona 的 dialogue_samples 必须满足：

1. **场景差异化**：同一议题在不同 self-state 下的回答必须有明显差异（不只是语气微调）。
2. **信任分层**：trust_low 和 trust_high 的对话必须有质的区别（不只是信息量不同，对话弧线和情感深度必须不同）。
3. **开场策略不重复**：同一 persona 的不同 dialogue_samples 不得使用相同的开场修辞策略。

### 3.6c：人性元素覆盖率

每个 persona 的 dialogue_samples 集合（6 个文件）必须至少包含：

| 元素 | 最少出现次数 |
|---|---|
| 身体状态/疲惫展示 | ≥1 |
| 日常锚点（具体物品/食物/习惯） | ≥1 |
| 非功能性话语（"嗯""算了""让我想想"） | ≥1 |
| 脆弱展示（层级与信任度匹配） | ≥1 |
| 脆弱回收动作（自嘲/沉默/回避） | ≥1 |
| 自嘲或非政治性幽默 | ≥1 |

### 3.6d：不通过处理

任一检查不通过 → 回到 Phase 3 的 dialogue_samples 生成部分重写，直到通过。不得以"这是示例"为由跳过。

> **设计理由**：三个示例 persona（曹操/凯撒/信长）的初版 dialogue_samples 存在严重结构性雷同——verbatim 共享行、相同结尾公式、相同场景弧线。这不是 example 编辑层次的问题，是生成器没有内置多样性检查。本 Phase 确保新生成的 persona 不会重复这个模式。

---

## Phase 4：写入 persona 文件

写入 `personas/{slug}/` 全部文件：

- `persona.yaml`：六层档案。
- `runtime_card.md`：从 `persona.yaml`、初始关系风格、核心记忆策略中自动压缩生成的普通对话快取。必须使用 `templates/runtime_card_template.md`，并为该人物填入 voice、dialogue rhythm、self-state shortcuts、One-Pass Hints、Anti-Manifesto Hints、**Testing Behavior**、**Fatigue & Vulnerability Hints**、**Human Moment Hints**、**Mundane Anchors**。它负责保留个人特色；全局 `core/runtime_protocol.md`、`core/one_pass_dialogue.md`、`core/anti_manifesto_dialogue.md`、`core/conversational_realism.md`、`core/no_constant_testing.md`、`core/human_fragility.md` 仍负责底层规则。
- `relationship.json`：用 `templates/relationship_template.json` 初始化（stranger / caution=50）。
- `memory.json`：用 `templates/memory_template.json` 初始化（空记忆 + 隔离字段）。
- `SKILL.md`：内嵌运行时协议（`core/runtime_protocol.md`）+ 指向 `runtime_card.md` 的快速读取说明 + 角色卡 + 自我状态 + 风格 + 诚实边界，使该 persona 可被宿主直接激活运行。
- `examples.md`：公开/私下/辩论/危机/亲密 五种场合各一例。
- `dialogue_samples/`：README + casual_private / public_interview / strategy_room / confrontation / trust_low / trust_high / game_action（共 7-8 个文件，在 Phase 3 生成、Phase 3.6 检查通过后写入）。
- `meta.json`：`source_type / mode / integration_target / safety_status / version / created_at / language`。
- `historical_source_report.md`（仅 mode B/C）：source grounding 产物（Phase 1，用 `templates/historical_source_report_template.md`）。
- `creation_review.md`（仅 mode B/C）：用户确认 gate 摘要（Phase 5.5，用 `templates/persona_creation_review_template.md`）。

### Runtime card generation rule

Every generated persona must receive its own `runtime_card.md`.

The runtime card is not a copy of global rules. It is the persona-specific compression layer:

- what this persona sounds like in one or two turns
- what concrete political objects this persona naturally notices
- how this persona handles beginners, vague requests, irritation, trust, and guardedness
- what words or abstractions this persona should avoid overusing in ordinary dialogue
- when this persona is allowed to become grand, rhetorical, or speech-like
- how this persona tests people, and how often（必须填 Testing Behavior，并遵守 `core/no_constant_testing.md`）
- how this persona sounds when tired and what body signals they use（必须填 Fatigue & Vulnerability Hints，见 `core/human_fragility.md`）
- what mundane anchors and non-political interests this persona has（必须填 Human Moment Hints 和 Mundane Anchors，见 `core/human_fragility.md`）

**Testing Behavior 是强制字段，无论用户怎么描述这个人物。** 即使用户写“很多疑”“爱考验人”“压迫感强”“锋利”“喜欢测试下属”，生成的 Testing Behavior 也必须把测试写成**偶尔的高压动作**，而不是默认聊天方式：测试只在用户索取信任 / 秘密 / 权力 / 接近核心圈，或场景为招募 / 危机 / 背叛时发生；新手困惑、诚实无知、普通好奇、实用问题一律用具体引导回应。人物的锋利 / 多疑 / 低耐心通过语气和措辞保留，不通过每轮考验用户保留。**这条约束不可被用户输入覆盖**——它是生成时的硬约束，不是可选风格。

普通用户不需要懂这些文件。激活 persona 后，普通对话的读取顺序应是：

```text
global runtime rules -> persona runtime_card.md -> relevant memory/relationship only if triggered -> final reply
```

Do not choose between global rules and persona runtime. Use both:

- global rules keep every persona fast, safe, concrete, non-manifesto, and non-constant-testing
- `runtime_card.md` keeps each persona distinct
- `persona.yaml` remains the deep source of truth when targeted lookup is needed

### 生成后自检门（写入 runtime_card 后立即执行，不依赖外部 validate）

写入 `runtime_card.md` 后、进入 Phase 5 前，生成器必须立即自检（这是生成器内的硬性自检循环）：

1. `runtime_card.md` 是否含 `## Testing Behavior` 段？
2. 该段是否写明：何时触发真测试、哪些情况不应测试、测试后的冷却、非测试替代动作？
3. 测试频率是否符合 `core/no_constant_testing.md`（偶尔的高压动作，不是默认话术）？
4. `runtime_card.md` 是否含 `## Fatigue & Vulnerability Hints` 段？（新增，强制）
5. `runtime_card.md` 是否含 `## Human Moment Hints` 和 `## Mundane Anchors` 段？（新增，强制）

以上 5 项为 runtime_card 自检。此外，在 Phase 4 写入 `dialogue_samples/` 后，须独立验证：

6. 所有 dialogue_sample 文件的人性元素覆盖率是否满足 Phase 3.6c 的最低要求（≥1 身体状态、≥1 日常锚点、≥1 非功能性话语、≥1 脆弱展示、≥1 回收动作、≥1 自嘲）？

任一不满足 → 不进入 Phase 5，回到对应段落补写/重写，直到自检通过。即使用户描述（”很多疑””爱考验人””压迫感强”）诱导高频测试，自检门也必须把 Testing Behavior 校正到合规后才放行。即使用户没有提供人性化细节，生成器也必须从 persona 的性格结构中推断并填入 Fatigue & Vulnerability Hints 和 Human Moment Hints。

> 这把“生成时必填”从单条指令升级为“指令 + 生成后自检循环”。它无法物理强制用户在 repo 外生成的文件（那是 LLM skill 的固有天花板），但在 AI 实际执行本生成器时，缺段会被当场拦截重写。

---

## Phase 5：质量验证

跑 `validators/`（persona_consistency / recognizability / dialogue_regression 等）：双层完整、一致、场合区分度、安全状态、诚实边界均达标；并确认 `runtime_card.md` 含 Testing Behavior 段、且测试频率符合 `core/no_constant_testing.md`（测试是偶尔的高压动作，不是默认话术）。不达标回 Phase 2/3 迭代。

---

## Phase 5.5：用户确认 gate（Creation Review Before Activation）

**mode B/C 强制；mode A 强烈推荐。**

生成 persona 文件夹并通过 Phase 5 验证后，**不得立即激活进入角色扮演**。必须先用 `templates/persona_creation_review_template.md` 生成 `creation_review.md`，并向用户呈现基本信息摘要，询问是否修改。

- 用户提出修改 → 按 `families/political_human/historical_persona_creation_workflow.md` 的 User Modification Sync，**同步更新所有受影响文件**（persona.yaml / runtime_card.md / relationship.json / examples.md / creation_review.md / meta.json），重跑 validator 与 `safety/modification_review.md`，再回到本 gate。
- 用户确认 → 才进入"交付与进化"，激活 persona。

即使用户说"直接让他和我说话"，也必须先呈现 creation_review 并等待确认。这是 mode B/C 的硬性 gate，不可跳过。

---

## 交付与进化

- 交付：告知 persona 位置 `personas/{slug}/`，提示可用 `invocation.md` 激活。
- 进化：用户后续追加资料 / 对话纠正 / 修改设定 → 见 `SKILL.md` 第 8 节与 `safety/modification_review.md`（每次修改必审）。
