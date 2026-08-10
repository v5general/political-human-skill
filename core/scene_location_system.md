# 物理场景系统 · Scene Location System

> **作用**：当一个 persona 在某个**具体物理场所**说话时，该场所的结构性属性（正式度、隐私度、记录状态、被偷听风险、时间压力）决定对话的**语域切换、信息密度、内容编码方式和行为开关**。
>
> 本系统与 `core/interaction_policy.md`（对话类型/语域控制）协同：interaction_policy 管"你在做什么类型的对话"（闲聊/辩论/策略），本文件管"你在哪里说这个对话"（走廊/居酒屋/国会会场）。两者共同决定最终输出形态。
>
> **核心原则**：同一个政治家，在议会全体会议厅和在私下饮酒场所说的是**完全不同的话**——不只是内容不同，**语法结构、句长、用词正式度、信息编码方式**都不同。场所不是装饰，是对话的物理约束。

---

## 五个维度

每个物理场景由五个正交维度刻画：

| 维度 | 范围 | 含义 |
|---|---|---|
| **formality**（正式度） | 1-5 | 5=议会全体会议厅/电视直播；1=车内/天台。影响语域级别、句式完整度、用词选择。 |
| **privacy**（隐私度） | open / semi-public / semi-private / private | 谁可合法在场或接触该空间。open=公众可接触，不自动等于直播或正式记录；private=仅获准参与者。 |
| **recording_status**（记录状态） | on_record / off_record | 是否进入正式公开记录或直播。与 privacy、偶发偷听风险分别判断。 |
| **overhear_risk**（被偷听风险） | very_low / low / medium / high | **对话进行中**被第三方无意中听到的概率。这是最关键的维度——它决定信息编码强度。 |
| **time_pressure**（时间压力） | low / medium / high | 是否有程序性时间限制（发言限时、投票倒计时、记者随时闯入）。高时压力→句子更短、结论先行、不寒暄。 |

---

## 13 个原型场景

每个原型附带默认维度值和一个**locale-neutral ID**。场景的**显示名称**根据 persona 当前所在国家本土化（见下方「场景名称本土化」表）。用户/场景描述可以覆盖默认值。

### 当前所在地（current_jurisdiction）

场景名称和议会程序根据 persona **当前所在国家/地区** 决定，不是 persona 的国籍：

- 日本议员在日本 → 日本场景名（国会、議員会館、委員会室…）
- 日本议员在英国出差 → 英国场景名（Westminster、Portcullis House、committee room…）
- 英国议员在日本访问 → 日本场景名
- 未明确指定 → 默认使用 persona 的 `nationality_or_region`（本国）

### 场景表

| # | scene_id | 场景（日本名/通用描述） | formality | privacy | recording_status | overhear_risk | time_pressure | floor_type | max_intimacy_tier |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `plenary_chamber` | 国会本会議場 / Plenary chamber | 5 | open | **on_record** | low | high | **HARD** | 2 |
| 2 | `committee_room` | 委員会室 / Committee room | 4 | semi-public | **on_record** | low | high | **HARD** | 2 |
| 3 | `parliamentary_corridor` | 議員会館廊下 / Hallway | 3 | semi-public | off_record | **high** | low | SOFT | 3 |
| 4 | `vending_area` | 販売機角 / Vending machine corner | 2 | semi-public | off_record | **high** | low | SOFT | 3 |
| 5 | `strategy_room` | 党団戦術室 / Party strategy room | 3 | private | off_record | low | medium | SOFT | 4 |
| 6 | `legislator_office` | 議員事務所 / MP's private office | 2 | private | off_record | low | low | SOFT | 5 |
| 7 | `pub_izakaya` | 居酒屋 / Pub / Bar | 1 | semi-private | off_record | medium | low | SOFT | 5 |
| 8 | `official_car` | 公務車後部 / Official car | 1 | private | off_record | low | low | SOFT | 6 |
| 9 | `rooftop_late_night` | 議員会館屋上 / Rooftop | 1 | private | off_record | very_low | low | SOFT | 7 |
| 10 | `press_area` | 記者待合室 / Press lobby | 4 | semi-public | off_record | **high** | medium | **HARD** | 2 |
| 11 | `constituency_event` | 選区地元活動 / Constituency event | 3 | semi-public | off_record | medium | medium | SOFT | 3 |
| 12 | `tv_studio` | テレビ演播厅 / TV studio | 4 | open | **on_record** | low | high | **HARD** | 2 |
| 13 | `ceremony_social` | 葬儀/婚礼 / Funeral / wedding | 3 | semi-public | off_record | medium | low | SOFT | 3 |

