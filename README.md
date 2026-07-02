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

[Why it exists](#why-it-exists) · [Inspiration](#inspiration) · [Darwin quality loop](#darwin-quality-loop) · [Three generation modes](#three-generation-modes) · [How a persona is created](#how-a-persona-is-created--source-grounded-workflow) · [Persona structure](#persona-structure) · [Safety stance](#safety-stance) · [Install & use](#install--use) · [Converted archetypes in action](#converted-archetypes-in-action) · [Repository structure](#repository-structure)

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

This project is inspired by three excellent open-source projects:

- **[nuwa-skill](https://github.com/alchaincyf/nuwa-skill)** (by [@alchaincyf / 花叔](https://github.com/alchaincyf)) — its method of "distilling a person's thinking framework from public information" inspired this project's **archetype extraction** step: extracting temperament structure from a historical figure, and separating documented evidence / strong inference / creative speculation into three levels.
- **[colleague-skill · dot-skill](https://github.com/titanwings/colleague-skill)** (by [@titanwings](https://github.com/titanwings)) — its **generate → invoke → update → family** structure inspired this project's self-contained persona directory layout, the intake → generate → preview → write → evolve creation flow, and the layered persona writing style.
- **[darwin-skill](https://github.com/alchaincyf/darwin-skill)** (by [@alchaincyf / 花叔](https://github.com/alchaincyf)) — its **evaluate → improve → validate → keep/revert** loop inspired this project's quality-evolution layer: a Darwin adapter, domain gates, regression prompts, and result logging for maintaining the skill over time.

But Political Human Skill is an **independent framework** serving a very different object — "a complete person whose profession is politics". Original cores of this project include: the **two-layer (Human + Political) structure and its inner conflicts**, the political-profession dimension (6-axis ideology / support base / action style), the **relationship system** (a user claiming closeness is not automatically trusted), **memory isolation** (independent namespaces between personas), **context detection** and 5 **self-states**, the **recognizability safety boundary for modern real figures**, and the **game-action adapter** for [Absolute Majority](https://github.com/v5general/Absolute_Majority). 

---

## Darwin quality loop

**[darwin-skill](https://github.com/alchaincyf/darwin-skill)** is integrated as a **maintenance and optimization layer**, not as a persona runtime dependency. Use it when you want to evaluate or improve this repository's skill quality.

This repository provides:

- [`quality/darwin-adapter.md`](quality/darwin-adapter.md): how Darwin's 9-dimension rubric maps to Political Human Skill;
- [`validators/darwin_quality_gate.md`](validators/darwin_quality_gate.md): domain gates that override numeric score when safety, memory isolation, or game JSON fails;
- [`test-prompts.json`](test-prompts.json): regression prompts for original creation, historical conversion, safety refusal, user modification, dialogue context shift, memory isolation, Absolute Majority JSON, and README consistency;
- [`scripts/validate_repo.py`](scripts/validate_repo.py): parseability and required-file validation for JSON, YAML, SKILL frontmatter, examples, and Absolute Majority adapter files;
- [`demo/`](demo/): minimal dialogue and Absolute Majority walkthrough files;
- [`quality/results.tsv`](quality/results.tsv): local optimization history.

Typical use:

```text
Use darwin-skill to evaluate this repository. Read quality/darwin-adapter.md first, then run the prompts in test-prompts.json.
```

Optimization use:

```text
Use darwin-skill to improve political-human-skill by one round. Keep changes only if the Darwin score improves and all domain gates pass.
```

The rule is strict: Darwin may improve wording, structure, checks, and tests, but it must not weaken the safety boundary, merge persona memories, or turn the political-human runtime into a generic roleplay prompt.

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
- Mode C is a translation, not a slogan copy: **understand the historical social conditions** → **strip the non-portable era context** → **distill the stable personality structure** → **re-derive the stance inside a modern parliamentary setting**. The modern stance is **re-inferred from modern conditions, never mechanically copied** from the old era.
- Conversion first strips away what belonged to that era, then distills the personality that travels across time — how this person sees the world, what they care most about — and lets that personality walk into a modern parliament to find today's problem from its own angle and derive its own stance. 

---

The conversion method rests on dialectical materialism.

> Note: the "personality base" is a **biological temperament** (reaction speed, risk appetite, mood — a hereditary material substrate), not a soul that crosses eras — it produces no stance on its own; a stance is always base × social existence.

## How a persona is created — Source-Grounded Workflow

Every persona — original, historical, or derived from a modern real figure — is built through **one unified pipeline**, never an ad-hoc character card:

```text
classify source → safety/eligibility → collect source material → separate facts / interpretations / creative
→ extract temperament → embed in modern parliament → generate full folder → creation_review
→ user modifies → re-run all checks → … → user confirms → activate
```

### Four source types

| Source type | Source material | Safety note |
|---|---|---|
| `original_fictional_persona` | user brief, world setting, usage mode | no real-figure cloning |
| `historical_archetype_conversion` | historical sources, documented facts, interpretations, later myth, creative inference | figure must be before the regional boundary; stance is re-derived, never copied |
| `modern_real_figure_archetype_extraction` | **public information only** — public bio, offices, speeches, policy positions, election history | **never** an interactive persona of the real figure; output is a de-identified fictional archetype |
| `composite_archetype` | multiple broad types / references | no single identifiable near-clone target |

> **Near-modern** = after the regional boundary but before 1945; **modern** = post-1945. Modern figures use public information only — no interactive persona, only a safe de-identified archetype extracted from public behavior. Modes A/B/C above map onto these source types (A → original, B/C → historical).

### Modification Recheck Loop (mandatory)

Any user modification **invalidates the previous review**. After each edit the system re-syncs every affected file (persona.yaml / runtime_card / relationship / memory / examples / meta / creation_review / source_report / dialogue_samples) and re-runs safety, recognizability, fingerprint-removal, and consistency checks, then asks the user again. **A persona activates only after the user confirms following the latest successful review.** This is what prevents gradual drift into an unsafe, inconsistent, or near-clone persona through repeated small edits.

For modern real figures specifically, any edit that **restores an identifying fingerprint** (real name, unique slogan, family pattern, unique office path, assassination / scandal / resignation event, signature policy package, …) is **refused or rewritten**.

### Creation review before activation

A generated persona is never activated on the spot. The system first presents a `creation_review.md` summary — identity, inferred temperament, modern role, ideology, support base, safety status, files generated — and waits for the user to modify or confirm.

Full workflow: [`core/source_grounded_persona_creation.md`](core/source_grounded_persona_creation.md). Modern real figure branch: [`safety/modern_real_figure_archetype_extraction.md`](safety/modern_real_figure_archetype_extraction.md).

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

> ⭐ **Persona evolution** — personality and stance aren't frozen: they drift as major events pile up (a betrayed ally turns colder, a win emboldens the bold), and a persona's public actions feed back into public opinion, constituency, and factions. **Person and era shape each other.** See `core/persona_evolution.md`.

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

> The first time a persona is activated, it states once: "I am a character based on fictional / converted settings and do not correspond to any real political figure"; it is not repeated afterwards, to avoid repetitive disclaimers during normal use.

---

## Converted archetypes in action

> ⚡ **Converted archetypes**: Oda Nobunaga · Cao Cao · Julius Caesar — three historical figures converted via **Mode C** (Historical Figure → Modern Parliamentary Archetype). Below: one political crisis, three completely different responses.

Three historical figures — **Oda Nobunaga** (Sengoku period, 1534–1582), **Cao Cao** (Three Kingdoms, 155–220), **Julius Caesar** (Roman Republic, 100–44 BC) — have been converted into modern parliamentary politicians via Mode C. Below: one crisis, three completely different responses. Every line is driven by the persona's own Human Layer × Political Layer conflict.

---

### Scenario · Parliamentary blockade

> The ruling coalition joins forces with the conservative opposition. Tomorrow they will push three bills through parliament simultaneously, aiming to suffocate your reform agenda in a single stroke. The media has already lined up behind them. Your base is starting to waver.
>
> Your chief of staff advises: take one step back, preserve your seat, and live to fight another day.
>
> **What do you do?**

---

### Oda Nobunaga — Opposition reformist vanguard · Age 30 · Lower-house member

> **Human Layer**: Extreme agency · zero patience · wild and unorthodox · "if you don't risk dying, you can't win"
>
> **Political Layer**: Reformist opposition party · young-voter base · radical minority squeezed by the ruling party and conservatives alike
>
> **Core Conflict**: Wants to tear down the old order that creates monopolies, not just the monopolies — yet must use party machinery and parliamentary combat, the very products of the old politics, to do it

<div align="center">

**"Take one step back? One step back is one step into the coffin."**

</div>

**Nobunaga**: Three bills, the media, the conservatives — the fact that they're throwing everything they have at me just proves they're afraid of one man. Listen carefully. Tomorrow I don't defend. I attack. I hit their weakest bill, tear it open, and let the other two collapse on their own. Gamble my life? I've always lived by one rule: retreat guarantees defeat. The only way to flip the board is to push every last chip onto the table.

Tell the revolutionary vanguard corps: **follow me, and either we flip this board together, or we die on it together. I don't abandon my own.**

```
                     No defense ──→ Concentrate fire on the weakest bill
  Conventional ──┤
   response        Retreat & compromise ──→ ✗ This option does not exist
```

> 🧩 **Framework insight**: Nobunaga's response is driven by three layers firing simultaneously — `strategic_self` (cold calculus: use speed to overwhelm procedure), `wounded_self` (being surrounded triggers "risk everything to live" mode), and his deepest inner conflict (fierce loyalty to his followers — the fiercer the loyalty, the more isolated he becomes). His refusal to defend isn't recklessness. He's already priced in the patience cost of the conservative counterattack, and chosen to close the deal before they recover.

---

### Cao Cao — Ruling-coalition faction leader · Age 52

> **Human Layer**: Extreme realism · chronic suspicion · "talent above all" · only in poetry and wine does he ever let his guard down
>
> **Political Layer**: Dominant-party faction leader in the ruling coalition · bureaucratic-network base · rebuilder of order
>
> **Core Conflict**: Depends on "hire talent wherever you find it" and tolerating heterodox people to keep order running — yet is too suspicious to genuinely trust those same people

<div align="center">

**"Adjustments will be made through proper procedure. No need to amplify rumors into headlines."**

</div>

**Cao Cao**: Three bills pushed simultaneously — this isn't about reform. This is aimed at me. They think a wavering base will make me panic. I don't panic. First, lock down the center: replace key personnel with people who can hold. Then send one signal: the reform package can be tweaked, but control of the legislative calendar does not change hands. What do they want? They want me to make a mistake in the chaos. **I don't make mistakes. Their coalition will crack on its own.**

As for taking a step back — taking a step back isn't preserving a seat. It's telling them the center can be shaken. Not one step. Not half a step.

```
                     Lock down center first ──→ Signal flexibility ──→ Wait for their coalition to self-crack
  Crisis ──┤
   response           Retreat & compromise ──→ ✗ "Retreat tells them the center can be shaken"
```

> 🧩 **Framework insight**: Cao Cao's answer is a live demonstration of his control matrix — `strategic_self` (secure the power center first, lock it down with personnel and institutions), `public_self`'s calibrated vagueness ("adjustments through proper procedure"), and his core fear driving everything: loss of control and betrayal. He reframes the entire crisis as "someone testing whether the center can be shaken," then eliminates every variable with personnel and process. This isn't defense — it's turning a crisis into a loyalty test.

---

### Gaius Julius Caesar — Civic reform coalition leader · Age 48

> **Human Layer**: Magnetic charisma · iron self-discipline · profound historical consciousness · believes a little too much in personal destiny
>
> **Political Layer**: Civic-reform coalition leader · urban working-class and youth base · strongman reformer
>
> **Core Conflict**: Must transcend the old elite order — yet needs the old elite to recognize his legitimacy, and the stronger he becomes, the more they fear him

<div align="center">

**"This is not the moment to slow down. This is the moment to raise the stakes until they dare not follow."**

</div>

**Caesar**: Take one step back? Did you hear what you just said? The moment we take one step back, they'll smell blood — and the next move is flipping the entire table. This isn't a policy dispute. This is the old order trying to strangle reform. Three bills? Fine. Let them push them. Tomorrow I don't respond to the bills — I walk out of this chamber, straight to the people. I turn their three bills into a nationally televised debate: **is reform destroying the rules, or are the rules protecting the entrenched?**

Tell the ones who are hesitating: follow me, and you live. Look back, and you get swallowed. I'm putting myself on the line — my name, my standing, everything I've built. Either they get out of the way, or we walk this road to the end.

```
                     Fight inside parliament ──→ ✗ Don't enter their board
  Crisis ──┤
   response           Go to the people ──→ Turn it into a national broadcast ──→ Overwhelm institutional gridlock with popular will
```

> 🧩 **Framework insight**: Caesar's answer reveals his most distinctive political instinct — `strategic_self` doesn't choose to fight inside parliament; it chooses to **reset the board itself**: walk out, go to the people, turn three bills into a national broadcast. This is exactly the `primary: "bold reset"` action style. Driving this choice: his core fear (the moment he stops, the old order surges back and swallows every reform) and his inner conflict (championing reform and popular will, yet depending increasingly on personal prestige and extra-procedural means). His answer is simultaneously magnificent and dangerous — which is exactly Caesar.

---

### One crisis · Three signatures

| Same crisis | Instinctive move | One-line DNA |
|---|---|---|
| **Oda Nobunaga** | Don't defend. Attack. | *"Retreat guarantees defeat. Risk everything to live."* |
| **Cao Cao** | Lock the center first, signal second | *"I don't make mistakes. Their coalition cracks on its own."* |
| **Julius Caesar** | Leave the board. Reset the rules. | *"Raise the stakes until they dare not follow."* |

> Same crisis, same framework, three fundamentally different people. This is not prompt engineering — it is **Human Layer × Political Layer × Inner Conflicts**, six layers driving every response simultaneously. In each answer, you can read what they desire, what they fear, where they are weak, and the one thing they are most afraid of.
>
> 📂 Full persona files at [`personas/examples/`](personas/examples/): `oda_nobunaga_modernized/` · `cao_cao_modernized/` · `caesar_modernized/`. Each directory contains 7 self-contained files (SKILL.md / persona.yaml / runtime_card.md / relationship.json / memory.json / examples.md / meta.json), ready to run.

---

## Repository structure

```text
political-human-skill/
├── README.md / README_zh.md / README_ja.md / README_ko.md    # four-language READMEs
├── SKILL.md                                                    # canonical English runtime protocol
├── SPEC.md                                                     # canonical English authoring & safety spec
├── SPEC_zh.md                                                  # Chinese localized authoring & safety spec
├── test-prompts.json                                           # Darwin regression prompts
├── requirements.txt                                            # Python validation dependencies
├── scripts/                                                     # repository validation script
├── demo/                                                        # minimal runnable dialogue/game demos
├── quality/                     # Darwin quality-evolution layer (adapter + results)
├── safety/                      # safety ruleset (6 docs: policies, review flows, examples)
├── templates/                   # persona & runtime templates (5 files: YAML + JSON)
├── core/                        # runtime engines (7 docs: protocol, detectors, policies)
├── validators/                  # validators (7 docs: consistency, isolation, regression tests)
├── game_adapter/                # Absolute Majority adapter (schema, scoring, events)
├── families/political_human/    # family metadata (definition, generator, invocation)
├── review-stage/                # review state
└── personas/examples/           # ⚡ three converted Mode C personas (each 7 self-contained files)
    ├── oda_nobunaga_modernized/ # Oda Nobunaga → opposition reformist vanguard
    ├── cao_cao_modernized/      # Cao Cao → ruling-coalition faction leader
    └── caesar_modernized/       # Caesar → civic-reform coalition leader
```

> Full directory plan in [SPEC.md](SPEC.md) section 22. The repo ships the framework core: `SKILL.md` main protocol, `safety/` ruleset, `templates/`, `core/` runtime engines, `validators/`, `game_adapter/` (Absolute Majority adapter), `families/` (family metadata), the Darwin quality layer, and three self-contained converted example personas under `personas/examples/` (Oda Nobunaga · Cao Cao · Julius Caesar); all parts keep evolving.

---

## Generated personas and examples

`personas/examples/` is a small set of built-in examples, not a place where every generated character should be saved. Personas created during normal use belong in your own runtime, game data, local workspace, or downstream project. For example, an *Absolute Majority* integration can store generated NPCs in its own game data directory instead of adding them to this repository.

The examples are also not fixed templates. They show the file shape, safety boundaries, and conversion style. If you ask for a new Oda Nobunaga, Cao Cao, or Caesar conversion, the skill should generate it again from the current request and safety rules rather than copying the example folder.

For the stricter storage and example reuse rules, see [SPEC.md](SPEC.md) sections 18-19.

---

## Validation and demos

Install the YAML parser dependency if your Python environment does not already have it:

```bash
pip install -r requirements.txt
```

Run the repository validator:

```bash
python scripts/validate_repo.py
```

For a minimal walkthrough, see:

- [`demo/run_dialogue_demo.md`](demo/run_dialogue_demo.md)
- [`demo/run_absolute_majority_demo.md`](demo/run_absolute_majority_demo.md)
- [`game_adapter/absolute_majority_input_schema.json`](game_adapter/absolute_majority_input_schema.json)

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
