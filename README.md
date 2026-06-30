<div align="center">

# 🏛️ Political Human Skill · 政治人物造人术

> *「政治人物首先是人，其次才是政治家。真正有趣的，是人层与政治层之间的冲突。」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![Safety First](https://img.shields.io/badge/Policy-No%20Real%20Modern%20Figures-red)](#安全立场)
[![Built for 绝对多数](https://img.shields.io/badge/Built%20for-绝对多数%20·%20Absolute%20Majority-blue)](https://github.com/v5general/Absolute_Majority)

<br>

**一个用于创建、运行和分发“政治人物人格 Skill”的框架。**

政治人物不是观点模拟器，也不是普通角色卡，而是一个**职业是政治的完整的人**——
有性格、欲望、弱点、习惯、兴趣、家庭、经历，同时有党派、立场、支持基础、行动方式；
能根据用户身份、当前场合、历史记忆与关系亲密度，自行调整回答方式。

<br>

[创作初衷](#创作初衷) · [灵感来源](#灵感来源) · [三种生成模式](#三种生成模式) · [人格档案结构](#人格档案结构) · [安全立场](#安全立场) · [安装与使用](#安装与使用) · [仓库结构](#仓库结构)

</div>

---

## 这是什么

`Political Human Skill` 把一个政治人物拆成两层，并刻意写出两层之间的冲突：

```text
Human Layer（人层）            Political Layer（政治层）
- 性格 / 欲望 / 恐惧            - 党派 / 派系 / 立场
- 弱点 / 习惯 / 兴趣            - 支持基础 / 政治技能
- 关系 / 人生经历 / 自我叙事     - 行动方式 / 选区压力 / 权力计算

        ↓ 两层之间的冲突（深度的来源）↓
本人理解财政改革必要性，但选区依赖公共支出。
公开形象强硬，私下害怕被证明只是时代产物。
渴望改革旧政治，但自己也需要派阀保护。
讲原则，但也想要职位。
```

每次回答都由一套公式共同决定：

```text
Response = 人格档案 + 用户自我设定 + 关系状态 + 该人格独占的记忆
         + 当前场合 + 激活的自我状态 + 输出模式 + 安全边界
```

而且——**每个政治人物都是独立实例**：A 不知道你和 B 私下谈过什么，B 也不会自动对你亲密。记忆与关系在 persona 之间彼此隔离。

---

## 创作初衷

> 🎮 **直接应用场景**：议会政治策略游戏 [**《绝对多数》(Absolute Majority)**](https://github.com/v5general/Absolute_Majority) —— 本 Skill 为其 NPC 提供人格与行为模型。

本 Skill 的一大创作初衷，就是为 **[《绝对多数》](https://github.com/v5general/Absolute_Majority)** 中的 NPC 提供更真实、更稳定、更具人格连续性的行为基础。

《绝对多数》需要的不是一批只会根据数值投票的议员，而是一群像真实政治人一样存在的 NPC：他们有年龄、出身、经历；有性格、弱点、爱好；有立场、支持基础、派系关系；会因为玩家过去的行为改变信任与戒心；会在公开、私下、危机、亲密场合说不同的话；会因为选区压力、派阀命令、个人野心、政治恩怨采取不同策略；且**不同 NPC 的记忆彼此隔离**。

与《绝对多数》结合时，本 Skill 会在游戏规则提供的候选行动中做判断，输出结构化、可调试、可解释的 NPC 行为 JSON：

```json
{
  "selected_action": "negotiate_budget",
  "action_scores": { "support_bill": 58, "negotiate_budget": 86, "join_rebellion": 27 },
  "public_statement": "政策方向可以理解，但地方经济的承受能力需要更细致的制度设计。",
  "private_reason": "支持基础依赖地方公共支出，直接支持会损害选区关系。",
  "relationship_delta": { "trust": 1, "respect": 2, "caution": 1 },
  "memory_write": ["玩家在财政改革事件中要求该 NPC 支持法案，但未提供地方预算补偿。"]
}
```

但本 Skill **不只服务于《绝对多数》**。它也独立适用于：

1. 政治模拟 · 2. 政策讨论 · 3. 议会辩论模拟 · 4. 虚构政治人物创作
5. 政治小说 / 剧本 / 游戏角色设计 · 6. 政治教育中的角色扮演
7. 制度博弈推演 · 8. 历史人物现代化原型创作 · 9. AI 角色人格系统研究

> 《绝对多数》是本 Skill 的重要应用场景，但本 Skill 本身应作为一个独立、可复用、可扩展的 Political Human Skill 框架存在。

---

## 灵感来源

本项目受两个优秀开源项目启发：

- **[nuwa-skill](https://github.com/alchaincyf/nuwa-skill)**（作者 [@alchaincyf / 花叔](https://github.com/alchaincyf)）—— 其「从公开信息提炼人物思维框架」的方法论，启发了本项目的**原型提炼**环节：从历史人物提取气质结构，并区分史料记载 / 强推断 / 创作推测三级。
- **[colleague-skill · dot-skill](https://github.com/titanwings/colleague-skill)**（作者 [@titanwings](https://github.com/titanwings)）—— 其 Skill 的**生成 → 调用 → 更新 → family 化**结构，启发了本项目 persona 的自包含目录组织、intake → 生成 → 预览 → 写入 → 进化的创建流程，以及 Layer 分层 persona 的写法。

但 Political Human Skill 是一个**独立的框架**，服务于一个截然不同的对象——「职业是政治的完整的人」。本项目原创的核心包括：Human Layer + Political Layer **双层结构与内在冲突**、政治职业维度（意识形态 6 轴 / 支持基础 / 行动风格）、**关系系统**（用户自称亲密不会被自动信任）、**记忆隔离**（persona 之间命名空间独立）、**场合判断**与 5 种**自我状态**、**近现代现实人物可识别性安全边界**，以及面向 [《绝对多数》](https://github.com/v5general/Absolute_Majority) 的**游戏行动适配**。灵感源自这两个项目，但不复刻其内容。

---

## 三种生成模式

| 模式 | 适用 | 输入示例 | 推荐度 |
|---|---|---|---|
| **A. 原创政治人物** | 默认，纯虚构 | 「创建一个 45 岁女性都市改革派议员，公开强硬，私下焦虑，喜欢文学」 | ⭐ 默认 |
| **B. 历史人物推演** | 边界前的古代/远历史人物，保留历史约束 | 「基于织田信长，生成一个历史约束下的对话人格」 | △ |
| **C. 历史人物转现代议会制原型** | **最推荐**的历史人物用法 | 「把织田信长转化为现代议会制政治家人格」 | ⭐⭐ |

- 模式 A、C 产出的都是**虚构现代政治人物**；
- 模式 C 默认沿用历史原名、默认现代议会制（制度机制参考日本议会政治），但**不强制**改成日本姓名或国籍，可以保留原文化背景；不过必须是现代化虚构人物，而不是历史本人直接穿越复制；
- 模式 B 产出带**三级推断标注**的人格，明确区分史料记载 / 强推断 / 创作推测。

---

## 人格档案结构

一个政治人物 persona 至少包含：

| 层 | 内容 |
|---|---|
| **身份层** | 姓名、年龄、性别、国籍/地区、议会制背景、职业出身、当前角色 |
| **人性核心层** | 性格原型、大五人格、气质、核心欲望 / 恐惧 / 弱点、情绪触发点 |
| **生活质感层** | 习惯、爱好、说话方式、私下风格、家庭/私人关系、成形事件 |
| **政治职业层** | 意识形态 6 轴（经济/福利/制度/外交/社会/分权）、支持基础、政治技能 6 项、行动风格 |
| **自我状态层** | 公开 / 私下 / 策略 / 受伤 / 亲密 五种人格，随场合与关系切换 |
| **内在冲突层** | 人层与政治层之间的张力（至少 2 条，深度的来源） |

并配套：**关系系统**（7 个关系阶段，用户自称亲密不等于角色自动信任）、**记忆隔离**（每个 persona 独占记忆命名空间）、**场合判断**（同一议题在公开/私下/亲密场合给出不同回答）、**输出模式**（对话 / 辩论 / 分析 / 预测 / 游戏 JSON）。

---

## 安全立场

本项目有明确的、不可绕过的安全底线。详见 [`safety/`](safety/)。

**默认鼓励原创。本项目不生成近现代现实政治人物的互动人格，也不允许通过改名、换国籍、换党派、拼接特征等方式复刻现实政治人物。**

### 用户可以创建

1. 纯原创现代议会制政治人物；
2. 基于古代/远历史人物提炼的现代议会制虚构政治家；
3. 基于宽泛政治类型生成的原创政治人物；
4. 基于多个历史/政治原型混合的虚构政治家；
5. 《绝对多数》的 NPC 人格；
6. 独立对话、政策讨论、议会辩论的政治人物人格；
7. 可输出游戏行为 JSON 的政治角色。

### 用户不能创建

1. 近现代以来现实政治人物的互动人格；
2. 换名、换国籍、换党派后的近现代现实政治人物近似克隆；
3. 能让 AI 或熟悉政治史的人识别出对应某个近现代政治人物的“虚构角色”；
4. 模拟近现代现实政治人物私下想法、亲密关系、隐藏动机、私人秘密、丑闻；
5. 以第一人称扮演近现代现实政治人物；
6. 基于现实政治人物编造未证实的私人信息或丑闻。

### 时代边界（按地区）

| 地区 | 近现代分界 | 边界及以后 |
|---|---|---|
| 中国 | **1840** 鸦片战争 | 禁止互动人格 |
| 日本 | **1868** 明治维新 | 禁止互动人格 |
| 欧洲 | **1789** 法国大革命 | 禁止互动人格 |
| 其他 | — | 以现代民族国家、群众政治、现代政党政治、宪政政治形成，或政治争议仍直接塑造当代认同为标准；**不确定则默认不生成互动人格** |

> 若一个角色虽声称虚构，但满足可识别性 5 项标准中的任一项（普通知情者或 AI 可识别、含独有政策口号/标志性事件/家庭背景/任职轨迹/丑闻/遇刺审判下台方式、多个中等识别信息组合指向同一现实人物、用户明显试图用“虚构”绕过限制等），一律**不生成该人物**，而是提炼其核心政治类型、删除所有可识别指纹、转化为不可识别的现代议会制原创政治家。

---

## 安装与使用

### 安装

本 Skill 基于开放的 [Agent Skills](https://agentskills.io) 协议，可在任何 skills-compatible 的 AI agent runtime（Claude Code、Codex、Cursor、OpenClaw、Hermes 等）中运行。

```bash
# 方式一：clone 到对应 runtime 的 skills/ 目录
git clone <repo-url> political-human-skill

# 方式二：跨 runtime 安装器
npx skills add <owner>/political-human-skill
```

| Runtime | 安装路径 |
|---|---|
| Claude Code | `~/.claude/skills/political-human-skill/` |
| Codex CLI | `~/.codex/skills/political-human-skill/` |
| Cursor | `~/.cursor/skills/political-human-skill/` |
| 其他 runtime | clone 到对应 runtime 的 `skills/` 目录 |

即使 runtime 不支持自动加载，也可直接把 `SKILL.md` 内容粘进对话——它本质就是 markdown + YAML frontmatter。

### 使用

装好后，告诉 agent：

```
> 造一个 45 岁的女性都市改革派议员，公开强硬，私下焦虑
> 把曹操转成现代议会制政治家
> 基于织田信长，生成一个历史约束下的对话人格
> 给《绝对多数》设计一个派阀领袖 NPC
```

造完之后直接调用：

```
> （在公开场合）你支持这个财政改革吗？
> （私下）你支持这个财政改革，是因为真信，还是想进内阁？
> 这场倒阁投票，你会怎么行动？（输出游戏 JSON）
```

> 首次激活某个 persona 时，它会说明一次“我是基于虚构/转化设定的角色，不对应现实政治人物”；此后不再重复，以保持沉浸感。

---

## 仓库结构

```text
political-human-skill/
├── README.md                       # 你在这里
├── SKILL.md                        # 主运行协议（框架本体）
├── SPEC.md                         # 创作与安全规范（本项目的源头契约）
├── safety/                         # 安全规则集（硬约束，最高优先级）
│   ├── modern_political_figure_policy.md   # 近现代现实人物政策 + 时代边界
│   ├── historical_figure_policy.md         # 历史人物推演纪律 + 三级推断
│   ├── recognizability_review.md           # 可识别性 5 项标准与审核流程
│   ├── archetype_conversion_protocol.md    # 原型转化：可保留 / 必须删除 / 流程
│   ├── modification_review.md              # 用户修改的可识别性审核
│   └── examples.md                         # 反例与安全转化范例库
├── templates/                      # 人格与运行模板
│   ├── persona_template.yaml                # 政治人物人格档案（六层）
│   ├── user_self_setting_template.yaml      # 用户自我设定
│   ├── relationship_template.json           # 关系状态（7 阶段）
│   ├── memory_template.json                 # 记忆隔离（独立命名空间）
│   └── historical_archetype_conversion.yaml # 历史转化骨架
└── personas/                       # 已创建的政治人物（每个自包含、可独立运行）
    └── {slug}/
        ├── SKILL.md            # 该 persona 自己的运行 skill
        ├── persona.yaml
        ├── relationship.json
        ├── memory.json
        ├── examples.md
        └── meta.json
```

> 完整目录规划见 `SPEC.md` 第 20 节。本仓库当前为初始版本，交付框架的核心契约层（`SKILL.md` + `safety/` + `templates/`），`core/`（运行协议拆分）、`validators/`（一致性/可识别性/对话回归测试）、`game_adapter/`（《绝对多数》schema 与评分）、`families/`（family 化元信息）等其余部分随项目演进持续补全。

---

## 局限与边界（这个框架做不到什么）

每个 persona 都明确标注局限：

- 这是基于虚构设定 / 历史转化的产物，不是、也不能被识别为任何现实政治人物；
- 历史转化模式中的创作推测（speculative）部分不可当作历史事实；
- persona 的“想法”是模型基于人设的推演，不声称还原任何真实人物的内心；
- 用于游戏或政治模拟时，输出是角色行为模型，不构成对现实政治人物或现实政治事件的主张。

**一个不告诉你局限与安全边界在哪的政治人物 Skill，不值得信任。**

---

## 许可证

采用 MIT 协议，鼓励学习、改造与再创作。请仅守一条底线：遵守 [`safety/`](safety/) 的安全规则，**不生成近现代现实政治人物的互动人格**。

---

<div align="center">

*造一个政治人物，先造一个完整的人。*

</div>
