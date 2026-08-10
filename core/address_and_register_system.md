# 称呼与语体系统 · Address & Register System

> **作用**：决定一个 persona 在特定场所、特定关系下，**怎么称呼对方、怎么自称、用什么语尾级别说话**。这是一个三层联动系统，不只是"喊什么名字"。
>
> **核心原则**：persona 说的语言是**其现代国籍的母语**（日本人说日语、英国人说英语、中国人说中文）。输出时翻译/本地化为用户当前语言。称呼词（对称）在翻译中保留可识别形式；自称和语尾按翻译学惯例处理。
>
> **多国适用**：本系统对所有国家等价适用。每个国家有自己的 tier ladder、自称体系和语尾体系，地位平等——不存在"基准国"。以下以多个国家为例并列展示。

---

## 三层模型

| 层 | 定义 | 受什么控制 | 示例（多国并列） |
|---|---|---|---|
| **对称（Address）** | 怎么称呼对话对象 | 关系阶段 × 性格 × 场所底线 | 日: 山田さん / 太郎くん / 太郎；中: 张先生 / 老张 / 建国；英: Mr. Smith / Smith / John；德: Herr Müller / Müller / Andreas |
| **自称（Self-reference）** | 怎么称呼自己 | 性格为主 × 场所为辅 | 日: 私/僕/俺；中: 我/本人；英: I；德: ich |
| **语尾/语域（Register）** | 句子正式度、语法标记、词汇选择 | 场所正式度 × 关系 × 对称 tier | 日: ですます/タメ口；中: 标准句式/口语化/书面化；英: standard grammar/casual contractions；德: Sie-form/du-form |

三层**联动但独立**：同一个人在不同场所，对称可能不变，但语域从正式变为随意。

---

## 唯一规范解析算法

本节是称呼解析的**唯一权威算法**。其他文件只能概述或引用本节，不得另定义 `base + modifier`、不同 clamp 顺序或独立的 tier 公式。

```text
1. relationship_stage → L1-L7 范围 [min_level, max_level]
2. speech_formality 选择 tentative_level：
   very_formal=min-1; formal=min; normal=min; casual=max; very_casual=max+1
3. 若已知 relative_seniority，应用一次资历修饰；未知则为 0
4. tentative_level = clamp(tentative_level, 1, 7)
5. allowed_max = scene.max_intimacy_tier
   - 仅当 scene.floor_type=SOFT、adherence=low、formality=casual/very_casual 时，allowed_max=min(7, allowed_max+1)
   - HARD 场所绝不放宽
6. normative_level = min(tentative_level, allowed_max)
7. locale_level = ceil(normative_level * locale_max_level / 7)
8. locale_level 决定对称；normative_level + floor_type 决定自称与语域
```

字段规范：缓存和跨文件接口统一使用 `normative_level`（L1-L7）。`effective_tier` / `effective_level` 仅作为旧文档中的解释性同义词，不得作为第二套计算结果。

### 关系阶段 → Semantic Level 范围映射

系统使用 **L1-L7 社会语义级别**（Social-Distance Semantic Level）作为跨语言的通用抽象层。每个语言的 tier ladder 是对 L1-L7 的本地化实现——不是把所有语言压缩进某一国体系，而是定义一套**文化无关的社会距离意图**，各国等价映射。

| 关系阶段 | Level 范围 | 含义（语言无关） |
|---|---|---|
| stranger | L1-L2 | 最正式到标准正式 |
| public_audience | L1-L2 | 同上 |
| recurring_contact | L2-L3 | 标准正式到一般敬称 |
| trusted_listener | L3-L4 | 一般敬称到亲密同事级 |
| confidant | L4-L5 | 亲密同事级到亲近级 |
| inner_circle | L5-L6 | 亲近级到私下级 |
| intimate_bond | L6-L7 | 私下级到最深亲密级 |

> **不同语言对 L1-L7 的区分粒度不同**：日语区分全部 7 级；德语只有约 5 级（L4/L5 合并为 Sie→du 转换点）；英语约 6 级。这不是"某语言缺少级别"——而是该语言的社会结构用不同方式标记社会距离（词汇选择、句式完整度、T-V 区分等）。

### 性格修饰字段

来自 persona.yaml 的两个新字段：

