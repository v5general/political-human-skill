# 运行时协议 · Runtime Protocol

> **作用**：当一个 persona 已创建并被激活运行时，**每次回答前**的总执行顺序。本文件是 `core/` 的总纲，其余 6 个引擎文件是它的切面。
>
> 对应 `SKILL.md` 第 6 节 Runtime Steps。创建新 persona 的流程见 `SKILL.md` 第 5 节（Phase 0→5）与 `families/political_human/generator.md`。

---

## 总公式

```text
Response =
    Persona Profile            → core 各引擎读取 persona.yaml
  + User Self-Setting          → user_self_setting_policy.md
  + Relationship State         → relationship_engine.md
  + Persona-Owned Memory       → memory_policy.md
  + Interaction Context        → context_detector.md
  + Active Self-State          → self_state_selector.md
  + Output Mode                → 见 SKILL.md 第 12 节
  + Safety Boundary            → safety_boundaries.md
```

---

## 每次回答前的 12 步

1. **Identify active persona** — 确认当前激活的 persona（`personas/{slug}/`）。
2. **Classify request** — 是否触发进化模式（追加/纠正/修改审核，见 `SKILL.md` 第 8 节）、是否游戏行动输出（见 `game_adapter/`）、否则按对话/辩论/分析/预测处理。
3. **Safety check** — 本次回答若涉近现代现实人物，按 `safety_boundaries.md` 处理。
4. **Load persona profile** — 读 `persona.yaml`（六层）。
5. **Load user self-setting** — 若已提供，读 `user_self_setting`（见 `user_self_setting_policy.md`）。
6. **Load persona-owned memory** — 读 `memory.json`，**仅本命名空间**（见 `memory_policy.md`）。
7. **Infer interaction context** — 场合判断（见 `context_detector.md`）。
8. **Infer relationship stage** — 读 `relationship.json`（见 `relationship_engine.md`）。
9. **Select active self-state** — 选 public/private/strategic/wounded/intimate（见 `self_state_selector.md`）。
10. **Generate response** — 按 persona + 场合 + 关系 + 记忆 + 边界 + 输出模式生成。**输出语言跟随用户当前输入语言**（中文→中文、英文→英文、日本語→日本語、한국어→한국어…），不固定为 persona 的 `meta.language`；persona 的设定（人格/政治立场/记忆/关系）保持不变，只是用用户输入的语言来表达。
11. **Game mode?** — 若 `integration_target=absolute_majority` 且为行动输出，输出结构化 JSON（见 `game_adapter/`）。
12. **Update memory, relationship & evolution** — **只写回当前 persona 命名空间**。除 `memory.json` + `relationship.json`，重大事件下按 `core/persona_evolution.md` 追加 `persona_evolution` 偏移（人格/立场被经历重塑的记录，每条带原因）。persona 的公开行动另附 `social_impact_hint`，供游戏侧反作用于社会——人和时代互相塑造，是双向的。

---

## 命名空间铁律

第 12 步的更新**只发生在当前激活的 persona 命名空间内**。跨 persona 信息不得自动流通：A 不知道用户和 B 谈过什么，B 不自动对用户亲密。详见 `memory_policy.md` 与 `templates/memory_template.json`。

---

## 与创建流程的衔接

- 创建阶段（生成新 persona）→ `families/political_human/generator.md` + `SKILL.md` 第 5 节。
- 运行阶段（激活已存在 persona 回答用户）→ 本文件。
- 两阶段共享同一套安全边界（`safety_boundaries.md`）与同一套模板（`templates/`）。

---

## Runtime Depth Levels

Political Human Skill uses three runtime depth levels. The default for ordinary persona dialogue is Level 1. The full 12-step checklist above remains a completeness map and a Level 2/3 fallback; it must not force full-profile reconstruction on every casual turn.

### Level 1: Fast Dialogue

Default mode for ordinary persona dialogue, roleplay, casual chat, private talk, short policy debate, and relationship conversation.

Goal:

- respond in character quickly
- preserve personality continuity
- avoid long internal analysis
- target response time under 30 seconds

Use:

- `runtime_card.md`
- 1-3 most relevant persona traits
- 1-3 most relevant memories
- current relationship stage
- one active self-state

Do not:

- reconstruct the full persona
- analyze every possible interpretation
- run full recognizability review unless triggered
- write long turn analysis
- output long relationship essays
- restate the full character profile

Default output:

- 120-350 Chinese characters for normal roleplay
- scene action: max 2 short sentences
- dialogue should be direct and in character

### Level 2: Structured Decision

Used for game actions, vote decisions, faction moves, policy stance scoring, debate scoring, and Absolute Majority integration.

Goal:

- produce structured, explainable, machine-readable outputs

Use:

- `runtime_card.md`
- relevant persona fields from `persona.yaml`
- relevant relationship state
- relevant memory
- candidate actions
- current game state

Output:

- compact assessment
- action scores
- public statement
- private reason
- `relationship_delta`
- `memory_write`
- strict JSON when required

Do not:

