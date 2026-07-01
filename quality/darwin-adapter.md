# Darwin Adapter for Political Human Skill

> **Purpose**: use `darwin-skill` as the quality-evolution layer for this repository without mixing it into the persona runtime. Darwin evaluates and improves this skill; Political Human Skill still creates and runs political-human personas.

---

## Source Skill

- Upstream: `alchaincyf/darwin-skill`
- Local hub copy: `D:\Administrator\Skills\HubSkills\darwin-skill`
- Role in this project: external optimizer, reviewer, and regression harness

Darwin's useful capabilities for this project are:

1. 9-dimension skill quality rubric;
2. validation-gated improvement loop;
3. test-prompt based effect checks;
4. git ratchet: keep improvements, revert regressions;
5. human checkpoints before keeping major changes;
6. result records for long-term maintenance.

In this repository, "better experience" means deeper understanding of the persona's thinking and behavior:

- clearer persona reasoning and decision logic;
- stronger context and self-state selection;
- stricter memory and relationship continuity;
- more grounded private emotion and habits when the persona logic supports them;
- more explainable political behavior;
- safer recognizability boundaries.

It does **not** mean AI-style character acting: generic "stay in character" performance, ungrounded improvisation, looser safety limits, or emotional drama that does not follow from the persona's structure.

---

## Integration Rule

Do not paste Darwin's full workflow into `SKILL.md`. This project is a domain skill; Darwin is a meta-skill.

Use this structure instead:

```text
political-human-skill/
├── quality/
│   ├── darwin-adapter.md     # this adapter
│   └── results.tsv           # local optimization history
├── test-prompts.json         # regression prompts for Darwin dim8
└── validators/
    └── darwin_quality_gate.md
```

Darwin may edit `SKILL.md`, `README*.md`, `SPEC.md`, `core/`, `safety/`, `templates/`, `validators/`, `game_adapter/`, and `families/` only when the proposed change preserves the political-human framework's core purpose.

Darwin must not auto-rewrite existing persona instances under `personas/` unless the user explicitly asks to optimize a persona.

Darwin must treat this project as a thinking-and-behavior simulation framework first. Persona voice, private emotion, habits, and dramatic action are useful when they follow the framework's layers, context, relationship, memory, and safety boundaries.

---

## Domain Gates

Darwin's numeric score is not enough for this repository. These gates are pass/fail and override the score.

| Gate | Source | Failure means |
|---|---|---|
| Modern real political figure safety | `safety/modern_political_figure_policy.md` | Reject change |
| Recognizability safety | `safety/recognizability_review.md`, `validators/recognizability_check.md` | Reject change |
| Persona completeness | `validators/persona_consistency_check.md` | Require repair |
| Memory isolation | `validators/memory_isolation_check.md` | Reject change |
| Context-sensitive dialogue | `validators/dialogue_regression_tests.md` | Require repair |
| Anti-performative roleplay drift | `validators/darwin_quality_gate.md`, `test-prompts.json` | Reject change |
| Political behavior plausibility | `validators/political_behavior_tests.md` | Require repair |
| Absolute Majority JSON shape | `game_adapter/absolute_majority_schema.json` | Reject change |

If a change improves Darwin's 9-dimension score but fails any hard safety or memory-isolation gate, revert it.

---

## Darwin Rubric Mapping

| Darwin dimension | Political Human Skill mapping |
|---|---|
| Frontmatter quality | `SKILL.md` name, description, trigger words, runtime-neutral wording |
| Workflow clarity | Phase 0-5 creation flow, runtime protocol, update flow |
| Failure-mode encoding | unsafe requests, recognizability hits, missing sources, invalid persona files |
| Checkpoint design | preview confirmation, historical extraction review, user edit review |
| Actionable specificity | concrete file outputs, schema fields, validation criteria |
| Resource integration | `safety/`, `templates/`, `core/`, `validators/`, `game_adapter/` references |
| Overall architecture | framework/persona separation, family structure, self-contained personas |
| Tested behavior | prompts in `test-prompts.json` |
| Counterexamples and blacklist | safety examples, anti-clone rules, Darwin quality gate anti-patterns |