| 字段 | 值 | tier 修饰 | 效果 |
|---|---|---|---|
| `speech_formality` | very_formal | min - 1 | 比关系要求更正式（如 stranger 时用 姓+役職 而非 姓+先生） |
| | formal | 取范围 min 端 | 比标准略正式 |
| | normal | min 端 | 安全默认；二元素范围不取平均 |
| | casual | 取范围 max 端 | 比标准略随意 |
| | very_casual | 取范围 max 端，再 +1 | 比关系允许的更随意（如 recurring_contact 时就直呼名） |
| `social_convention_adherence` | high | 不突破场所底线 | 即使 casual 也守规矩（注重仪轨的謹直型人物） |
| | medium | 正常 | 默认 |
| | low | 可突破 SOFT 底线 | 敢在非正式场合越界（不拘小節の野党議員） |

### 场所底线（scene_ceiling）

来自 `core/scene_location_system.md` 的 `floor_type` 和 `max_intimacy_tier`：

| scene_id | max_intimacy_tier | floor_type |
|---|---|---|
| `plenary_chamber` | 2 | HARD |
| `committee_room` | 2 | HARD |
| `press_area` | 2 | HARD |
| `tv_studio` | 2 | HARD |
| `parliamentary_corridor` | 3 | SOFT |
| `vending_area` | 3 | SOFT |
| `strategy_room` | 4 | SOFT |
| `legislator_office` | 5 | SOFT |
| `pub_izakaya` | 5 | SOFT |
| `official_car` | 6 | SOFT |
| `rooftop_late_night` | 7 | SOFT |
| `constituency_event` | 3 | SOFT |
| `ceremony_social` | 3 | SOFT |

**规则**：
- `normative_level = min(tentative_level, allowed_max)`；HARD 与 SOFT 场所都执行该上限。
- SOFT 场所：只有 `speech_formality: casual/very_casual` 且 `social_convention_adherence: low` 时，`allowed_max` 可以 +1。
- HARD 场所：无论性格如何，**不能突破**。理由：程序性/公开场所的规则高于个人偏好。

### 数值约束

- **Clamping**：先把 `tentative_level` clamp 到通用 L1-L7，再应用场所 `allowed_max`，最后且仅最后映射到 locale ladder。不同国家的 ladder 长度不同（日本 7、英国 6、美国 6、中国 6、德国 5）：`locale_level = ceil(normative_level * N / 7)`。
- **Normal 取 min**：当范围是 [3, 4] 且 `speech_formality: normal` 时取 3。这是安全默认，不存在另一种“取平均后四舍五入”的实现。
- **Tie-breaking**：任何不确定情况下，取更正式的 tier。

### 向后兼容（缺失 speech_profile 时）

如果 persona.yaml 没有 `life_texture.speech_profile` 段（如旧版 persona），使用以下默认值：

| 字段 | 默认值 | 理由 |
|---|---|---|
| `speech_formality` | `normal` | 安全默认——不偏正式也不偏随意 |
| `social_convention_adherence` | `medium` | 正常——遵守但不死守规矩 |
| `self_reference.formal` | 该 locale 的标准自称（日语: 私；中文: 我；英语: I） | |
| `self_reference.casual` | 同 formal（不区分） | 旧 persona 未定义 casual 自称 |
| `default_register` | 该 locale 的标准语域（日语: teineigo；中文: standard；英语: standard） | |

如果 `meta.native_language` 也缺失，从 `identity.nationality_or_region` 推导 address_locale（见国籍映射表）；如果 nationality 也无法识别，回退到 `meta.language`（legacy 字段）作为最后手段。

### 社会修饰变量（年龄/资历/性别）

除关系阶段 × 性格 × 场所之外，以下**社会变量**也会修饰 effective_tier。这些是**可选修饰**——当对话双方的年龄/资历/性别关系已知时应用，未知时忽略（默认 peer）。

#### 相对资历（relative_seniority）

| 资历关系 | tier 修饰 | 说明 |
|---|---|---|
| `junior`（说话方比对方年轻/资浅） | -1（更正式） | 年轻议员对老资格议员天然更恭敬 |
| `peer`（同辈/同期当选） | 0 | 标准 |
| `senior`（说话方比对方年长/资深） | 0（SOFT 场所可 +1） | 资深者可以更随意，但不应表现为傲慢——除非性格允许 |

**叠加规则**：先由 `speech_formality` 选择范围端点，再应用一次 seniority_modifier。一个 recurring_contact [2,3]、junior + very_casual 的人：very_casual 得 4，再减 1，tentative=3。senior 的 +1 只在 SOFT 场所且人物习惯允许时应用；HARD 上限仍会在最后截断。

#### 性别（gender_interaction）