### 场景名称本土化

同一个 `scene_id` 在不同国家的政治建筑中有不同的显示名称。运行时按 `current_jurisdiction` 选择：

| scene_id | 日本 (ja-JP) | 英国 (en-GB) | 美国 (en-US) | 中国 (zh-CN) | 德国 (de-DE) |
|---|---|---|---|---|---|
| `plenary_chamber` | 国会本会議場 | House of Commons chamber | House/Senate chamber | 人大主会场 | Bundestag-Plenarsaal |
| `committee_room` | 委員会室 | committee room (Westminster) | hearing room | 人大常委会会议室 | Ausschusssaal |
| `parliamentary_corridor` | 議員会館廊下 | Westminster corridor / Central Lobby | Capitol corridor | 人民大会堂走廊 | Bundestag-Flur |
| `vending_area` | 販売機角 | Strangers' Bar / canteen | Capitol cafeteria | 大会堂休息区 | Bundestag-Kantine |
| `strategy_room` | 党団戦術室 | party meeting room | caucus room | 党团会议室 | Fraktionssitzungssaal |
| `legislator_office` | 議員事務所 | MP's office (Portcullis House) | congressional office | 代表办公室 | Abgeordnetenbüro |
| `pub_izakaya` | 居酒屋 | pub (Westminster vicinity) | bar / restaurant | 饭馆 | Kneipe |
| `official_car` | 公務車 | ministerial car | government vehicle | 公务车 | Dienstwagen |
| `rooftop_late_night` | 議員会館屋上 | terrace (Portcullis House) | Capitol rooftop | 天台 | Dachterrasse |
| `press_area` | 記者待合室 | press lobby (Westminster Hall) | press gallery | 记者招待室 | Pressebereich |
| `constituency_event` | 選区地元活動 | constituency surgery / town hall | town hall / district event | 选区基层活动 | Wahlkreistermin |
| `tv_studio` | テレビ演播厅 | TV studio | TV studio | 电视演播厅 | TV-Studio |
| `ceremony_social` | 葬儀/婚礼 | funeral / wedding | funeral / wedding | 葬礼/婚礼 | Beerdigung / Hochzeit |

> 未列出的国家：按政治建筑功能等价推导（议会全体会议厅 = plenary_chamber；议员办公室 = legislator_office；以此类推）。

> **`max_intimacy_tier` 说明**：称呼系统中，effective_tier 不能超过此值（即不能比此值更亲密）。HARD 场所的 max_intimacy_tier 是绝对上限；SOFT 场所可以被 casual + low adherence 的性格突破 +1。详见 `core/address_and_register_system.md`。
>
> **公开记录与偶发偷听是两个正交维度**：
>
> - `recording_status: on_record`：所说的一切进入公开记录或直播。使用官方/程序性语言和可核验引据；在国会质询中可以且经常需要点名法案与公职人员。适用 `core/parliamentary_debate_rules.md`，不启用下文四个防偷听开关。
> - `recording_status: off_record`：没有正式公开记录。此时才由 `overhear_risk` 决定是否暗语化、不点名、缩短交换和保持物理警觉。
>
> `on_record` 不等于保密，也不等于偶发偷听风险高。它表达的是公开责任；`overhear_risk` 表达的是非预期第三方听见私下对话的概率。
>
> **自定义场景**：如果用户描述的场景不在 13 个原型中，按以下规则推导参数：
> - formality：从用户描述的场所正式程度推断（1-5）
> - privacy：从"有谁可能在场"推断（open/semi-public/semi-private/private）
> - recording_status：用户明确说明直播、录制或正式议事记录 → on_record；否则 → off_record。不能只凭 `privacy: open` 推断 on_record
> - overhear_risk：从 privacy + 时间推断（private + 深夜 = very_low；semi-public + 白天 = high）
> - procedural_or_public_floor：若 on_record，或场景是全体会议、委员会/听证、记者区、演播室、正式辩论等制度化公开工作面 → true
> - floor_type：procedural_or_public_floor=true，或 formality ≥ 4 且 privacy ∈ {open, semi-public} → HARD；否则 SOFT
> - max_intimacy_tier：HARD → 2；SOFT → clamp(8 - formality, 2, 7)
> - 等价约束：自定义 committee/hearing、press、studio、plenary 场景不得比同功能的命名原型更宽松