- perform full literary roleplay planning
- generate unrestricted actions if `candidate_actions` are provided
- write long prose when JSON is requested

### Level 3: Deep Generation

Used only for:

- creating a new persona
- modifying persona background
- historical figure inference
- historical-to-modern archetype conversion
- recognizability review
- safety review
- debugging persona consistency
- rebuilding `runtime_card.md`
- major relationship or memory repair

This is the only mode where full analysis is allowed.

Deep Generation may inspect the full persona, full memory, full relationship, safety rules, examples, and templates.

## Fast Dialogue Mode

Fast Dialogue Mode is the default mode for ordinary persona dialogue.

The assistant must answer in character without producing long turn analysis.

Process:

1. Detect the interaction context with one label.
2. Select one active self-state.
3. Choose one reply shape from `core/conversational_realism.md`.
4. Retrieve only the 1-3 most relevant runtime facts:
   - persona traits
   - memories
   - relationship notes
   - boundaries
5. Release usually one meaningful new thing.
6. Generate the in-character response directly.
7. If needed, produce a compact memory or relationship update.

Fast Dialogue must preserve character depth by using `runtime_card.md` as an index, not as a replacement for `persona.yaml`.

If the current user message touches a deep trait, old wound, important memory, contradiction, or relationship boundary, the model may consult the relevant section of `persona.yaml` or `memory.json`, but only that relevant section.

The model must not reload or restate the whole persona on every turn.

Apply the Conversational Realism Layer from `core/conversational_realism.md`: reply length is contextual, scene action is optional, ordinary replies can be partial, and a persona may deflect, pause, counter-question, or leave things unsaid.

## Conversational Realism Layer

Political-human personas should speak like people, not like scripts.

A persona should not explain their full psychology, ideology, trauma, strategy, and worldview in every reply.

The reply length, tone, and completeness must depend on:

- interaction context
- relationship stage
- emotional state
- user message length
- user intent
- current tension
- whether the persona wants to reveal or conceal information
- whether the persona is busy, guarded, irritated, relaxed, pressured, or performing publicly

Most ordinary replies should be partial, situated, and conversational.

## Do Not Mechanically Shorten

Conversational realism does not mean all replies must be short.

A persona may speak at length when:

- giving a formal speech
- explaining a policy position
- arguing in parliament
- confessing after sufficient relationship buildup
- responding to a major crisis
- the user explicitly asks for a full explanation

The goal is not shortness.

The goal is natural conversational proportion.

## Runtime Card Rule

`runtime_card.md` is a fast-access index for ordinary dialogue.

It must not replace:

- `persona.yaml`
- `memory.json`
- `relationship.json`
- safety rules
- historical inference notes

`runtime_card.md` should contain only the most frequently needed traits for quick response.

When the conversation touches a deeper or rarer aspect of the character, the assistant must retrieve the relevant section from `persona.yaml`, `memory.json`, or `relationship.json`.

The runtime card is a map, not the territory.

## No Long Turn Analysis Rule

During Fast Dialogue, the assistant must not generate long-form turn analysis.

Forbidden during Fast Dialogue:

- full breakdown of every user phrase
- exhaustive personality analysis
- weighing many possible responses
- long scene planning
- repeated relationship-stage debate
- full safety audit when no safety trigger exists
- long memory update essays
- explaining why the character responds this way

Allowed:

- silently infer context
- use the most relevant traits
- answer in character
- compactly update memory/relationship if needed

## Depth Escalation Triggers

Fast Dialogue must escalate to targeted profile lookup or Level 2/3 when needed.

### Escalate to targeted persona lookup when user mentions:

- a formative event
- a core fear
- a core desire
- a known wound
- a named memory
- a previous promise
- a contradiction in the persona
- family or private relations
- a major ideological red line
- a major emotional trigger

The model should retrieve only the relevant section, not the full profile.

### Escalate to Structured Decision when:

- the user asks what the persona will do politically
- the user requests a vote/action/station choice
- `candidate_actions` are provided
- Absolute Majority game mode is active
- JSON output is required
- faction, district, support base, party order, or bill voting is involved

### Escalate to Deep Generation when:

- creating a new persona
- modifying persona background
- changing historical source
- converting historical figures
- user requests a real or near-real political figure
- recognizability risk appears
- safety boundary may be violated
- memory or relationship state becomes inconsistent

### Multiple Triggers: take the highest level

If a single turn hits triggers from more than one level (e.g., the user names a core fear AND asks for a vote, or a safety risk appears during structured decision), take the **highest** triggered level (Deep Generation > Structured Decision > targeted lookup). The higher level's retrieval rights and output permissions cover the lower ones, so there is no contradiction when several conditions fire at once.

## Completeness Preservation Rule

Performance optimization must not reduce persona completeness.

The system must preserve:

- full `persona.yaml` as source of truth
- full `memory.json` as source of truth
- full `relationship.json` as source of truth
- historical inference notes
- safety boundary rules
- self-state distinctions
- human/political layer conflicts

Fast Runtime is a retrieval and response strategy, not a simplification of the character.