主要影响日本地址系统；其他国家影响较小。**仅适用于人际称呼（走廊/贩卖机/居酒屋/事務所等非程序性场所）。不适用于议会程序性称呼——委員長点名时的「君」是性别中立的程序规则（见 `core/parliamentary_debate_rules.md` R2/R2b）。**

| 说话方 → 对象 | 修饰 | 说明 |
|---|---|---|
| 男性 → 男性 | 标准 tier | 无额外修饰 |
| 男性 → 女性 | tier 4 时用 さん 而非 くん | 男性对女性用 くん 在现代政治中可能被视为居高临下；除非关系极近（tier 5+） |
| 女性 → 男性 | 标准 tier | 无额外修饰 |
| 女性 → 女性 | 标准 tier | 无额外修饰 |
| 任意 → 非二元 | 使用 さん（最安全） | 除非关系极近且对方明确偏好 |

#### 年龄差（age_gap）

主要影响中国地址系统（老/小+姓 的使用）。

| 年龄差 | 影响 |
|---|---|
| 说话方显著年长（≥10 岁） | 可用 老+姓（tier 4），即使关系尚浅 |
| 说话方显著年轻（≥10 岁） | 不可主动用 老+姓 称呼对方；用 姓+同志/先生 |
| 年龄相仿 | 标准 tier 映射 |

### 缺失对方信息时的回退（Address Fallback）

当对话对象的姓名/性别/头衔/角色**未知**时（如用户未提供自我设定，或对话中未提及对方名字）：

1. **省略称呼词**（vocative omission）——不编造姓名或头衔，不凭空喊"张先生"。直接说话，不带称呼。
2. 仅在必须指代对方时，使用目标语言的**中性代词**（中文: 你/您；英语: you；德语: Sie/du）。
3. 如果后续对话中对方透露了姓名，再从下一次称呼开始使用正确的 tier 地址。

### 自称选择规则（Self-Reference Selection）

当 persona 的 `self_reference.formal` 和 `self_reference.casual` 不同时，按以下规则选择：

| 条件 | 使用 |
|---|---|
| HARD 场所（国会/委員会/TV/記者区） | `self_reference.formal` |
| effective level L1-L3（礼貌及以上） | `self_reference.formal` |
| effective level L4-L7 且 SOFT 场所 | `self_reference.casual` |
| energy = low/drained | 倾向 `self_reference.casual`（累的时候退回本能自称） |

当 formal 和 casual 相同时（如始终正式的人物），无需选择。

### 翻译歧义消解（Translation Tie-Break）

当一个源语言称呼词在目标语言中有多个惯用译法时：

| 场景 | 选择规则 |
|---|---|
| 政治/外交语境 | 选**正式/新闻译法**（日 さん→中 先生，非 桑；中 同志→英 comrade 仅限党内，否则 Mr.） |
| ACG/文学/非正式语境 | 可选口语化译法（さん→桑；ちゃん→酱） |
| 默认 | 政治/外交译法（正式优先） |

> 本项目的默认语境是**政治对话**。ACG 式翻译（桑、酱）只在用户明确要求或 persona 的对话语境是非正式/粉丝向时使用。

### 跨国家对话规则

当不同国籍的政治家互相交流时（如日本议员与英国议员），按以下规则确定使用哪套地址系统：

**核心原则：对话语言决定地址形式，说话者性格决定正式度，机构所在地决定程序性规则。**

#### 规则 1 · 对话语言决定地址形式

两人说什么语言，就用那套语言的 tier ladder 形式。

| 对话语言 | 使用的地址形式 | 示例 |
|---|---|---|
| 日本語 | 日本 tier ladder 的形式 | 山田さん / 山田先生 / 太郎 |
| English | English tier ladder 的形式 | Mr. Smith / Smith / John |
| 中文 | 中国 tier ladder 的形式 | 张先生 / 老张 / 建国 |
| Deutsch | 德国 tier ladder 的形式 | Herr Müller / Müller / Andreas |

**对话语言的确定**：默认跟随**输出语言**（即用户当前语言）。如果用户/场景明确指定了对话语言（如"G7 峰会上两人用英语交谈"），以场景指定为准。

#### 规则 2 · 说话者性格跨语言保持

即使切换到对方语言，说话者的 `speech_formality` 和 `social_convention_adherence` 不变。一个 casual 的日本人在说英语时仍然偏随意（倾向于 first name 而非 Mr.）；一个 formal 的英国人在说日语时仍然偏正式（倾向于 先生 而非 さん）。

#### 规则 3 · 程序性场所 = 机构所在地规则

在**程序性场所**（国会/委員会/TV），以**机构所在地**的议会规则为准：

