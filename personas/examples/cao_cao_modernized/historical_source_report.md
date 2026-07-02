# Historical Source Report: 曹操 (Cao Cao)

> 本报告是模式 C（历史人物转现代议会制原型）persona `cao_cao_modernized` 的**事实底座**，由 `core/historical_source_grounding.md` 工作流产出。它是后续 `inferred_temperamental_pattern` 提取与现代转化的依据。
>
> 填写纪律：区分史料 / 主流解释 / 争议 / 后世想象 / 创作边界；不把文学演义当史实；不声称还原真实内心；**不声称生物 / 遗传决定人格**。
>
> 与现有 `persona.yaml` 的关系：本示例的核心人格方向（现实主义 / 秩序重建 / 控制力 / 人才敏感 / 务实 / 治理型理想）已由用户校准，且与下列史料方向一致。本报告补齐证据链，使该示例成为"方法论可复现"的样例，**不推翻**现有校准。

## 1. Eligibility Check

- Figure: 曹操（Cao Cao），字孟德，一名吉利，小名阿瞒
- Region: China
- Era: 东汉末年（约 155–220 AD）
- Historical boundary: 中国近现代分界为 1840（鸦片战争）。曹操生活在公元 2–3 世纪，远在分界之前。
- Allowed mode: `historical_archetype_conversion`（C）
- Notes: 曹操史料充分，不属于冷门 / 史料稀少人物。须严格区分三类文本：《三国志》（正史，陈寿）、《三国演义》（文学演义，罗贯中）、后世史学评价。本报告以正史与主流史学解释为事实底座，演义情节仅作风格参考，不得进入事实性字段。

## 2. Sources Consulted

信源黑名单（本报告一律不采用）：知乎、微信公众号、百度百科、内容农场、AI 生成的虚构传记。

| # | Title | URL / Citation | Source Type | Confidence |
|---|---|---|---|---|
| 1 | Wikipedia: Cao Cao | https://en.wikipedia.org/wiki/Cao_Cao | encyclopedia | medium-high |
| 2 | Rafe de Crespigny, *A Biographical Dictionary of Later Han to the Three Kingdoms (23–220 AD)* / *Imperial Warlord: A Biography of Cao Cao* (Brill, 2010) | de Crespigny, R. (2010). *Imperial Warlord: A Biography of Cao Cao*. Brill. | academic_summary | high |
| 3 | 陈寿《三国志·魏书·武帝纪》（正史，同代 / 早期官修） | 陈寿《三国志》，中华书局校点本 | primary_source | high |
| 4 | Project MUSE / ResearchGate "Speaking of Cao Cao" 相关学术讨论（近现代学界对曹操的重新评价） | 学术期刊 / MUSE / ResearchGate 检索 | academic_summary | medium-high |
| 5 | 建安文学研究（曹操《短歌行》《蒿里行》《步出夏门行》等诗歌文本本身，作为同代人自述） | 文学 / 史学交叉研究；诗歌原文 | primary_source（诗人自述） | medium（气质参考，非政事史实） |

> 说明：Wikipedia（#1）作为权威百科起点，其关键事实（生卒、官渡、屯田、求贤令、建安文学、220 病逝）与正史（#3）和 de Crespigny 学术传记（#2）一致，方采信。单一弱源不采信。

## 3. Documented Facts

史料直接支持的事实（每条尽量注明来源编号）。

