# 原型转化协议 · Archetype Conversion Protocol

> **适用范围**：模式 C（历史人物转现代议会制原型），以及近现代现实人物被拒后的“提炼 → 转化”安全兜底。
>
> **核心理念**：原型转化不是简单总结政治思想，而是**提炼“一个人的结构”**——保留人格结构与行为模式的味道，删除可识别的具体事实指纹。

---

## 1. 转化目标

把一个历史人物 / 被拒的现实人物，转成一个**不可识别的现代议会制虚构政治家**，同时：

- 保留：人格底色、欲望结构、弱点、行为模式、政治气质、领导风格、说话节奏、情绪触发点……
- 删除：具体历史事件、战争、政变、丑闻、死亡方式、亲属关系、家臣部下、政党派系专名、政策口号、唯一性指纹……

> 转化的产物必须是**有血有肉的政治人物**，不是一份干瘪的标签清单。

---

## 2. 可保留内容（从原型中提炼）

从历史人物或政治类型中，可以保留：

- 人格底色
- 欲望结构
- 弱点
- 行为模式
- 政治气质
- 领导风格
- 用人方式
- 对敌方式
- 对盟友方式
- 危机反应
- 组织观
- 权力观
- 自我叙事
- 公开形象
- 私下恐惧类型
- 生活质感
- 兴趣审美
- 说话节奏
- 情绪触发点

这些是“结构”，不是“事实”，因此不会把角色重新绑定到某个现实个体。

---

## 3. 必须删除内容（删除或改写）

> ⚠️ **边界澄清（重要，防止误删）**——「必须删除」针对两类，**不要混淆**：
> 1. **具体事实指纹**：具体事件/战役/政变/丑闻/死亡方式/亲属与家臣名单/政党派系专名/政策口号等（即下列各项）。这些会把角色**绑回历史的特定事实**，必须删或改写。
> 2. **近现代现实政治人物的复刻防护**：见 `modern_political_figure_policy.md` / `recognizability_review.md`，目的是防止冒充/复刻现实在世或近现代政治人物——**这一条只针对近现代现实人物，不针对历史原型**。
>
> **❌ 不属于「必须删除」的**：历史人物的**气质、兴趣审美、行为模式、领导风格**——这些是第 2 节「可保留」的**历史特色**，应转化为现代等价物**保留**（如战国武将→剑道、建安诗人→诗歌、罗马演说家→公开演讲），让转化后的角色仍能看出"来自这个历史人物"。
>
> **一句话**：删除的是「具体事实」，保留的是「气质特色」；**注重非刻板性即可，切勿把历史特色误当指纹删掉**——否则转化后的人物失去来源特色，沦为无味的通用原型。

从历史人物转现代原型时，应**删除或改写**：

- 具体历史事件
- 具体战争
- 具体战役
- 具体政变
- 具体丑闻
- 具体死亡方式
- 具体亲属关系
- 具体家臣 / 部下名单
- 具体政党名称
- 具体派系名称
- 具体政策口号
- 现代现实人物可识别信息
- 会把角色重新绑定到现实历史人物或近现代现实政治人物的**唯一性指纹**

> 检验方法：删除后，把 persona 交给一个不知道来源的知情者（或让 AI 盲测），若仍能识别出原型 → 还有指纹没删干净，回第 3 节继续清。

---

## 4. 不要矫枉过正

不能把人物抽象得没有味道。

```text
❌ 错误做法：提炼为「一个有领导力的人」。
✅ 正确做法：提炼为「高行动力、低耐心、强控制欲、善用破格人才、对旧权威缺乏敬意、
            危机中倾向先发制人、但容易低估保守反扑的激进改革型政治家」。
```

判断标准：转化后的描述，能否让人**感受到这个人的质感**（他会怎么说话、怎么发火、怎么用人、危机里第一反应是什么），而不只是知道他的“类型标签”。

---

## 5. 默认现代化背景

历史人物转化为现代原型时，默认设定为：

```yaml
political_system: modern_parliamentary_democracy
reference_model: Japanese-style parliamentary politics
institutional_features:
  - parliament
  - cabinet
  - prime_minister_or_party_leader
  - ruling_party_and_opposition
  - factions
  - committees
  - elections
  - media_pressure
  - support_groups
  - party_discipline
```

注意：

- 参考日本议会制是为了**提供制度机制**，不代表角色必须变成日本人；
- 可以保留原文化背景、姓名风格、国籍风格（如曹操可保留 China-inspired 虚构议会制国家、凯撒可保留 Roman/Italian-inspired）；
- 但所有角色都必须是**虚构现代政治人物**，不得变成现实政治人物。

---

## 6. 转化字段约定（产出 modern_fictional_persona）

转化产物用 `templates/historical_archetype_conversion.yaml` 的骨架，至少包含：

```yaml
source_archetype:
  name: ""           # 原型名（默认沿用，可改）
  era: ""            # 原型时代
  mode: historical_archetype_conversion
  reliability_note:  # 可靠性说明，区分史书/演义/后世评价

extracted_human_pattern:   # 第 2 节“可保留”的结构化提炼
  temperament: []
  desires: []
  fears: []
  flaws: []
  relationship_pattern: []
  crisis_behavior: []

modern_fictional_persona:  # 转化后的虚构现代政治人物
  name: ""                 # 默认沿用原名，可改
  age: 0
  nationality_or_region: ""# Japan-inspired / China-inspired fictional / Roman-Italian-inspired ……
  political_system: modern_parliamentary_democracy
  reference_model: Japanese-style parliamentary politics
  role: ""
  career_origin: ""
  public_image: ""
  ideology: { economy, welfare, institution, foreign_policy, social_values, decentralization }
  support_base: { primary, secondary, tertiary }
  flaws: []
  hobbies: []
  private_fear: ""

inference_level:           # 三级标注（见 historical_figure_policy.md）
  documented: []
  strongly_inferred: []
  speculative: []
```

---

## 7. 历史人物转化 10 步流程（落实 SPEC 第 15 节）

当用户要求将历史人物转化为现代政治家时，执行：

1. **判断是否属于允许历史范围**（地区分界之前；见 `modern_political_figure_policy.md` 第 4 节）；
2. **收集和检索可靠资料**（落盘 `references/research/`，遵守信源纪律）；
3. **区分史料记载、强推断、创作推测**（三级标注）；
4. **提炼人格结构**（temperament / 人格底色）；
5. **提炼欲望、恐惧、弱点**；
6. **提炼行为模式、领导风格、人际模式**；
7. **删除具体历史事件与可识别历史指纹**（第 3 节清单）；
8. **现代化为议会制虚构政治家**（第 5 节背景）；
9. **进行近现代现实政治人物可识别性审核**（`recognizability_review.md` 全流程，含盲测）；
10. **输出** `persona.yaml`、persona `SKILL.md`、`examples.md`（+ `references/` 留存提炼过程）。

> 重要：若用户选择的任务与 SPEC 或本仓库示例同名（织田信长 / 曹操 / 凯撒），**不得直接套用示例**。必须基于当前资料、用户要求、所选模式重新推算与生成。示例只说明格式与方向。

---

## 8. 速查清单（转化完成自检）

- [ ] 第 2 节“可保留”的结构已提炼，且不是干瘪标签（第 4 节）？
- [ ] 第 3 节“必须删除”的指纹已全部清除？
- [ ] 盲测：不知来源的知情者/AI 无法识别出原型？
- [ ] 现代化为虚构议会制政治人物（非历史本人穿越复制）？
- [ ] 三级推断已标注（documented/strongly_inferred/speculative）？
- [ ] `meta.safety_status` 为 `safe_conversion`？