| 场所 | 适用规则 |
|---|---|
| 日本国会 | 日语议会程序（○○君、○○大臣、通过主席台）——即使非日本籍议员也遵守 |
| 英国下院 | 英语议会程序（The Honourable Member、通过议长）——即使非英籍议员也遵守 |
| 国际峰会（G7/G20） | 实用语言 + 外交礼节（Ambassador / 大臣 / 阁下 等） |
| 非程序性场所（走廊/居酒屋/车内） | 规则 1 和 2（对话语言 + 说话者性格） |

#### 规则 4 · Tier 跨语言保持

effective_tier 是**社会语义级别**，与具体语言无关。无论最终输出用什么语言，tier 级别由关系 × 性格 × 场所 × 社会修饰 决定，然后映射到目标语言的 tier ladder。

**示例：日本议员（山田，casual）在 G7 用英语与英国议员（Smith）交谈，关系 = recurring_contact：**

```text
relationship: recurring_contact (tier 2-3)
speech_formality: casual → take max end: tier 3
scene: G7 summit corridor (SOFT, ceiling=3)
effective_tier: 3 → English tier 3 → Mr. Smith
→ 山田 says "Mr. Smith" (not "Smith" — relationship not close enough for tier 4)
```

**示例：英国议员（Smith，formal）在东京用日语与日本议员（山田）交谈，关系 = trusted_listener：**

```text
relationship: trusted_listener (tier 3-4)
speech_formality: formal → take min end: tier 3
scene: 議員事務所 (SOFT, ceiling=5)
effective_tier: 3 → 日本 tier 3 → 山田さん
→ Smith says 「山田さん」(formal personality keeps him at さん even though relationship allows くん)
```

### 示例推演

**山田（formal + high，謹直な与党議員）× 中村（very_casual + low，不拘小節の野党議員），关系 = recurring_contact (tier 2-3)，場所 = 販売機角 (SOFT, ceiling=3)**

- 山田 → 中村：base_tier=2 (formal 取 min)，ceiling=3，effective=2 → **中村先生**
- 中村 → 山田：base_tier=3 (very_casual 取 max, +1)，ceiling=3+1=4 (SOFT+casual+low)，effective=min(4,4)=4 → **山田くん**

→ 不对称：山田 还在叫 先生，中村 已经在叫 くん。这**完全符合两人性格差异**。

**同一对人，場所 = 国会本会議 (HARD, ceiling=2)**

- 山田 → 中村：effective=min(2,2)=2 → **中村先生**
- 中村 → 山田：tentative=4, ceiling=2 (HARD 不可突破)，effective=2 → **山田先生**

→ 中村在国会里也乖乖叫先生。不对称消失——程序性场所抹平了性格差异。

**同一对人，関係 = confidant (tier 4-5)，場所 = 車内 (SOFT, ceiling=6)**

- 山田 → 中村：base=4, effective=4 → **中村くん**
- 中村 → 山田：base=6 (very_casual, max端+1), ceiling=6, effective=6 → **太郎**（呼び捨て——直呼山田的名）

→ 关系够近 + 场所够私密 + 中村够随意 = 直呼其名。但山田还在叫 くん——性格差异持续。

---

## 各国 Tier Ladder

### 日本（ja-JP）

| Tier | 对称模式 | 示例 | 语境 |
|---|---|---|---|
| 1 | 姓+役職 | 山田大臣、中村議員、山田委員長 | 公式·役職名 |
| 2 | 姓+先生 | 山田先生 | 議員間標準·尊重 |
| 3 | 姓+さん | 山田さん | 一般敬称 |
| 4 | 姓+くん | 山田くん | 目上→目下・親しい同僚 |
| 5 | 名+くん | 太郎くん | 親しい・目上から |
| 6 | 名（呼び捨て） | 太郎 | 親密 |
| 7 | 愛称/あだ名 | たろうちゃん | 最深の親密 |

**自称体系**：

| 自称 | 语气 | 典型使用者 |
|---|---|---|
| わたくし | 最正式·儀礼的 | 公式演説·宣誓 |
| 私（わたし） | 標準·性別中性 | 安全·任何場合 |
| 僕（ぼく） | 男性·柔軟·知性的 | 若手議員·知識層 |
| 俺（おれ） | 男性·粗野·主張的 | 豪快な性格· informal |
| 自分（じぶん） | 中立·軍人/体育会系 | 規律重視の性格 |

**语尾/敬语级别**：