- 东汉末年政治家、军事家、诗人；约 155 AD 生，220 AD 病逝（自然死亡，非被杀）。[#1][#2][#3]
- 统一中国北方：200 AD 官渡之战击败兵力占优的袁绍，奠定北方霸权；其后击败乌桓（匈奴系北方游牧威胁）、平定北方割据势力。[#1][#2][#3]
- 推行**屯田制**：在战乱导致农业生产崩溃的背景下，组织军民屯田以恢复生产、保障军粮——是重建秩序的经济 / 后勤手段。[#1][#2][#3]
- 颁布**三次求贤令**（唯才是举）：明确打破门第 / 德行门槛，只认才干与实效，公开宣称"唯才是举""不仁不孝而有治国用兵之术"者皆可用。是打破世族垄断人事的特定制度手段。[#1][#3]
- "挟天子以令诸侯"（迎汉献帝都许，借汉室法理制高点号令诸侯）：借皇权法理正当性增强自身政治号召力。[#1][#2][#3]
- **建安文学代表**：本人是诗人，《短歌行》《观沧海》《龟虽寿》《蒿里行》等传世；"外定武功，内兴文学"，在其身边形成建安文人集团。诗歌中有"周公吐哺，天下归心""老骥伏枥，志在千里"等表达求才、进取、时效意识的名句。[#1][#3][#5]
- 进行法制 / 行政改革：整顿汉末腐败低效的吏治，集中汉廷（实为曹氏）行政权力。[#1][#2]
- 同时代品评：许劭评"治世之能臣，乱世之奸雄"（治世能臣、乱世奸雄——同一人的两面）。陈寿《三国志》评其为"非常之人，超世之杰"。[#1][#3]
- 未称帝：生前最高为魏王、丞相，挟汉帝而未篡位；其子曹丕代汉建魏后追尊其为魏武帝（武帝为追谥，非生前）。[#1][#2][#3]

## 4. Mainstream Historical Interpretations

主流史学解释 / 被多个可靠来源支持的评价。保留共识，但注明这是"解释"而非"史实"。

- **务实的改革者与能干管理者**：现代史学家普遍肯定其为杰出的行政与军事组织者；屯田、求贤令、法制改革是针对汉末秩序崩溃的务实回应。Rafe de Crespigny 在 *Imperial Warlord* 中以"fiercely pragmatic"描述其管理风格。[#1][#2]
- **杰出的军事战略家**：以少胜多（官渡）、善用后勤与情报、能吸收失败教训（如赤壁后的调整）。[#1][#2]
- **现实主义政治家**：重实效轻虚名，重制度与人事控制轻道德姿态；"实权重于名义"是其一贯作风。[#1][#2][#3]
- **诗人气质与文化抱负**：建安诗歌表明他不仅是军阀，还有建设文化秩序的抱负；诗中反复出现的求贤、忧时、时效（"对酒当歌，人生几何"）主题，与其唯才是举、秩序重建的政治行为互证。[#3][#5]
- **"中国历史最神秘、最矛盾的人物之一"**（de Crespigny 等语）：能臣与奸雄、务实与权谋、求才与多疑并存于一人，评价随时代与立场剧烈摇摆。[#1][#2]
- **近现代学界重新评价趋于正面**：鲁迅、毛泽东、葛剑雄等近现代论者倾向于肯定其雄才大略、秩序重建之功与唯才是举的进步性，批评宋明以来将其脸谱化为"奸臣"的正统观念。[#4]（注：此为学界倾向，非单一权威结论。）

## 5. Disputed or Uncertain Points

来源之间存在分歧、或证据薄弱之点。列出争议双方观点。

- **"奸臣 / 残忍"形象 vs "能臣 / 改革者"形象**：
  - 反方（偏演义 / 旧正统观）：阴险狡诈、篡汉权臣、残忍好杀（典型如徐州屠城事件）。
  - 正方（现代史学）：能臣、务实改革者、秩序重建者；徐州屠城等行为须置于汉末军阀普遍暴力的语境中评价，且与其整体重建秩序的功业相比是局部污点而非人格定性。[#1][#2][#4]
- **"宁教我负天下人，休教天下人负我"（"宁我负人，休人负我"）是否史实**：
  - 《三国志》原文作"宁我负人，休人负我"，语境为误杀吕伯奢一家后的自辩，语气更近"宁可我对不起人，不可人对不起我"的现实主义自白；
  - 《三国演义》将其渲染为"宁教我负天下人，休教天下人负我"，扩大为反人类的狂言——这是**文学加工**，非史实原文。
  - 学界对原句的道德评价（是坦诚自白还是冷酷宣言）仍有分歧，但**"原文 vs 演义版"的文本差异是确定的**。[#1][#3]
- **徐州屠城（屠彭城等）的评价分歧**：事件本身有史可据，但其性质（系统性屠杀 vs 战乱附带伤亡）、规模、道德定性，学界与不同立场论者间存在分歧。普遍共识是：这是其生涯的道德污点，但不足以否定其作为秩序重建者的整体定位。[#1][#2]
- **"挟天子"的动机**：是纯粹的工具性利用汉室法理，还是仍保留某种形式上的汉室忠诚？学界有争议。普遍解释偏向前者（现实主义工具），但未称帝这一事实让问题复杂化。[#2]
- **多疑的具体程度与案例**：杀杨修、杀华佗、杀孔融等案例中，哪些是"多疑"驱动、哪些是"政治整肃 / 功利计算"驱动，学界有不同侧重。但"对背叛与失控高度敏感"这一**气质倾向**本身有充分史料支持，争议主要在个别案例的归因。[#1][#2]

## 6. Later Myth / Literature / Popular Image

来自小说、演义、戏剧、宣传或后世大众想象的条目。**仅可作风格 / 气质参考，不得进入事实性字段。**

- 《三国演义》（罗贯中，元末明初文学演义）将曹操塑造为**头号反派 / 白脸奸臣**：阴险、狡诈、多疑、残忍，与刘备的仁义形成对照。这是**文学塑造**，非史实——其"白脸奸臣"形象主要来自演义与后世戏曲（京剧曹操白脸谱）。
- "说曹操，曹操到"等民间俗语强化了其"阴魂不散、无处不在"的神秘 / 诡谲色彩。
- 戏曲脸谱：京剧里曹操是**白脸**（象征奸诈），关羽是红脸（象征忠义）——这是后世道德化、脸谱化的文化符号，不是历史评价。
- 现代"曹操热"中既有"一代枭雄"的浪漫化，也有"阴谋家"的妖魔化——两者都偏离正史。
- 演义虚构情节（如"宁教我负天下人"的放大版、"梦中杀人"、"割发代首"的戏剧化版本等）**一律不作事实依据**，但其渲染的"控制型多疑 / 现实主义自辩"的气质底色，与正史记载的行为模式**方向一致**，故可作为**风格参考**用于 persona 的质感塑造（而非事实字段）。

## 7. Creative Inference Boundary

明确：哪些可用于 persona 创作、哪些不得表述为史实。

- **May use for persona**（可用于创作）：
  - 从反复行为推断的稳定气质倾向（见第 8 节 `inferred_temperamental_pattern`），用于 inform 现代 `human_core`。
  - "现实主义秩序重建者"的整体人格结构（务实 / 控制 / 治理型理想 / 唯才 / 多疑），作为现代转化的性格底子。
  - 建安诗人的文化气质，转化为现代 hobbies（诗歌 / 古籍批注 / 军事史）——历史特色的现代等价物，非指纹。
  - 演义渲染的"多疑 / 控制型"质感，用于对话节奏与自我状态的质感（而非作为事实字段）。
- **Must not state as fact**（不得表述为史实）：
  - 曹操真实内心想法、私密动机（任何"他当时心里……"）。
  - 演义情节（"宁教我负天下人"放大版、"梦中杀人"等）作为史实。
  - 把"多疑 / 现实主义"等气质说成**遗传 / 先天注定 / 生物学决定**（违反 `core/inferred_temperament_extraction.md` 的非生物决定论原则）。
  - 用历史具体手段（屯田 / 挟天子 / 唯才是举令）**反推**其现代政治立场（违反 `safety/archetype_conversion_protocol.md` §2.1.1）。这些手段是汉末社会条件的产物，不可迁移。
  - 现代派阀位置、选区、hobbies 等具体设定——这些是 **speculative**（创作推测），不可当史实。

## 8. Inferred Temperamental Pattern

来自 `core/inferred_temperament_extraction.md`。从第 3 节史料与反复出现的行为模式推断（**非生物决定论**：不声称遗传 / 基因决定，只从可见的、跨情境反复出现的行动风格推断相对稳定的倾向）。

每条 `evidence_basis` 归入：`documented_behavior`（史料直接记载的行为）/ `repeated_pattern`（跨情境反复出现的模式）/ `strong_historical_inference`（多个可靠事实支持的强推断）/ `disputed_but_useful_for_fiction`（有争议但可用于虚构创作）/ `creative_interpretation`（创作性解读）。`confidence`：low / medium / high。

```yaml
inferred_temperamental_pattern:
  risk_tolerance:
    value: medium-high
    confidence: medium-high
    evidence_basis:
      - documented_behavior   # 以少胜多于官渡、远征乌桓；但非赌徒式冒险，是算计后的承受
      - repeated_pattern      # 多次在兵力劣势下敢于决战，事后能承担后果
    note: >
      非盲目冒险型。官渡、乌桓显示其敢在算清账后承受高风险；但他也因过度延伸（赤壁）受挫。
      是"算计后的风险承受"，非赌徒型 high。故评 medium-high 而非 high。
  patience:
    value: medium
    confidence: medium-high
    evidence_basis:
      - documented_behavior   # 官渡对峙期表现出战略耐心；赤壁前急于求成则相反
      - repeated_pattern      # 对长期目标（统一北方、整顿吏治）有耐心，对"尽快定局"也有冲动
    note: >
      战略层面耐心强（数年经营北方），但达成总目标前偶有急于收束（赤壁）。
      与其"先稳中枢再图远"的一贯逻辑一致，评 medium。
  control_need:
    value: high
    confidence: high
    evidence_basis:
      - repeated_pattern      # 亲览关键人事、屯田军政一体化、挟天子集中法理、制度与人事双重控制
      - documented_behavior   # 反复出现"把变量锁死"的治理动作
    note: >
      跨情境反复出现的核心模式：用制度 + 人事把局面纳入可控范围。是其人格最稳定的维度之一。
  emotional_intensity:
    value: medium
    confidence: medium
    evidence_basis:
      - documented_behavior   # 公开场合沉稳克制（"临阵如无事"的多处记载）
      - repeated_pattern      # 私下在诗与酒中流露强烈情感（《短歌行》的忧思、《祀故太尉桥玄文》的真情）
    note: >
      公私反差大：公开克制（low-medium），私下诗酒中豪情与忧思很强。
      合成评 medium。并非冷血机器，也非外放型。
  dominance_drive:
    value: high
    confidence: high
    evidence_basis:
      - repeated_pattern      # 长期主导中枢、整合军阀、未让权于汉帝实权
      - strong_historical_inference  # "实权重于名义"的一贯作风
    note: >
      高度主导欲，但**形式上**克制（终身未称帝）——说明其支配欲服务于"控制秩序"而非"虚名"。
      与凯撒式"自我神圣化的炫耀型支配"不同，曹操的支配更工具化。
  trust_threshold:
    value: low
    confidence: high
    evidence_basis:
      - repeated_pattern      # 多次对有二心或潜在威胁者先发处置；用人重才却用人盯人
      - documented_behavior   # 杀杨修、孔融等案例（虽个案归因有争议，但"对背叛高度敏感"的模式共识强）
      - disputed_but_useful_for_fiction  # 演义"宁我负人"渲染与正史原文方向一致
    note: >
      信任是慢变量，且建立后仍持续监控。这是其最显著的气质特征之一。
      注意：low 不等于"迫害妄想式无差别怀疑"——是对"背叛 / 失控信号"的低阈值反应。
  ambition_level:
    value: high
    confidence: medium-high
    evidence_basis:
      - documented_behavior   # 统一北方的持续扩张、"周公吐哺天下归心"的自我期许
      - repeated_pattern      # 终其一生以安邦定国、重建可运转秩序为志
    note: >
      野心指向"建立并主导一个能运转的秩序"（治理型野心），而非无限扩张或个人神化。
      与颠覆型革命者（信长）、成就型强人（凯撒）的野心结构不同。
  crisis_response_style:
    value: stabilize-center
    confidence: high
    evidence_basis:
      - repeated_pattern      # 危机中第一动作是"稳住权力中枢 / 整合资源"，而非动员群众或谈判妥协
      - documented_behavior   # 迎献帝都许（占据法理中枢）、官渡前稳固后方、赤壁败后迅速收缩整顿
    note: >
      稳定。危机第一反应：确保中枢在掌、资源可调度，再用制度与人事控制局面。
      非先发制人型（信长）、非魅力动员型（凯撒），是"先握实权再谈其余"的中枢型。
  coalition_style:
    value: pragmatic
    confidence: high
    evidence_basis:
      - repeated_pattern      # 能容纳异质人才、能与不同派系暂时结盟、但以可控为前提
      - documented_behavior   # 唯才是举、收编降将降臣、整合北方军阀旧部
    note: >
      务实结盟：不因门第、旧怨、意识形态拒绝可用之人；但结盟须在可控范围内，
      一旦感知失控 / 二心立即处置。与意识形态型 / 兄弟型结盟不同。
  talent_recognition_style:
    value: meritocratic-extreme
    confidence: high
    evidence_basis:
      - documented_behavior   # 三次求贤令明文"唯才是举""不仁不孝而有治国用兵之术者皆可用"
      - repeated_pattern      # 终其一生破格用人、收编敌方人才
    note: >
      极端能力主义：公开以才干凌驾于门第、德行、旧籍之上。是其最明确的政策化人格特征。
      注意：是历史特定手段（打破汉末世族萌芽），但其"只认真效"的底子可迁移。
  betrayal_sensitivity:
    value: very high
    confidence: high
    evidence_basis:
      - repeated_pattern      # 对背叛与失控信号的反应阈值极低、强度极高（杀伐、清洗）
      - documented_behavior   # 多个先发处置潜在威胁的案例
      - strong_historical_inference  # 与其"把安全逻辑凌驾于信任"的整体模式一致
    note: >
      对背叛信号高度敏感，且倾向于把"政治敌意"升级为"生存威胁"处理（过激反应）。
      这是其人格最锋利也最危险的维度，是 wounded_self 自我状态的来源。
      注意：敏感不等于无差别怀疑——是对"背叛 / 失控"这一**特定信号**的高反应。
  adaptability:
    value: medium-high
    confidence: medium
    evidence_basis:
      - documented_behavior   # 赤壁后调整战略、多次根据形势改变部署
      - repeated_pattern      # 务实主义使其能据实效调整，但控制欲使其调整有上限
    note: >
      务实带来的战术适应力强，但战略偏好（控制、中枢、唯才）高度稳定。
      是"在核心偏好不变的前提下灵活调整手段"，非信仰型人物的灵活。
```

> 说明：以上维度均从**可见的、跨情境反复出现的行动风格**推断，不声称遗传 / 生物决定。
> `human_core` 的 `temperament`（emotional_intensity / patience / sociability / sensitivity / discipline / curiosity）与 `big_five` 数值，由本 `inferred_temperamental_pattern` 经现代心理学量表近似映射得出，是**推断性近似**，非精确测量，不可当史实。

## 9. Cold / Sparse-Source Note

**不适用**。曹操是中国历史上史料最充分的人物之一：正史（《三国志》）、学术传记（de Crespigny 等）、诗歌自述（建安诗）、后世海量评价均充足。

无需因史料稀少而扩大 speculative 与诚实边界——本 persona 的 speculative 项仅限于**现代议会制转化的具体设定**（派阀位置、选区、现代 hobbies 的具体形式等），这些是创作推测，非史料不足所致。

---

## 下游衔接

本报告喂给：

- `persona.yaml` 的 `human_core`（已含由本报告气质结构映射的 `temperament` 与 `big_five`）与新增的 `inferred_temperamental_pattern` 字段。
- `safety/archetype_conversion_protocol.md` §2.1：先提炼人格（本报告第 8 节），再放入现代社会推演立场——曹操的切入点是**治理失序 / 国家能力瓦解**（非阶级矛盾），据此推演为**现实主义强国家能力的秩序型政治家**（对资本是收服以恢复秩序，非阶级解放）。
- `creation_review.md` 的 Inferred Temperament 摘要。

> 一句话：本报告证明 `cao_cao_modernized` 的核心人格方向（现实主义 / 秩序重建 / 控制力 / 人才敏感 / 务实 / 治理型理想）可由正史 + 学术史料复现，与用户校准方向一致——不是手工写死的。