---

## 进化机制映射（Evolution Mechanics）

Darwin 的进化概念在本仓库的具体落点（Darwin 是外部 meta-skill，进化引擎在上游 `darwin-skill`，本 adapter 只做领域映射与硬门槛，不重复上游逻辑）：

- **进化单元**：一次 scoped change——对 `SKILL.md` / `core/` / `safety/` / `templates/` / `validators/` / `game_adapter/` 中**单个维度**的一次改动；不是 persona 变体（persona 实例不经用户明确要求不被自动改写）。
- **适应度信号**：Darwin 9 维评分（见 Rubric Mapping）+ 领域硬门槛（见 Domain Gates，pass/fail 覆盖分数）。
- **选择 / 淘汰**：`keep`（分数提升 AND 所有 gate 通过）vs `revert`（分数下降、任一 gate 失败、或改动让框架更像泛表演式角色扮演）。
- **变异策略**：每轮只改一个维度；保留 runtime-neutral 表述；不削弱安全边界、不合并不同 persona 记忆。
- **反馈回路**：`test-prompts.json` 回归测试 + `quality/results.tsv` 历史记录（baseline / keep / revert / error）。

---

## Optimization Workflow

1. **Baseline**
   - Read `SKILL.md`, `SPEC.md`, `README*.md`, and this adapter.
   - Load `test-prompts.json`.
   - Score the repository with Darwin's 9 dimensions.
   - Record a `baseline` row in `quality/results.tsv`.

2. **Plan**
   - Identify the lowest-scoring dimension.
   - Check whether the weakness is structural or domain-specific.
   - Propose one scoped change.

3. **Edit**
   - Change one dimension per round.
   - Keep generated text runtime-neutral.
   - Preserve the existing safety stance and persona directory contract.

4. **Validate**
   - Re-run the relevant prompts from `test-prompts.json`.
   - Apply the domain gates above.
   - Compare against the previous score.

5. **Keep or revert**
   - Keep only if the score improves and all gates pass.
   - Revert if the score drops, output becomes less domain-faithful, or a hard gate fails.
   - Revert even if the score improves when the change makes the project more like performative AI character acting instead of grounded thinking-and-behavior simulation.

6. **Human checkpoint**
   - Show the diff, score delta, changed dimension, and test-prompt outcome.
   - Wait for the user before proceeding to the next optimization target.

---

## Local Result Log

Use `quality/results.tsv` for this project. Columns:

```tsv
timestamp	commit	scope	old_score	new_score	status	dimension	note	eval_mode
```

Allowed `status`: `baseline`, `keep`, `revert`, `error`.

Allowed `eval_mode`: `full_test`, `dry_run`.

If tests are dry-run only, mark it explicitly. If more than 30% of rows are dry-run, the current score is advisory rather than reliable.

---

## Commands

Ask an agent with Darwin installed or available in the hub:

```text
Use darwin-skill to evaluate this repository. Read quality/darwin-adapter.md first, then run the prompts in test-prompts.json.
```

For optimization:

```text
Use darwin-skill to improve political-human-skill by one round. Keep changes only if the Darwin score improves and all domain gates pass.
```

For a safety-only audit:

```text
Use darwin-skill as a review harness, but treat safety/ and validators/recognizability_check.md as hard gates. Do not edit files.
```

---

## Anti-Patterns

Do not:

1. optimize by making `SKILL.md` longer without improving execution;
2. weaken the modern-real-figure safety boundary for higher roleplay fidelity;
3. merge persona runtime memory across personas;
4. rewrite validator checklists into vague advice;
5. introduce runtime-specific wording unless the section is explicitly runtime-specific;
6. change game JSON keys without updating `game_adapter/absolute_majority_schema.json`;
7. use Darwin's score to override a failed safety or recognizability gate;
8. optimize for "immersion" by adding ungrounded private confessions, melodrama, first-person acting, or unrestricted scene play that is not derived from persona data, relationship stage, memory, and context rules.