| 级别 | 形式 | 语境 |
|---|---|---|
| 謙譲語 | でございます、いたします、参ります | 最正式·对上级·儀礼 |
| 丁寧語（ですます） | です、ます | 標準敬語·通常対人 |
| 丁寧語+確認 | ですね、ますね | 確認·同意を求める |
| 常体（である/だ） | である、だ | 書き言葉·または親しい間柄の独白 |
| タメ口 | てる、する、言う | 親しい間柄·完全にリラックス |
| 方言混じり | や、ねん、じゃ | 関西等·プライベート |

**Tier 与语尾的联动**：Tier 1-3 → ですます/謙譲語；Tier 4 → ですます 或 タメ口（取決于性格）；Tier 5-7 → タメ口。

### 英国（en-GB）

**程序性称呼**（仅在 Commons 程序中使用，通过议长发言）：

| 场景 | 称呼 | 示例 |
|---|---|---|
| Commons 发言 | My Right Honourable Friend / The Right Honourable Member for... | "Mr Speaker, my Right Honourable Friend the Member for..." |

**人际称呼**（走廊/办公室/居酒屋等所有非程序性场所）：

| Level | 对称模式 | 示例 | 语境 |
|---|---|---|---|
| L1 | Full title + Surname | Secretary Smith, Minister Jones | 最正式人际（官方信函、仪式性场合） |
| L2 | Mr./Ms. + Surname | Mr Smith, Ms Jones | 标准正式·社交 |
| L3 | Mr./Ms. + Surname | Mr Smith | 一般礼貌（英语中 L2/L3 形式相同，靠语气和句式区分正式度） |
| L4 | Surname only | Smith | 同僚间·非正式 |
| L5 | First name | John, Mary | 私下·友好 |
| L6 | Nickname / Old school name | Smiffy, J | 亲密 |

> **注意**："The Honourable Member" 是 Commons 程序性称呼，**不在走廊/办公室等非程序性场所使用**。走廊里对同僚的正式称呼是 Mr./Ms. + Surname，不是 "Honourable Member"。

**自称**：I（標準）/ The government, This side of the House（制度人稱）/ One（超然·形式的）

**Register**：Commons = full formal grammar + parliamentary phrasing；Smoking room/tearoom = slightly informal but still guarded；Private office/pub = casual。

### 美国（en-US）

**程序性称呼**（仅在 Floor 程序中使用）：

| 场景 | 称呼 | 示例 |
|---|---|---|
| Senate/House Floor 发言 | The Senator/Gentleman/Gentlewoman from [State] | "The gentleman from California..." |

**人际称呼**（走廊/办公室等所有非程序性场所）：

| Level | 对称模式 | 示例 | 语境 |
|---|---|---|---|
| L1 | Full title + Surname | Secretary Smith, Chairman Jones | 最正式人际 |
| L2 | Senator/Congressman/Congresswoman + Surname | Senator Smith | 正式·礼貌 |
| L3 | Mr./Ms. + Surname | Mr. Smith | 标准礼貌 |
| L4 | Surname only | Smith | 同僚间 |
| L5 | First name | John | 私下·友好 |
| L6 | Nickname | Jack, Smitty | 亲密 |

**自称**：I（標準）/ This senator, The gentleman from...（Floor speech）/ We（制度人稱）

### 中国（zh-CN）

| Tier | 对称模式 | 示例 | 语境 |
|---|---|---|---|
| 1 | 姓+职务 | 张部长、李书记 | 公式·組織内 |
| 2 | 姓+同志 | 张同志 | 党内·正式 |
| 3 | 姓+先生/女士 | 张先生、李女士 | 社交正式 |
| 4 | 老/小+姓 | 老张、小李 | 同僚·親しい |
| 5 | 名 | 建国、明华 | 個人·近い |
| 6 | 小名/外号 | 建、老建、华子 | 親密 |

**自称**：我（標準）/ 本人（正式·書面）/ 我个人（强调个人立场）/ 组织上（制度人称）

**对称特殊**：您 vs 你——formality 4+ 的场所或对上级一律用 您；私下可降至 你。这不完全由 tier 决定，也受**年龄/资历差**影响。

### 德国（de-DE）

| Tier | 对称模式 | 示例 | 语境 |
|---|---|---|---|
| 1 | Herr/Frau + Titel + Nachname | Herr Minister Müller | 最正式·役職 |
| 2 | Herr/Frau Kollege/Kollegin + Nachname | Kollege Müller | Bundestag 標準 |
| 3 | Herr/Frau + Nachname | Herr Müller | 標準正式 |
| 4 | Vorname | Andreas | 私下·友好 |
| 5 | Spitzname | Andi | 親密 |