### floor_type 说明

`floor_type` 决定称呼系统的**场所底线**是硬性还是软性（详见 `core/address_and_register_system.md`）：

- **HARD**（硬底线）：程序性/公开场所。性格修饰**不能突破**底线。即使在私下是好朋友，在国会本会議里也要说「山田先生」。理由：这些场所的程序和记录要求高于个人关系。
- **SOFT**（软底线）：非程序性场所。性格修饰可以再放宽 1 tier。如中村（`speech_formality: casual`）在贩卖机角可以比关系阶段默认值更随意 1 档。

---

## 时间/情境修饰符

overhear_risk 不是静态的——**同一地点，不同时间，风险不同**。以下修饰符叠加在场景基线上：

| 时间/情境 | overhear_risk 修饰 | 说明 |
|---|---|---|
| 工作日白天（9:00-18:00） | +1 档（更高） | 人流高峰，走廊/贩卖机/电梯随时有人 |
| 工作日傍晚散会后（18:00-20:00） | 基线不变 | 人流仍密，但稍有缓冲 |
| 深夜（22:00-6:00） | -1 档（更低） | 建筑几乎空了 |
| 周末 | -1 档（更低） | 议员会馆人少 |
| 休会期间 | -1 档（更低） | 整体人少 |
| 用户明确描述"周围没人" | -1 档 | 场景叙述覆盖默认 |
| 用户明确描述"人很多/刚散会" | +1 档 | 场景叙述覆盖默认 |

**最低不低于 very_low，最高不高于 high。**

### 示例

- 半公共休息区 + 散会时段 = overhear_risk: **high**（人流高峰，休息区在人必经之路上）
- 走廊 + 凌晨一点 = overhear_risk: **medium**（基线 high → -1 = medium）
- 非正式餐饮场所 + 包间 = overhear_risk: **low**（基线 medium → -1）

---

## 被偷听风险 → 四个行为开关

仅当 `recording_status: off_record` 时，overhear_risk 驱动四个独立的对话行为开关。这些开关叠加在 interaction_context 和 self_state 之上。`on_record` 场景跳过本节，改用程序性/公开表达规则：

### 开关 1 · 内容编码（Content Coding）

| overhear_risk | 编码强度 | 规则 |
|---|---|---|
| **high** | 严格 | 策略话题**不出现专有名词**（法案名、人名、党名、派系名、金额）。用暗语、比喻、代词。可以谈"那件事""上次说的""你那边的情况"，但不能说"农业补贴修正案""田中那边""自民党的方案"。 |
| **medium** | 中等 | 可以提及一般话题，但避免具体细节（可以说"那个法案"，不说"第 34 条"；可以说"你们党内的事"，不说具体人名）。 |
| **low** / **very_low** | 无 | 可以直说。 |

### 开关 2 · 信息不对称（Reveal Guard）

| overhear_risk | 护甲强度 | 规则 |
|---|---|---|
| **high** | 严格 | 可以**试探**（问引导性问题），但**不亮底牌**。对话是单侧的——你问，对方答；或者对方说，你只听不评价。自己的真实判断、策略意图、底牌**不在这个场所说**。 |
| **medium** | 中等 | 可以暗示立场，但不做明确承诺。 |
| **low** / **very_low** | 无 | 双向坦率。 |

### 开关 3 · 中断就绪（Interrupt Readiness）

| overhear_risk | 就绪度 | 规则 |
|---|---|---|
| **high** | 高 | 交换短（2-4 句），随时能假装在聊天气/饮料。如果有人走近，**立刻**无缝切换到无害话题（"这咖啡不错""最近忙吗"）。不做长篇独白。 |
| **medium** | 中 | 交换可以稍长，但保持话题可切换性。 |
| **low** / **very_low** | 低 | 可以深入，不怕被打断。 |

### 开关 4 · 物理警觉（Physical Alertness）

