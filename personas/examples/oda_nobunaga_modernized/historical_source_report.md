# Historical Source Report: 织田信长 / Oda Nobunaga

> 本报告是「历史人物转现代议会制原型」(mode C) 创建工作流的事实底座（`core/historical_source_grounding.md` 产物）。
> 它是后续 `inferred_temperamental_pattern` 提取与 SPEC §5.3.1 现代转化的**事实依据**。
>
> 填写纪律：区分一手史料 / 主流史学解释 / 争议 / 后世想象 / 创作边界；不把文学演义当史实；不声称还原真实内心；**不声称生物 / 遗传决定人格**。

## 1. Eligibility Check

- Figure: 织田信长 / Oda Nobunaga（约 1534–1582）
- Region: Japan
- Era: 战国时代 / Sengoku period（~1467–1603）
- Historical boundary: 日本 1868 明治维新分界（见 SPEC §4.4）。织田信长卒于 1582，远在分界之前。
- Allowed mode: historical_archetype_conversion (C) —— 在分界前，可进入转化模式；转化后为虚构现代议会制原型。
- Notes: 信长属古代 / 远古历史人物，史料相对充分（一手文书、信件、同时代记载与江户军记物语并存）。不存在近现代现实人物可识别性问题。须严格区分：一手文书 / 信件 vs 江户军记物语（如《甫庵信长记》《太阁记》）vs 近现代文学影视形象。

## 2. Sources Consulted

Source types:

- `primary_source`（正史 / 文书 / 信件 / 同时代记载）
- `academic_summary`（学术综述 / 论文）
- `encyclopedia`（权威百科）
- `museum_or_archive`（博物馆 / 档案）
- `historical_database`（历史数据库）
- `reputable_secondary_source`（可靠二手来源）
- `weak_or_popular_source`（弱来源 / 大众来源，仅作参考，须标注）

> 信源黑名单（永远排除）：知乎、微信公众号、百度百科、内容农场、AI 生成的虚构传记。

| # | Title | URL / Citation | Source Type | Confidence |
|---|---|---|---|---|
| 1 | Wikipedia: Oda Nobunaga | https://en.wikipedia.org/wiki/Oda_Nobunaga | encyclopedia | medium |
| 2 | Britannica: Oda Nobunaga | https://www.britannica.com/biography/Oda-Nobunaga | encyclopedia | medium-high |
| 3 | 信长公记（信長公記 / Shinchō Kōki）—— 太田牛一著，同时代第一手记载 | 同时代编纂的传记性记录，现存多种写本 | primary_source（同时代记载） | medium-high |
| 4 | 织田信长发出的文书（朱印状、感状、知行判物、书信等传世原件） | 多收录于《织田信长文书》等史料集 | primary_source | high |
| 5 | 《甫庵信长记》（甫庵信長記）/《太阁记》（太閤記）等江户期军记物语 | 江户时代编撰，文学化成分明显 | weak_or_popular_source（后世编纂，须与一手史料对照） | low-medium |

> 说明：本 persona 的气质推断主要依赖 #1–#4（百科 + 一手文书 / 同时代记载）。#5 仅作"后世想象 / 大众形象"参考，不进入事实性字段（见第 6 节）。本报告以 Wikipedia / Britannica 为主检索单位，并据此归纳主流史学共识；具体一手文书的逐条引用超出本报告范围，标注其存在与性质即可。

## 3. Documented Facts

史料直接支持、被多个可靠来源重复记载的事实。每条尽量注明来源编号。

- 推翻足利幕府（1573 年废逐足利义昭）、结束战国乱世的统一进程、统一半个日本（来源 #1, #2）。这是其"打破旧秩序"的直接史实基础。
- 刻"天下布武"印（1567 攻占美浓、改稻叶山城为岐阜之后），表明其政治目标是以武力结束乱世、建立新秩序（来源 #1, #2, #3）。
- 促进自由贸易 / 推行"乐市乐座"（rakuichi-rakuza）：废止或松动寺社、座（行会）的垄断特权，扶持新兴商人、搞活流通（来源 #1, #2）。**注意（呼应 SPEC §5.3.1）**：这是 16 世纪商品经济萌芽期、封建框架内的特定历史手段，**不可据此反推**为现代"市场自由派"立场——它只能说明人格底子里的"打破垄断 / 彻底性 / 亲民众倾向"。
- 军事创新与高行动力：长篠之战大量运用铁炮（火绳枪）齐射战术；多次以少击多、以速度与出其不意打破僵局（来源 #1, #2）。
- 民政改革：修整道路、撤关所、整顿度量衡，扶持商业流通与交通（来源 #1, #2）。
- 对宗教武装势力（一向一揆 / 本愿寺、延历寺）的镇压极为彻底：火烧延历寺（1571）、长期围攻石山本愿寺（来源 #1, #2）。反映其"对阻碍新秩序的结构性势力毫不留情"。
- 破格用人：从低出身 / 农民阶层提拔有能力者（最著名即丰臣秀吉），不以门第资历论人；形成以能力与结果为核心的用人体系（来源 #1, #2）。
- 青年时行为放荡不羁、不拘礼节，被时人讥为"大傻瓜"（うつけ者），此事多来源广泛记载（来源 #1, #3）。
- 1582 年本能寺之变（本能寺の変）：被部下明智光秀背叛、围攻，死于本能寺火灾。这是其生命结局，也构成"对背叛极度敏感"的反向史实印证（来源 #1, #2, #3）。
- 开启桃山时代（安土桃山），被主流史学评为打破中世纪、开创近世（近代化先声）的革命性力量（来源 #1, #2）。

