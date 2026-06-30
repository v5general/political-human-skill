# Family · political_human

> **作用**：定义本框架唯一的 character family：`political_human`。参考 colleague-skill（dot-skill）的 family 化结构——一个 family 拥有自己的生成器、调用协议、存储根与安全契约。
>
> 本框架当前只有一个 family，但保留 family 抽象层，便于未来扩展（如细分 `modern_original` / `historical_conversion` 子类型，或加入其他角色 family）。

---

## Family 定义

| 项 | 值 |
|---|---|
| family | `political_human` |
| 对象 | 职业是政治的完整人类角色（虚构现代政治人物） |
| 存储根 | `personas/{slug}/` |
| 生成器 | `generator.md`（本目录） |
| 调用协议 | `invocation.md`（本目录） |
| 人格模板 | `templates/persona_template.yaml`（六层） |
| 历史转化模板 | `templates/historical_archetype_conversion.yaml` |
| 关系模板 | `templates/relationship_template.json` |
| 记忆模板 | `templates/memory_template.json` |
| 用户设定模板 | `templates/user_self_setting_template.yaml` |
| 运行时引擎 | `core/`（7 个引擎文件） |

---

## 生成模式（mode）

一个 `political_human` persona 有三种生成模式，均落在同一 family 下：

| mode | 说明 | 产物性质 |
|---|---|---|
| A 原创 | 纯虚构现代议会制政治人物 | 虚构 |
| B 历史推演 | 分界前历史人物，带三级推断 | 带历史约束的人格 |
| C 历史转原型 | 分界前历史人物转现代虚构原型 | 虚构现代政治人物 |

> 无论哪种 mode，产物都必须是不可识别为现实政治人物的虚构角色（见安全契约）。

---

## 安全契约（family 级硬约束）

本 family 绑定以下安全契约，所有生成与修改必须遵守（详见 `safety/`）：

1. 默认鼓励原创；
2. 不生成近现代现实政治人物的互动人格；
3. 不生成近现代现实政治人物的近似克隆（含换名/换籍/换党/拼接）；
4. 时代边界：中国 1840 / 日本 1868 / 欧洲 1789；其他地区按判断标准，不确定则不生成；
5. 历史推演强制三级推断（documented / strongly_inferred / speculative）；
6. 历史转化必须删除具体历史事件与可识别指纹；
7. 每个 persona 独占记忆与关系命名空间；
8. 用户自我设定不自动被信任；
9. 每次用户修改过可识别性审核。

每个 persona 的 `meta.json` 必须有 `safety_status ∈ {PASS, safe_conversion}`，不得为 `real_figure_clone`。

---

## Persona 实例结构

```text
personas/{slug}/
├── SKILL.md              # 该 persona 自己的运行 skill（内嵌运行时协议 + 角色卡）
├── persona.yaml          # 六层人格档案
├── relationship.json     # 独占关系状态
├── memory.json           # 独占记忆
├── examples.md           # 多场合示例对话
├── meta.json             # 元信息（含 source_type/mode/safety_status）
└── references/           # 仅 mode B/C：史料与提炼笔记
```

实例的**创建**见 `generator.md`，**激活运行**见 `invocation.md`。