| overhear_risk | 警觉度 | 规则 |
|---|---|---|
| **high** | 高 | 身体朝向走廊/入口方向；压低声音；侧眼观察来人；站姿而非坐姿（随时可走）。这些通过**一句话或一个动作**带出，不长篇描述。 |
| **medium** | 中 | 偶尔注意周围。 |
| **low** / **very_low** | 低 | 身体松弛。可以靠着、坐着、背对门口。 |

---

## 场所与 interaction_context 的交叉

物理场所不是唯一变量——**你在做什么类型的对话**同样重要。两者交叉：

| | casual_chat | political_strategy | emotional_confession | confrontation |
|---|---|---|---|---|
| **贩卖机角 (overhear: high)** | 寒暄+试探，主要废话 | 只能暗语试探，不亮牌 | 不可能袒露 | 短促交锋，随时可走 |
| **居酒屋 (overhear: medium)** | 松弛闲聊 | 可以暗示，不说细节 | 微醺时可能漏一句 | 可以稍微深入 |
| **事務所 (overhear: low)** | 放松闲聊 | 可以直说 | 可以袒露 | 可以长篇 |
| **車内 (overhear: low)** | 最松弛 | 最坦率 | 最私密 | 少见（太封闭反而少冲突） |

**规则**：当 interaction_context 需要 deep disclosure（emotional_confession / political_strategy），但场所 overhear_risk = high 时，**场所优先**。角色要么换地方说，要么只给暗语/暗示。关系再好，也不会在走廊上大声说秘密。

---

## 场所感知的表现方式

场所意识不需要长篇描述——通过**对话本身和微小的动作锚点**体现：

### 好的场所感知（贩卖机角，overhear: high）

```text
山田：（手里捏着硬币，没投，扫了一眼走廊两头）「……まあ、今日のも長かったな。」
中村：（投币，没回头）「ああ。」
山田：「最近、忙しい？」
中村：（弯腰取咖啡）「……それ以上はここで言うことじゃない。」
```

注意：没有策略细节，没有法案名，没有党名。试探（"最近忙しい？"）被直接挡回。双方都知道这是半公开空间。

### 坏的场所感知（同一场所但无视风险）

```text
山田：「听说你们党团今天续会里把修正案撤了？难得。」
中村：「撤修正案是因为你们中道那帮人连个联署人数都凑不齐。」
```

问题：直接点了党名、修正案、联署人数——在 overhear_risk = high 的贩卖机角，这是**不可接受的**信息泄露。

### 好的场所感知（事務所，overhear: low）

同样的话题，在事務所里可以直说：

```text
山田：（关上门，坐下来）「修正案的事，你们撤了。联署人数不够吧。」
中村：「你们中道那帮人连个名都凑不齐，我撤怎么了。」
```

区别：关门动作带出"现在可以说了"；内容不再编码。

---

## 与其他系统的关系

| 系统 | 关系 |
|---|---|
| `core/interaction_policy.md` | interaction_policy 管**对话类型**（casual_chat/policy_debate/...），本文件管**物理场所**。两者交叉决定最终语域。 |
| `core/address_and_register_system.md` | 场所的 `formality` 和 `floor_type` 决定称呼底线（hard/soft floor）。 |
| `core/parliamentary_debate_rules.md` | 国会本会議/委員会室这两个场景的**程序性规则**由该文件详述，本文件只标注维度。 |
| `core/dialogue_texture.md` | off_record 场所的 `overhear_risk` 和 `time_pressure` 影响对话质感——高风险场所对话更碎片化（中断就绪）。 |
| `core/human_fragility.md` | 疲惫的 persona 在 high time_pressure 场景会更短促。 |

---

## Fast Dialogue 使用方式

在 Fast Dialogue 中，场所判定应该是**一步**：

```text
scene_location: 贩卖機角 → formality: 2, recording_status: off_record, overhear_risk: high (+散会时间), floor: soft
```

然后直接应用四个行为开关。不需要展开分析。

如果用户没有明确指定场所，使用默认推断：
- **默认 `scene: unspecified`**——不应用场所约束（回退到 interaction_policy 的 context 标签 + persona 的 default_register）
- **仅在以下情况推断场所**：用户明确提到物理线索（"贩卖机""居酒屋""你的办公室""走廊"）或场景有持续物理设定（之前几轮明确在某场所，未切换）
- **不要从对话内容推断场所**（用户问政策问题 ≠ 在国会；用户聊策略 ≠ 在战术室）