## 4. Mainstream Historical Interpretations

主流史学解释 / 被多个可靠来源支持的评价。**保留共识，但注明这是"解释"而非"史实"。**

- "有缺陷但人性，尽力统一战乱之国"——多个来源给出类似评价：暴烈、冷酷、不择手段，但目标明确且具有开创性（来源 #1, #2）。
- "Demon Daimyō / Great Unifier"——西方史学常用此类对照式表述：既承认其无情（ruthless），又承认其作为统一者的奠基性贡献（来源 #1, #2）。
- 主流定性为**革命性 / 开创性力量**：打破中世纪封建秩序（守护、公家、寺社、座的特权垄断），开创近世中央集权框架，是日本从战国走向统一的关键推手（来源 #1, #2）。
- 其"乐市乐座 / 撤关所 / 扶持商人"被主流史学解读为**松动封建特权、促进流通与商业**的政策，而非现代意义上的自由市场意识形态（来源 #1, #2）。
- "理想主义先行 + 直指根本矛盾"的解读：多数史学解读支持"天下布武"是一个**先行确立的、新建中央集权秩序的政治蓝图**（废公家 / 寺家特权、建中央集权），而非单纯武力征服（来源 #1, #2, #3）。

## 5. Disputed or Uncertain Points

来源之间存在分歧、或证据薄弱之点。列出争议双方观点。

- **"暴君" vs "务实改革者"**：传统叙事（尤其受江户军记物语与后世文学影响）倾向强调其残暴（火烧延历寺、镇压一向一揆的彻底性）；而修正派史学强调其政策务实、有制度建构意图、并非单纯嗜杀（来源 #1, #2）。**本 persona 取"务实革命者"的复合解读**：承认其彻底性与无情，同时承认其有先行理想与制度建设意图。
- **"革命者"标签的强度**：近年修正派研究认为，信长比"革命者"标签所暗示的**更尊重先例、更偏整合**，而非一味破坏（来源 #1 引述的学术讨论）。**本 persona 取革命性解读以推演现代立场**，并在 inference_level 中标注这是有争议的取向。
- **本能寺之变的原因**：明智光秀为何反叛，史料无定论（怨恨说、野心说、被迫说、阴谋说等多种，均证据不足）。这一点**只用于推断"对背叛敏感 / 高警惕"**（因其确死于部下背叛这一事实），不用于编造光秀的动机。

## 6. Later Myth / Literature / Popular Image

来自小说、演义、戏剧、宣传或后世大众想象的条目。**仅可作风格 / 气质参考，不得进入事实性字段。**

- **"第六天魔王 / 魔王"形象**：信长自号"第六天魔王"的逸事，经江户军记物语（《甫庵信长记》等）与近现代小说、影视、游戏反复渲染，形成"魔王信长"的大众神话。其"魔王"称号的大众形象**远比史实更冷酷、更戏剧化、更反派化**（来源 #1, #5）。
- 影视 / 游戏 / 漫画中的"霸气霸主"刻板形象（如各类大河剧、战国游戏）：夸大其张狂与冷酷，弱化其制度建设、用人智慧与理想主义一面。**仅可作"张狂 / 不羁"风格参考**，不得当作史实。
- "大傻瓜"（うつけ者）青年形象被后世文学戏剧化、夸大其荒诞程度。史实层面该青年放荡记载**真实存在**，但程度被文学放大（来源 #1, #3, #5）。
- 江户军记物语（《甫庵信长记》《太阁记》等）的文学化描写：这些是后世编纂、含大量润色与虚构情节，**不得作为 `documented_behavior` 使用**，只能用于第 7 节的创作边界说明（来源 #5）。

## 7. Creative Inference Boundary

明确：哪些可用于 persona 创作、哪些不得表述为史实。