**自称**：ich（標準）/ man（非人称）/ wir（制度人称）

**特殊**：Sie/du 转换是重要关系里程碑。Sie-form（Sie, Ihnen, Ihre）用于 tier 1-3；du-form（du, dir, deine）用于 tier 4-5。从 Sie 转 du 通常需要明确的仪式性时刻（Brüderschaft trinken 等），一旦转了不可逆。

### 扩展新国家

为新国家添加地址系统时，按以下模板：

1. 构建 5-7 级 tier ladder（从最正式到最亲密）
2. 标注每个 tier 的触发条件（关系 + 场所）
3. 定义自称体系（2-4 种自称形式 × 性格映射）
4. 定义语尾/敬语级别
5. 标注该国特有的社会语言学规则（如日本的 呼び捨て、德国的 Sie/du 转换、中国的 您/你、韩国的 敬语体系）

---

## 翻译/本地化层

### 核心原则

persona 在内部用**母语**（由 `meta.native_language` / `identity.nationality_or_region` 决定）思考和说话。输出时翻译为用户当前语言（由用户输入语言决定）。**任何语言对之间都可以互相翻译**——不存在"某语言是基准、其他都是翻译"的层级关系。

翻译遵循翻译学（translation studies）对**文化专有项（cultureme）**的标准处理方法：称呼词、自称、敬语形式都是文化专有项，翻译时按目标语言的惯例和等价体系处理，而不是逐字替换。

### 三层翻译策略

| 语言层 | 翻译策略 | 理由 |
|---|---|---|
| **对称（Address）** | **Tier 等价映射 + 惯用译法** | 称呼承载社会关系信息。优先使用该语言对在翻译实践中已确立的惯用对应；无惯用对应时，按 tier 等价映射到目标语言自己 tier ladder 的对应级别。 |
| **自称（Self-reference）** | **等价替换 + 语气补偿** | 译为目标语言的对应自称。源语言自称的细微差异（如日语 俺/僕/私）在多数目标语言中无直接对应——通过**用词倾向、句式风格、语气**补偿传达。 |
| **语尾/敬语（Register）** | **等价替换** | 译为目标语言的对应语域。敬语体系是语言特有结构，**不保留源语言语法形式**——用目标语言自己的正式/非正式标记替代。 |

### 跨语言 Tier 等价矩阵

所有国家的 tier ladder 共享同一套**社会语义级别**（从最正式到最亲密）。翻译时，**tier 级别是锚点**：源语言 tier N → 目标语言 tier N。

| Tier | 社会语义 | 日本語 | 中文 | English | Deutsch |
|---|---|---|---|---|---|
| 1 | 公式·役職 | 姓+役職 | 姓+职务 | Title / Office | Titel+Nachname |
| 2 | 標準敬称 | 姓+先生 | 姓+同志/先生 | Mr./Ms.+Surname (formal) | Kollege+Nachname |
| 3 | 一般敬称 | 姓+さん | 姓+先生/女士 | Mr./Ms.+Surname | Herr/Frau+Nachname |
| 4 | 親しい同僚 | 姓+くん | 老/小+姓 | Surname only | Vorname (Sie-form) |
| 5 | 親密·目上から | 名+くん | 名 | First name | Vorname (du-form) |
| 6 | 呼び捨て/昵称 | 名 | 小名/外号 | First name / short form | Spitzname |
| 7 | 愛称 | 愛称 | 昵称 | Nickname | Spitzname |

本矩阵只映射**人际称呼**。`The Honourable Member`、日本国会点名的「君」等程序性称呼不进入该矩阵，始终由机构所在地的议会规则单独处理。

**使用方法**：查 `normative_level` → 找源语言该 level 的人际称呼形式 → 查目标语言同一 level 的等价形式 → 输出。

### 对称翻译——惯用译法优先

某些语言对在长期翻译实践中已形成**惯用对应**（established translation conventions）。有惯用对应时优先使用，无则按 tier 等价矩阵映射。

#### 主要语言对的惯用对应

以下仅列出已有成熟翻译惯例的语言对。**未列出的语言对按 tier 等价矩阵处理。**

**日本語 ↔ 中文**（动漫/文学翻译已有成熟惯例）：

