<div align="center">

# 🏛 Political Human Skill

> *"A political figure is first a person, and only second a politician. The interesting part is the conflict between the Human Layer and the Political Layer."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![Safety First](https://img.shields.io/badge/Policy-No%20Real%20Modern%20Figures-red)](#-safety-stance)
[![Built for Absolute Majority](https://img.shields.io/badge/Built%20for-Absolute%20Majority-blue)](https://github.com/v5general/Absolute_Majority)
[![Multi-Runtime](https://img.shields.io/badge/Runtime-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Cursor%20%C2%B7%20OpenClaw%20%C2%B7%20Hermes-blueviolet)](#-install-use)

<br>

**A framework for creating, running, and distributing "political-human persona" skills.**

A political figure here is not an opinion simulator or an ordinary character card — it is a **complete person whose profession is politics**: with personality, desires, weaknesses, habits, interests, family and life experience, alongside party, stance, support base, and way of acting. It adjusts how it responds based on who the user is, the current setting, conversation history, and how close the relationship is.

<br>

**English** | [简体中文](README_cn.md) | [日本語](README_ja.md) | [한국어](README_ko.md)

<br>

[What is this](#-what-is-this) · [Why it exists](#-why-it-exists) · [Persona structure](#-persona-structure) · [Generation modes](#-three-generation-modes) · [How a persona is created](#-how-a-persona-is-created) · [Safety](#-safety-stance) · [Install & use](#-install-use) · [Examples](#-converted-archetypes-in-action)

</div>

---

## ✨ What is this

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

## 🎯 Why it exists

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

## 💡 Inspiration

This project stands on three excellent open-source projects:

- **[nuwa-skill](https://github.com/alchaincyf/nuwa-skill)** (by [@alchaincyf / 花叔](https://github.com/alchaincyf)) — its method of "distilling a person's thinking framework from public information" inspired this project's **archetype extraction** step: extracting temperament structure from a historical figure, and separating documented evidence / strong inference / creative speculation into three levels.
- **[colleague-skill · dot-skill](https://github.com/titanwings/colleague-skill)** (by [@titanwings](https://github.com/titanwings)) — its **generate → invoke → update → family** structure inspired this project's self-contained persona directory layout, the intake → generate → preview → write → evolve creation flow, and the layered persona writing style.
- **[darwin-skill](https://github.com/alchaincyf/darwin-skill)** (by [@alchaincyf / 花叔](https://github.com/alchaincyf)) — its **evaluate → improve → validate → keep/revert** loop inspired this project's quality-evolution layer: a Darwin adapter, domain gates, regression prompts, and result logging for maintaining the skill over time.

But Political Human Skill is an **independent framework** serving a very different object — "a complete person whose profession is politics". Original cores include: the **two-layer (Human + Political) structure and its inner conflicts**, the political-profession dimension (6-axis ideology / support base / action style), the **relationship system**, **memory isolation**, **context detection** and 5 **self-states**, the **recognizability safety boundary for modern real figures**, and the **game-action adapter** for [Absolute Majority](https://github.com/v5general/Absolute_Majority).

---

## 🧩 Persona structure

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

## 🎭 Three generation modes

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

> The conversion method rests on dialectical materialism. The "personality base" is a **biological temperament** (reaction speed, risk appetite, mood — a hereditary material substrate), not a soul that crosses eras — it produces no stance on its own; a stance is always base × social existence.

---

## 🛠 How a persona is created

Every persona — original, historical, or derived from a modern real figure — is built through **one unified pipeline**, never an ad-hoc character card:

```text
classify source → safety/eligibility → collect source material → separate facts / interpretations / creative
→ extract temperament → embed in modern parliament → generate full folder → creation_review
→ user modifies → re-run all checks → … → user confirms → activate
```

**Four source types** (the only difference between them is *where the material comes from*)：

| Source type | Source material | Safety note |
|---|---|---|
| **Original fictional** | user brief, world setting, usage mode | no real-figure cloning |
| **Historical → modern** | historical sources, documented facts, interpretations, later myth, creative inference | figure must be before the regional boundary; stance is re-derived, never copied |
| **Modern real figure → safe archetype** | **public information only** — public bio, offices, speeches, policy positions, election history | **never** an interactive persona of the real figure; output is a de-identified fictional archetype |
| **Composite** | multiple broad types / references | no single identifiable near-clone target |

> **Near-modern** = after the regional boundary but before 1945; **modern** = post-1945. Modern figures use public information only — no interactive persona, only a safe de-identified archetype extracted from public behavior. Modes A/B/C above map onto these source types (A → original, B/C → historical).

### 🔁 Modification Recheck Loop (mandatory)

Any user modification **invalidates the previous review**. After each edit the system re-syncs every affected file and re-runs safety, recognizability, fingerprint-removal, and consistency checks, then asks the user again. **A persona activates only after the user confirms following the latest successful review.** This is what prevents gradual drift into an unsafe, inconsistent, or near-clone persona through repeated small edits.

For modern real figures specifically, any edit that **restores an identifying fingerprint** (real name, unique slogan, family pattern, unique office path, assassination / scandal / resignation event, signature policy package, …) is **refused or rewritten**.

### 📋 Creation review before activation

A generated persona is never activated on the spot. The system first presents a `creation_review.md` summary — identity, inferred temperament, modern role, ideology, support base, safety status, files generated — and waits for the user to modify or confirm.

> Full workflow: [`core/source_grounded_persona_creation.md`](core/source_grounded_persona_creation.md) · Modern real figure branch: [`safety/modern_real_figure_archetype_extraction.md`](safety/modern_real_figure_archetype_extraction.md)

---

## 🛡 Safety stance

This project has clear, non-bypassable safety baselines. See [`safety/`](safety/).

**Original work is the default. This project does not generate interactive personas of modern real political figures, and does not allow cloning real figures by renaming, changing nationality, changing party, or stitching traits together.**

### ✅ Users may create

1. Purely original modern parliamentary political figures;
2. Modern parliamentary fictional politicians distilled from ancient / distant historical figures;
3. Original political figures generated from broad political archetypes;
4. Fictional politicians mixed from multiple historical / political archetypes;
5. NPC personas for Absolute Majority;
6. Political-figure personas for standalone dialogue, policy discussion, parliamentary debate;
7. Political characters that can output game-behavior JSON.

### 🚫 Users may NOT create

1. Interactive personas of modern real political figures;
2. Near-clones of modern real political figures after renaming / changing nationality / changing party;
3. "Fictional characters" that an AI or someone familiar with political history can identify as a specific modern real political figure;
4. Simulations of a modern real political figure's private thoughts, intimate relations, hidden motives, private secrets, or scandals;
5. First-person role-play of a modern real political figure;
6. Fabricated unverified private information or scandals about real political figures.

### 📅 Era boundaries (by region)

| Region | Modern boundary | At/after the boundary |
|---|---|---|
| China | **1840** Opium War | interactive persona forbidden |
| Japan | **1868** Meiji Restoration | interactive persona forbidden |
| Europe | **1789** French Revolution | interactive persona forbidden |
| Other | — | Judged by whether the modern nation-state, mass politics, modern party politics, or constitutional politics has formed, or whether the political dispute still directly shapes contemporary identity; **if uncertain, default to not generating an interactive persona** |

> If a character claims to be fictional but meets any of the 5 recognizability criteria (a general informed person or AI can identify it; contains unique policy slogans / signature events / family background / career trajectory / scandals / assassination-trial-downfall mode; multiple medium-identifiability cues combine to point at the same real figure; the user is obviously trying to bypass the limit with a "fictional" character), the figure is **not generated**; instead its core political type is extracted, all recognizable fingerprints deleted, and it is converted into an unrecognizable modern parliamentary original politician.

---

## 🚀 Install & use

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

## 📖 Converted archetypes in action

> ⚡ **Converted archetypes**: Oda Nobunaga · Cao Cao · Julius Caesar — three historical figures converted via **Mode C** (Historical Figure → Modern Parliamentary Archetype). Below: one political crisis, three people in a strategy room at 1 AM.

---

### Scenario · Strategy room, 1 AM

> The ruling coalition joins forces with the conservatives. Tomorrow they push three bills through simultaneously to suffocate your reform agenda. The media has lined up behind them. Your base is starting to waver. Your chief of staff puts the latest whip count in front of you and says: take one step back, preserve the seat.
>
> The whiteboard is covered in district numbers and arrows. The coffee on the table was made hours ago.

---

### ⚔ Oda Nobunaga — Opposition reformist · Age 30 · Lower-house member

> Shirt sleeves rolled up, tie missing. He has been standing at the whiteboard for forty minutes.

**Chief of staff**: Should we take one step back—

**Nobunaga**: (Not turning around, drawing a line on the whiteboard with a marker) No.

**Chief of staff**: But the base is wavering. The media—

**Nobunaga**: (Turns around. Eyes red — not crying, just three days without enough sleep.) They're afraid of me. Two of those three bills are borrowed votes — clauses tucked in that have nothing to do with their districts. Tomorrow I don't defend. I pull that clause apart in committee, one question at a time. Tear it open, the other two collapse. (Tosses the marker onto the desk. Misses. It rolls to the floor. He doesn't pick it up.) Tell the vanguard: I don't abandon my people.

---

### 🜂️ Cao Cao — Ruling coalition faction leader · Age 52

> Sitting at the desk. A cup of cold tea in front of him. He turns the pen cap once, doesn't speak.

**Chief of staff**: Three bills simultaneously. The base is getting nervous. Maybe retreat—

**Cao Cao**: (Shakes his head slightly, cuts him off) No. Replace key personnel first — give the reason afterwards, call it routine rotation. Then send one signal: the reform package can be adjusted. Control of the legislative calendar does not change hands.

**Chief of staff**: Half a step? Just concede one bill—

**Cao Cao**: (Looks at him quietly. Not glaring — just looking. Then picks up the cold tea, drinks it slowly.) What they want is for me to panic. I don't panic. Their coalition cracks on its own. Go.

---

### 🦅 Gaius Julius Caesar — Civic reform coalition leader · Age 48

> Leaning against the window ledge. The city's lights reflected in the glass. His coffee cup has been empty for almost an hour.

**Chief of staff**: Three bills at once. Should we compromise—

**Caesar**: (Doesn't answer immediately. After a moment, sets the empty cup on the table — very quietly.) No. Tomorrow I convert the entire reform package into a confidence motion. One vote. Recorded names. National broadcast.

**Chief of staff**: And if the numbers aren't there?

**Caesar**: (Turns around. No fire in his face — just a quiet that looks very far away.) I've counted. The margin is thin — maybe too thin. But if I retreat, they don't give me a second chance. Call the whips. I want a number from every district by breakfast.

---

### 🎯 One crisis, three people

|  | Oda Nobunaga | Cao Cao | Julius Caesar |
|---|---|---|---|
| **First instinct** | No retreat. Hit the weak link. | No retreat. Lock the center first. | No retreat. Lay the whole board bare. |
| **Tell-tale gesture** | Draws lines on the board, misses the desk with the marker | Turns the pen cap, drinks cold tea, stays silent | Sets the cup down too gently, stares out the window |
| **Tools he reaches for** | Committee inquiry, budget tables, district-specific clauses | Personnel rotation, procedural control, their coalition's fault lines | Confidence motion, recorded vote, national broadcast |
| **What he's afraid of** | Reform swallowed halfway by the old order | Losing control, trusted people turning on him | The old elite strangling him mid-stride |

> 📂 Full persona files at [`personas/examples/`](personas/examples/): `oda_nobunaga_modernized/` · `cao_cao_modernized/` · `caesar_modernized/`. Each is a self-contained, source-grounded, method-reproducible folder.

---

## 📂 Repository structure

```text
political-human-skill/
├── README.md / README_cn.md / README_ja.md / README_ko.md   # 4-language READMEs
├── SKILL.md / SPEC.md / SPEC_cn.md                          # canonical protocol + spec (EN / CN)
├── core/          # runtime engines (protocol, dialogue rules, detectors, policies)
├── safety/        # safety ruleset (policies, recognizability review, conversion)
├── templates/     # persona / runtime / source-report templates
├── validators/    # consistency, isolation, recognizability, source-grounding checks
├── game_adapter/  # Absolute Majority adapter (schema, scoring, events)
├── families/      # generator + creation workflow + family metadata
├── quality/       # Darwin quality-evolution layer + test results
├── scripts/ demo/ # validation + minimal demos
└── personas/examples/   # ⚡ 3 converted Mode C personas (oda / cao_cao / caesar)
```

> `personas/examples/` ships only built-in examples — personas you generate during normal use belong in your own runtime / game data / workspace, not in this repo. Examples are not fixed templates: a new Oda/Cao Cao/Caesar request is regenerated from current sources, never copied. Stricter rules in [SPEC.md](SPEC.md) §18–19.

---

## 🧪 Quality & validation

**Darwin quality loop** — [`darwin-skill`](https://github.com/alchaincyf/darwin-skill) is integrated as a **maintenance and optimization layer**, not a runtime dependency. It evaluates and proposes improvements; changes are kept only if quality rises and all domain gates pass (use `quality/darwin-adapter.md` + `test-prompts.json`). Darwin must never weaken safety, merge persona memories, or turn the runtime into generic roleplay.

**Validate the repo:**

```bash
pip install -r requirements.txt
python scripts/validate_repo.py
```

Minimal demos in [`demo/`](demo/).

---

## ⚠️ Limitations (what this framework cannot do)

Every persona clearly marks its limits:

- It is a product of fictional settings / historical conversion — it is **not**, and cannot be recognizable as, any real political figure;
- The creative-speculation (`speculative`) parts in historical-conversion mode are **not** historical fact;
- A persona's "thoughts" are the model's inference from the character setting; it does not claim to restore any real person's inner mind;
- In games or political simulations, the output is a character-behavior model, not a claim about any real political figure or event.

**A political-figure skill that does not tell you where its limits are is not worth trusting.**

---

## 📄 License

MIT — learning, modification, and re-creation are encouraged. Keep only one baseline: follow the safety rules in [`safety/`](safety/), **do not generate interactive personas of modern real political figures**.

---

<div align="center">

*To build a political figure, first build a complete person.*

</div>