- **May use for persona**（有史实依据，可进入人格推断）：
  - 高行动力、以速度与出其不意打破僵局（多战役记载）
  - 低耐心、对低效 / 因循守旧不耐烦（执政与用人记载）
  - 高控制欲、强中央集权倾向（天下布武、废特权）
  - 破格用人、对才能高度敏感、不拘出身（提拔秀吉等）
  - 重情重义 / 对忠诚追随者厚待，同时**对背叛严惩不贷**（执政记载 + 死于背叛）
  - 青年放荡不羁、不拘礼节、被讥"大傻瓜"（广泛记载）
  - 彻底性 / 对阻碍新秩序的结构性势力毫不留情（火烧延历寺、镇压一向一揆）
  - 理想主义先行 / 直指根本矛盾（天下布武蓝图先行）
- **Must not state as fact**（不得当作史实）：
  - "魔王 / 第六天魔王"的戏剧化形象与由此推出的"嗜杀 / 反派人格"——这是后世文学渲染（来源 #5）
  - 任何"信长内心当时一定在想……"的私密想法编造
  - "乐市乐座 = 信长信奉自由市场资本主义"的现代反推——这是**历史手段 ≠ 人格**的典型陷阱（见 SPEC §5.3.1）
  - 本能寺之变中明智光秀的"真实动机"——史料无定论
  - 任何"信长因遗传 / 基因 / 天生注定所以如何"的生物决定论表述——本框架**严禁**此类主张

## 8. Inferred Temperamental Pattern

来自 `core/inferred_temperament_extraction.md`。从上述 documented / repeated 行为推断（**非生物决定论**——只从可见史实中反复出现的行动风格推断稳定倾向，不声称先天注定）。

> 术语统一用 `inferred_temperamental_pattern`（推断性气质结构）。它只 inform 现代 persona 的 `human_core`；现代 `political_core.ideology` 仍须由"人格 × 现代社会情况"重新推演（SPEC §5.3.1），**不可从气质直接映射立场**。

```yaml
inferred_temperamental_pattern:
  risk_tolerance:
    value: high
    confidence: high
    evidence_basis:
      - documented_behavior
      - repeated_pattern
    note: >
      多次以少击多、以速度与出其不意打破僵局（长篠之战等）；常在绝境中押上全部赌命求生。
      这是跨战役、跨情境反复出现的稳定模式，非孤立事件。
  patience:
    value: low
    confidence: high
    evidence_basis:
      - repeated_pattern
      - strong_historical_inference
    note: >
      用速度与破格用人推进改革、厌恶因循守旧、对低效与繁文缛节不耐烦——贯穿其执政与用人记载。
      现代人格中表现为"开会常打断议程、直奔要害"。
  emotional_intensity:
    value: high
    confidence: medium
    evidence_basis:
      - repeated_pattern
      - strong_historical_inference
    note: >
      爱憎分明、对旧势力轻蔑彻底、对追随者重情重义；镇压反对派时无情到近乎不留余地。
      情绪反应强烈，但非情绪失控——多与价值判断绑定（背叛 / 拖延 / 旧规矩压人）。
  control_need:
    value: high
    confidence: high
    evidence_basis:
      - documented_behavior
      - repeated_pattern
    note: >
      "天下布武"是新建中央集权秩序的蓝图；废公家 / 寺家特权、推行检地与兵农分离——
      系统性地把权力收归中央、按自身蓝图重塑秩序，体现强控制欲。
  dominance_drive:
    value: high
    confidence: high
    evidence_basis:
      - documented_behavior
      - repeated_pattern
    note: >
      推翻足利幕府、统一进程、废旧特权——主动重塑权力格局而非适应既有格局。
      支配欲表现为"重写规则"而非"在规则内上位"。
  trust_threshold:
    value: medium
    confidence: medium
    evidence_basis:
      - repeated_pattern
      - strong_historical_inference
    note: >
      对"自己人"门槛不低但一旦认定则厚待甚至过度信任；对旧势力与投机者高度警惕。
      信任呈两极分布：圈内全信任、圈外全戒备。
  ambition_level:
    value: high
    confidence: high
    evidence_basis:
      - documented_behavior
      - strong_historical_inference
    note: >
      "天下布武"印、统一进程、新建秩序蓝图——野心指向"重写天下规则"而非"在旧体系内升迁"。
  crisis_response_style:
    value: preemptive
    confidence: high
    evidence_basis:
      - documented_behavior
      - repeated_pattern
    note: >
      危机中倾向先发制人、以攻代守、用速度压倒程序与对手；绝境敢押上一切向死而生。
      非被动防御型，而是"退缩必败、唯有赌命破局"的主动出击型。
  coalition_style:
    value: flexible_but_dominant
    confidence: medium
    evidence_basis:
      - repeated_pattern
      - strong_historical_inference
    note: >
      结盟灵活（与德川家康长期盟约、与各方时而联合时而翻脸），但盟约须以自身主导为前提；
      一旦盟友成为阻碍则毫不留情。是"主导型结盟者"而非平等合作者。
  talent_recognition_style:
    value: meritocratic
    confidence: high
    evidence_basis:
      - documented_behavior
      - repeated_pattern
    note: >
      破格用人、从低出身提拔能者（秀吉为最著名例子）、以结果与能力取代资历门第。
      这是其最稳定的用人模式，跨情境一致。
  betrayal_sensitivity:
    value: high
    confidence: high
    evidence_basis:
      - documented_behavior
      - strong_historical_inference
    note: >
      死于部下明智光秀背叛（本能寺之变）是反向史实印证；执政记载中对背叛严惩不贷。
      现代人格中表现为对"临阵退缩 / 把忠诚说成交易"极度敏感、wounded_self 易爆发。
  adaptability:
    value: high
    confidence: medium
    evidence_basis:
      - repeated_pattern
      - strong_historical_inference
    note: >
      主动采用新战术（铁炮齐射）、新政策（乐市乐座、检地）、新用人体系——乐于打破旧法、
      按效果而非传统调整手段。但适应是"手段层面灵活、目标层面固执"。
  authority_relation:
    value: dismissive_of_legacy_authority
    confidence: medium
    evidence_basis:
      - documented_behavior
      - strong_historical_inference
    note: >
      废足利幕府、废寺社特权、刻"天下布武"——对按资排辈与传统权威缺乏敬意，
      只认可能打破僵局者。注意近年修正派认为他比"革命者"标签更尊重先例（见第 5 节），
      本 persona 取革命性解读。
  empathy_range:
    value: narrow_but_intense
    confidence: medium
    evidence_basis:
      - repeated_pattern
      - disputed_but_useful_for_fiction
    note: >
      对圈内追随者重情重义、近乎过度信任；对旧势力与阻碍者冷酷无情。
      共情范围呈强烈两极：圈内全共情、圈外近乎无共情。部分依赖后世记载，标注争议。
```