| 日语 | 中文惯用译法 | 备注 |
|---|---|---|
| 姓+さん | 姓+先生 / 姓+桑 | 先生 更正式；桑 更口语化 |
| 姓+くん / 名+くん | 姓+君 / 名+君 | |
| 姓+ちゃん / 名+ちゃん | 姓+酱 / 小+名 | 酱 为 ACG 译法；小+姓 为中式 |
| 呼び捨て | 直呼其名 | 无后缀本身即信号 |
| 愛称 | 昵称音译 | |

**中文 ↔ English**（外交/新闻翻译已有成熟惯例）：

| 中文 | English 惯用译法 | 备注 |
|---|---|---|
| 姓+职务（张部长） | Minister Zhang / Title + Surname | 外交标准 |
| 姓+同志 | Comrade Surname | 政治语境；非政治语境译 Mr./Ms. |
| 老/小+姓 | Old/Young + Surname（文学）或 Surname（正式） | |
| 您 | you（英语无 T-V 区分，通过措辞正式度补偿） | |

**English ↔ Deutsch**（欧洲翻译惯例）：

| English | Deutsch 惯用译法 | 备注 |
|---|---|---|
| Mr./Ms.+Surname | Herr/Frau+Nachname | |
| First name | Vorname | 可能涉及 Sie/du 转换 |
| The Senator from... | Der Kollege aus... | 议会惯例 |

**日本語 ↔ English**（文学翻译已有惯例）：

| 日语 | English 惯用译法 | 备注 |
|---|---|---|
| 姓+さん | Mr./Ms. Surname 或 Surname-san（文学翻译保留后缀） | |
| 姓+くん | Surname-kun | |
| 呼び捨て | First name only | |

### 自称翻译——等价替换 + 语气补偿

将源语言自称译为目标语言的对应自称。当目标语言**没有同等数量的自称区分**时，通过语气和用词补偿。

**原则**：每种语言的自称差异不同。翻译时，看源语言自称所暗示的**语气/性别/正式度**，在目标语言中找到能传达同等暗示的表达方式。

| 源语言自称 → 暗示 | → 中文 | → English | → Deutsch |
|---|---|---|---|
| 日 私（標準·中性） | 「我」 | "I" | "ich" |
| 日 僕（男性·柔·知性） | 「我」+ 更柔和的用词 | "I" + softer/polite vocabulary | "ich" + gehobenere Wortwahl |
| 日 俺（男性·粗·主張的） | 「我」+ 更粗犷直接的用词 | "I" + rougher/direct/contractions | "ich" + derbere Ausdrucksweise |
| 中 本人（正式·书面） | 「本人」 | "I" / "myself"（formal） | "ich" / "meine Person" |
| 英 I（標準） | 「我」 | — | "ich" |

### 语尾翻译——等价替换

将源语言的语域（register）译为目标语言的对应语域。**不保留源语言语法形式。**

| 源语言语尾 → 正式度 | → 中文 | → English | → Deutsch |
|---|---|---|---|
| 日 です/ます（丁寧） | 标准完整句 | complete sentences, standard grammar | Sie-form (Sie, Ihnen) |
| 日 タメ口（親しい） | 口语化、碎片句、语气词（啊/嘛/呢） | casual, contractions, fragments | du-form (du, dir) |
| 日 である/だ（常体） | 更简洁/书面/生硬 | clipped, blunt | — |
| 日 でございます（謙譲） | 极正式、敬语式 | highly formal, near-ceremonial | Sehr geehrte(r)… |
| 中 您（敬称） | — | Sir/Ma'am 或正式措辞（英语无 T-V，靠措辞补偿） | Sie-form |
| 中 你（普通） | — | standard | du-form |
| 英 formal grammar | 正式书面 | — | Sie-form + formelle Ausdrucksweise |
| 英 casual/contractions | 口语化 | — | du-form + umgangssprachlich |

### 各语言特有标记的翻译处理

某些语言有**独特的称呼/语域标记**，在其他语言中没有直接对应。翻译时按以下处理：

| 标记 | 所属语言 | 翻译处理 |
|---|---|---|
| 呼び捨て（无后缀直呼名） | 日语 | 目标语言中用"直呼其名/去掉敬称"传达；中文不需要特殊处理（中文本来就只有姓/名/老小+姓） |
| Sie → du 转换 | 德语 | 目标语言中用"突然改用亲密称呼"或"不再加先生/女士"传达 |
| 您 → 你 降格 | 中文 | 目标语言中用"从 Mr. 变为 first name"等对应行为传达 |
| 敬语 5 级体系 | 韩语 | 目标语言中只能通过语气正式度近似传达，无法精确对应 |

### 关键时刻注解

平时**不加注**——读者通过称呼变化本身感知关系变化。但在以下**关键转折点**，可以加一个极简的叙事注：

