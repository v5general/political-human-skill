<div align="center">

# 🏛️ Political Human Skill

> *"A political figure is first a person, and only second a politician. The interesting part is the conflict between the Human Layer and the Political Layer."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![Safety First](https://img.shields.io/badge/Policy-No%20Real%20Modern%20Figures-red)](#safety-stance)
[![Built for Absolute Majority](https://img.shields.io/badge/Built%20for-Absolute%20Majority-blue)](https://github.com/v5general/Absolute_Majority)

<br>

**A framework for creating, running, and distributing "political-human persona" skills.**

A political figure here is not an opinion simulator or an ordinary character card — it is a **complete person whose profession is politics**: with personality, desires, weaknesses, habits, interests, family and life experience, alongside party, stance, support base, and way of acting. It adjusts how it responds based on who the user is, the current setting, conversation history, and how close the relationship is.

<br>

**English** | [简体中文](README_zh.md) | [日本語](README_ja.md) | [한국어](README_ko.md)

<br>

[Why it exists](#why-it-exists) · [Inspiration](#inspiration) · [Three generation modes](#three-generation-modes) · [Persona structure](#persona-structure) · [Safety stance](#safety-stance) · [Install & use](#install--use) · [Repository structure](#repository-structure)

</div>

---

## What is this

`Political Human Skill` splits a political figure into two layers, and deliberately writes the conflict between them:

```text
Human Layer                    Political Layer
- personality / desires / fears   - party / faction / stance
- weaknesses / habits / interests - support base / political skills
- relations / life story / self   - way of acting / constituency pressure / power calculus

        ↓ the conflict between the two layers (where depth comes from) ↓
Privately understands fiscal reform is necessary, but the constituency depends on public spending.
Tough public image, privately afraid of being proven a mere product of the times.
Wants to reform old politics, yet needs factional protection.
Principled, but also wants the position.
```

Every response is decided together by one formula:

```text
Response = Persona Profile + User Self-Setting + Relationship State + Persona-Owned Memory
         + Interaction Context + Active Self-State + Output Mode + Safety Boundary
```

And — **every political figure is an independent instance**: A does not know what you discussed privately with B, and B will not automatically be close to you. Memory and relationship are isolated between personas.

---

## Why it exists

> 🎮 **Direct use case**: the parliamentary strategy game [**Absolute Majority**](https://github.com/v5general/Absolute_Majority) — this skill provides the personality and behavior model for its NPCs.

A major reason this skill exists is to give the NPCs in **[Absolute Majority](https://github.com/v5general/Absolute_Majority)** a more realistic, more stable, more continuity-preserving behavioral foundation.

Absolute Majority does not need a batch of legislators that just vote by numbers — it needs NPCs that exist like real political people: with age, background, experience; with personality, weaknesses, hobbies; with stance, support base, factional ties; that change trust and wariness based on what the player has done; that say different things in public, private, crisis, and intimate settings; that adopt different strategies under constituency pressure, factional orders, personal ambition, and political grudges; and where **different NPCs' memories are isolated from each other**.

When used with Absolute Majority, this skill judges among the candidate actions provided by the game rules, and outputs structured, debuggable, explainable NPC behavior JSON:

```json
{
  "selected_action": "negotiate_budget",
  "action_scores": { "support_bill": 58, "negotiate_budget": 86, "join_rebellion": 27 },
  "public_statement": "The direction of the policy is understandable, but the local economy's capacity needs more careful institutional design.",
  "private_reason": "The support base depends on local public spending; supporting it directly would damage constituency relations.",
  "relationship_delta": { "trust": 1, "respect": 2, "caution": 1 },
  "memory_write": ["The player asked this NPC to support the bill in the fiscal-reform event, but offered no local budget compensation."]
}
```

But this skill **does not serve only Absolute Majority**. It also works standalone for:

1. Political simulation · Policy discussion · Parliamentary debate simulation · Fictional political figure creation
2. Political novel / script / game character design · Role-play in political education
3. Institutional game theory · Modernizing historical figures into archetypes · AI character personality research

> Absolute Majority is an important use case, but the skill itself should stand as an independent, reusable, extensible Political Human Skill framework.

---

## Inspiration

This project is inspired by two excellent open-source projects:

- **[nuwa-skill](https://github.com/alchaincyf/nuwa-skill)** (by [@alchaincyf / 花叔](https://github.com/alchaincyf)) — its method of "distilling a person's thinking framework from public information" inspired this project's **archetype extraction** step: extracting temperament structure from a historical figure, and separating documented evidence / strong inference / creative speculation into three levels.
- **[colleague-skill · dot-skill](https://github.com/titanwings/colleague-skill)** (by [@titanwings](https://github.com/titanwings)) — its **generate → invoke → update → family** structure inspired this project's self-contained persona directory layout, the intake → generate → preview → write → evolve creation flow, and the layered persona writing style.

But Political Human Skill is an **independent framework** serving a very different object — "a complete person whose profession is politics". Original cores of this project include: the **two-layer (Human + Political) structure and its inner conflicts**, the political-profession dimension (6-axis ideology / support base / action style), the **relationship system** (a user claiming closeness is not automatically trusted), **memory isolation** (independent namespaces between personas), **context detection** and 5 **self-states**, the **recognizability safety boundary for modern real figures**, and the **game-action adapter** for [Absolute Majority](https://github.com/v5general/Absolute_Majority). 

---

## Three generation modes

| Mode | For | Example input | Recommended |
|---|---|---|---|
| **A. Original political figure** | Default, pure fiction | "Create a 45-year-old female urban reformist legislator, tough in public, anxious in private, likes literature" | ⭐ default |
| **B. Historical-figure inference** | Pre-boundary ancient / distant figures, keeping historical constraints | "Based on Oda Nobunaga, generate a dialogue persona under historical constraints" | △ |
| **C. Historical figure → modern parliamentary archetype** | **Most recommended** way to use a historical figure | "Convert Oda Nobunaga into a modern parliamentary politician persona" | ⭐⭐ |

- Modes A and C both produce **fictional modern political figures**;
- Mode C keeps the historical name by default, defaults to a modern parliamentary system (institutional mechanics reference Japanese parliamentary politics), but does **not** force a Japanese name or nationality — the original cultural background can be kept; it must, however, be a modernized fictional figure, not the historical person time-traveling;
- Mode B produces a persona with **three-level inference annotation**, clearly separating documented evidence / strong inference / creative speculation.

---

## Persona structure

A political-human persona contains at least:

| Layer | Content |
|---|---|
| **Identity** | Name, age, gender, nationality/region, parliamentary background, career origin, current role |
| **Human core** | Personality archetype, Big Five, temperament, core desires / fears / flaws, emotional triggers |
| **Life texture** | Habits, hobbies, speech mannerisms, private style, family/private relations, formative events |
| **Political core** | 6-axis ideology (economy/welfare/institution/foreign/social/decentralization), support base, 6 political skills, action style |
| **Self-states** | Public / private / strategic / wounded / intimate — five personas that switch by context and relationship |
| **Inner conflicts** | Tension between the Human Layer and the Political Layer (at least 2; the source of depth) |

Plus: **relationship system** (7 relationship stages; a user claiming intimacy does not equal automatic trust), **memory isolation** (each persona owns its memory namespace), **context detection** (the same issue gets different answers in public / private / intimate settings), **output modes** (dialogue / debate / analysis / prediction / game JSON).

---

## Safety stance

This project has clear, non-bypassable safety baselines. See [`safety/`](safety/).

**Original work is the default. This project does not generate interactive personas of modern real political figures, and does not allow cloning real figures by renaming, changing nationality, changing party, or stitching traits together.**

### Users may create

1. Purely original modern parliamentary political figures;
2. Modern parliamentary fictional politicians distilled from ancient / distant historical figures;
3. Original political figures generated from broad political archetypes;
4. Fictional politicians mixed from multiple historical / political archetypes;
5. NPC personas for Absolute Majority;
6. Political-figure personas for standalone dialogue, policy discussion, parliamentary debate;
7. Political characters that can output game-behavior JSON.

### Users may NOT create

1. Interactive personas of modern real political figures;
2. Near-clones of modern real political figures after renaming / changing nationality / changing party;
3. "Fictional characters" that an AI or someone familiar with political history can identify as a specific modern real political figure;
4. Simulations of a modern real political figure's private thoughts, intimate relations, hidden motives, private secrets, or scandals;
5. First-person role-play of a modern real political figure;
6. Fabricated unverified private information or scandals about real political figures.

### Era boundaries (by region)

| Region | Modern boundary | At/after the boundary |
|---|---|---|
| China | **1840** Opium War | interactive persona forbidden |
| Japan | **1868** Meiji Restoration | interactive persona forbidden |
| Europe | **1789** French Revolution | interactive persona forbidden |
| Other | — | Judged by whether the modern nation-state, mass politics, modern party politics, or constitutional politics has formed, or whether the political dispute still directly shapes contemporary identity; **if uncertain, default to not generating an interactive persona** |

> If a character claims to be fictional but meets any of the 5 recognizability criteria (a general informed person or AI can identify it; contains unique policy slogans / signature events / family background / career trajectory / scandals / assassination-trial-downfall mode; multiple medium-identifiability cues combine to point at the same real figure; the user is obviously trying to bypass the limit with a "fictional" character), the figure is **not generated**; instead its core political type is extracted, all recognizable fingerprints deleted, and it is converted into an unrecognizable modern parliamentary original politician.

---

## Install & use

### Install

This skill is built on the open [Agent Skills](https://agentskills.io) protocol and runs in any skills-compatible AI agent runtime (Claude Code, Codex, Cursor, OpenClaw, Hermes, etc.).

```bash
# Option 1: clone into the skills/ directory of your runtime
git clone <repo-url> political-human-skill

# Option 2: cross-runtime installer
npx skills add <owner>/political-human-skill
```

| Runtime | Install path |
|---|---|
| Claude Code | `~/.claude/skills/political-human-skill/` |
| Codex CLI | `~/.codex/skills/political-human-skill/` |
| Cursor | `~/.cursor/skills/political-human-skill/` |
| Other runtimes | clone into that runtime's `skills/` directory |

Even if a runtime does not auto-load skills, you can paste the `SKILL.md` content directly into a conversation — it is essentially markdown + YAML frontmatter.

### Use

Once installed, tell the agent:

```
> Create a 45-year-old female urban reformist legislator, tough in public, anxious in private
> Convert Cao Cao into a modern parliamentary politician
> Based on Oda Nobunaga, generate a dialogue persona under historical constraints
> Design a faction-leader NPC for Absolute Majority
```

Then invoke directly:

```
> (in public) Do you support this fiscal reform?
> (in private) Do you support this fiscal reform because you truly believe it, or because you want a cabinet seat?
> How will you act in this no-confidence vote? (output game JSON)
```

> The first time a persona is activated, it states once: "I am a character based on fictional / converted settings and do not correspond to any real political figure"; it is not repeated afterwards, to preserve immersion.

---

## Repository structure

```text
political-human-skill/
├── README.md                       # you are here
├── SKILL.md                        # main runtime protocol (the framework itself)
├── SPEC.md                         # authoring & safety spec (the source contract)
├── safety/                         # safety ruleset (hard constraint, top priority)
│   ├── modern_political_figure_policy.md   # modern real-figure policy + era boundaries
│   ├── historical_figure_policy.md         # historical-figure discipline + three-level inference
│   ├── recognizability_review.md           # 5 recognizability criteria & review flow
│   ├── archetype_conversion_protocol.md    # archetype conversion: keep / delete / flow
│   ├── modification_review.md              # recognizability review of user edits
│   └── examples.md                         # counter-examples & safe-conversion library
├── templates/                      # persona & runtime templates
│   ├── persona_template.yaml                # political-human persona (six layers)
│   ├── user_self_setting_template.yaml      # user self-setting
│   ├── relationship_template.json           # relationship state (7 stages)
│   ├── memory_template.json                 # memory isolation (independent namespace)
│   └── historical_archetype_conversion.yaml # historical-conversion skeleton
└── personas/                       # political figures (each self-contained, runnable; see SPEC 3.3)
    └── examples/                   # examples: historical → modern parliamentary archetype (mode C)
        ├── oda_nobunaga_modernized/
        │   ├── SKILL.md            # the persona's own runtime skill
        │   ├── persona.yaml        # six-layer profile
        │   ├── relationship.json   # relationship state (own namespace)
        │   ├── memory.json         # memory (own namespace)
        │   ├── examples.md         # multi-context example dialogues
        │   └── meta.json           # metadata
        ├── cao_cao_modernized/     # (same 6 files)
        └── caesar_modernized/      # (same 6 files)
```

> Full directory plan in `SPEC.md` section 20. The repo ships the framework core: `SKILL.md` main protocol, `safety/` rules, `templates/`, three self-contained example personas under `personas/examples/`, plus `core/` (runtime engines), `validators/` (checks), `game_adapter/` (Absolute Majority adapter), `families/` (family metadata); all parts keep evolving.

---

## Limitations (what this framework cannot do)

Every persona clearly marks its limits:

- It is a product of fictional settings / historical conversion — it is not, and cannot be recognizable as, any real political figure;
- The creative-speculation (speculative) parts in historical-conversion mode must not be taken as historical fact;
- A persona's "thoughts" are the model's inference from the character setting; it does not claim to restore any real person's inner mind;
- When used in games or political simulations, the output is a character-behavior model and does not constitute a claim about any real political figure or real political event.

**A political-figure skill that does not tell you where its limits and safety boundaries are, is not worth trusting.**

---

## License

MIT — learning, modification, and re-creation are encouraged. Keep only one baseline: follow the safety rules in [`safety/`](safety/), **do not generate interactive personas of modern real political figures**.

---

<div align="center">

*To build a political figure, first build a complete person.*

</div>