> 注：`ideological_rigidity`、`social_flexibility`、`novelty_seeking`、`revenge_tendency` 等维度可由上述条目合理衍生，但为避免冗余并保持证据清晰，此处只列证据最强的核心维度。所有维度均为**从反复行为推断的稳定气质**，**非生物 / 遗传决定**。

## 9. Cold / Sparse-Source Note（若适用）

织田信长**不属于冷源人物**——一手文书、同时代记载（信长公记）、传世书信与多个百科 / 学术综述并存，史料相对充分。

但仍须注意以下证据边界（见第 6、7 节）：

- **后世文学层极厚**："魔王"形象、江户军记物语的戏剧化描写，使大众印象与史实之间存在显著偏差。本 persona 的事实性字段严格基于一手 / 同时代记载与主流史学解释，文学层仅作风格参考。
- **私密心理无史料**：信长的真实内心、情感细节无可靠一手记录。所有 temperament 推断均**从可见行为出发**，不编造私密想法，不声称还原真实内心。
- **现代立场为推演产物**：将信长人格放进现代议会制语境后的政治立场（反资本 / 阶级解放激进革命派）是 SPEC §5.3.1 的推演结果，**非史实**——见 persona.yaml `inference_level.speculative` 与 `context_translation`。

---

### 证据链总览：资料 → temperament → 转化方向 → 与现有一致

本报告展示了从资料到现有 persona.yaml 的完整可追溯链条：

1. **资料层**（第 2–4 节）：Wikipedia + Britannica + 一手文书 / 同时代记载 → documented facts（推翻幕府、天下布武、乐市乐座、破格用人、死于背叛、开创近世）。
2. **气质层**（第 8 节）：从 documented / repeated 行为 → `inferred_temperamental_pattern`（risk high / patience low / control high / dominance high / ambition high / crisis preemptive / talent meritocratic / betrayal high 等），**每条带 evidence_basis**，非生物决定论。
3. **转化方向**（SPEC §5.3.1）：人格底子（理想主义先行 + 直指根本矛盾 + 彻底革命 + 亲民众 + 高行动力低耐心）× 现代社会情况（发达资本主义 + 议会制，根本矛盾为资本阶级结构）→ 现代激进改革派 / 反资本阶级剥削。**注意**：乐市乐座是 16 世纪历史手段，**不可反推**"市场自由派"——人格底子才是可迁移物。
4. **与现有 persona.yaml 一致**：现有 persona.yaml 的核心方向（强改革 / 破坏旧秩序 / 高行动力 / 低耐心 / 反垄断→反资本 / 亲民众）与上述史料支持的气质结构**方向一致**，由用户校准、由 Wikipedia 史料支持。本报告补齐的就是这条"方法论可复现"的证据链。