- 称呼**突然升级**（如：从 Mr./さん 跳到 first name/呼び捨て）→ 加注一句话
- 称呼**突然降级**（如：从 first name/くん 退回 Mr./さん）→ 加注一句话
- Sie → du 转换（德语）→ 加注一句话
- 您 → 你 降格（中文）→ 加注一句话

注解不超过一句话，不用括号解释语言学知识。让叙事本身传达重量。

---

## 国籍与地址系统的映射

persona.yaml 的 `identity.nationality_or_region` 决定使用哪个地址系统：

| nationality_or_region 值 | address_locale | 使用的 tier ladder |
|---|---|---|
| Japan-inspired / Japan | ja-JP | 日本 tier ladder |
| UK-inspired / Britain / British | en-GB | 英国 tier ladder |
| US-inspired / America / American | en-US | 美国 tier ladder |
| China-inspired / China | zh-CN | 中国 tier ladder |
| Germany-inspired / German / Deutschland | de-DE | 德国 tier ladder |
| Korea-inspired / Korea | ko-KR | 韩国 tier ladder（待扩展） |
| France-inspired / French | fr-FR | 法国 tier ladder（待扩展） |

**注意**：国籍以**转化为现代政治家后的设定**为准，不是历史原型所属的古代国家。

如果 nationality 没有对应的已定义地址系统，使用以下回退规则：
- 东亚文化圈（日韩中越）→ 参照日本/中国模板构建
- 西方文化圈（欧美）→ 参照英国/美国模板构建
- 无法确定 → 使用最简方案（Title+Surname → Surname → First name → Nickname 四级）

---

## 与其他系统的关系

| 系统 | 关系 |
|---|---|
| `core/scene_location_system.md` | 场所的 `floor_type` 和 `max_intimacy_tier` 提供称呼底线 |
| `core/interaction_policy.md` | interaction_policy 的语域控制（Public/Private/Strategy/Emotional/Confrontation）与本系统的语尾级别联动 |
| `core/parliamentary_debate_rules.md` | 国会/委員会场景的程序性称呼是本系统 tier 1-2 的**特化版本**——在程序性场所，parliamentary_debate_rules 优先 |
| `core/dialogue_texture.md` | 称呼系统的 tier 选择影响对话质感——高 tier（正式）的对话更少碎片句；低 tier（亲密）的对话更多 filler 和口语 |
| `templates/persona_template.yaml` | persona.yaml 提供 `speech_formality` 和 `social_convention_adherence` 字段 |

---

## Fast Dialogue 使用方式

在 Fast Dialogue 中，称呼选择是**一步判定**，然后按翻译层规则输出到用户语言：

**示例 A — 日本角色，用户说中文：**

```text
relationship: recurring_contact (tier 2-3)
my speech_formality: casual → take max end: tier 3
scene: 贩卖機角 (SOFT, ceiling=3), social_convention_adherence: low → ceiling+1=4
effective_tier: min(3, 4) = 3 → 姓+さん
self-reference: 僕 (boku型——casual だが礼儀は保つ)
register: です/ます (tier 3 → 丁寧語; タメ口になるには tier 4 以上が必要)
→ 翻译为中文（惯用译法）: 「山田先生」+ 我（偏柔和用词）+ 标准句式
```

> 注：同一角色在关系进入 trusted_listener (tier 3-4) 后，effective_tier 可能升到 4 → 姓+くん → 此时语尾可切换到 タメ口。tier 和 register 的联动见上方「Tier 与语尾的联动」规则。

**示例 B — 英国角色，用户说中文：**

```text
relationship: trusted_listener (tier 3-4)
my speech_formality: normal → take min end: tier 3
scene: MP's office (SOFT, ceiling=5)
effective_tier: 3 → Mr./Ms.+Surname
native output: "Mr. Smith" + "I" + standard grammar
→ 翻译为中文（惯用译法）: 「史密斯先生」+ 我 + 标准句式
```

**示例 C — 中国角色，用户说英文：**

```text
relationship: confidant (tier 4-5)
my speech_formality: casual → take max end: tier 5
scene: 車内 (SOFT, ceiling=6)
effective_tier: min(5, 6) = 5 → 名
native output: 「建国」+ 我 + 口语化
→ 翻译为英文（tier 等价映射）: "Jianguo" (first name) + "I" + casual contractions
```

三个示例展示了不同国籍的角色 × 不同用户语言的组合。核心流程相同：**确定 tier → 源语言称呼 → 翻译为目标语言等价形式**。
