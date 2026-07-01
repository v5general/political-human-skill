# Generator · 创建一个 political_human persona

> **作用**：创建新 persona 的生成器协议。它是 `SKILL.md` 第 5 节（Phase 0→5）在 family 层的操作手册。参考 colleague-skill 的 intake → 分析 → 生成预览 → 写入 流程。
>
> **前置**：本 family 的定义与安全契约见 `family.md`。

---

## 触发

用户表达创建意图：「造一个政治人物 / 做个议员 / 把 X 转成现代政治家 / 给《绝对多数》设计一个 NPC」等。

---

## Phase 0：入口分流 + 安全初筛

1. 判定生成模式（A 原创 / B 历史推演 / C 历史转原型），或“分析近现代现实人物”/“疑似不安全近克隆”。
2. **立即安全初筛**（`core/safety_boundaries.md` + `safety/modern_political_figure_policy.md`）：指向近现代现实人物（含换皮/拼接）→ 不进入生成，走 `safety/recognizability_review.md`。
3. 记录 `integration_target`（standalone / absolute_majority）。

---

## Phase 0.5：创建 persona 目录

```text
personas/{slug}/
├── persona.yaml  relationship.json  memory.json
├── SKILL.md  examples.md  meta.json
└── references/{research/, sources/}   # 仅 mode B/C
```

`slug` 规则：原创 `original_<主题>` 或自定；历史转化 `<人物拼音/罗马名>_modernized`。

---

## Phase 1：资料采集与原型提炼

- **mode A**：以用户描述为主，必要时补宽泛政治类型画像。
- **mode B/C**：史料采集（分轨落盘 `references/research/`），遵守 `safety/historical_figure_policy.md` 六条史料纪律与三级推断；信源黑名单（知乎/公众号/百度百科/内容农场）。
- **mode C 历史语境转译**：不得直接套用历史人物原时代的政治立场。先理解其原时代主要矛盾，剥离不可迁移的时代条件，再提炼稳定人格结构，最后放入现代议会制社会情况、制度条件与政治约束中推演现代立场。

> 同名历史人物任务**不得套用示例**，须基于当前资料重新推算（见 `safety/historical_figure_policy.md` 第 6 节）。

---

## Phase 1.5：提炼质量检查点

向用户展示结构化摘要（历史时代主要矛盾/不可迁移时代条件/稳定人格结构/欲望弱点/行为模式/危机反应/现代社会情况与政治约束/三级推断占比/待删指纹），确认后继续。冷门人物降低推断密度、扩大诚实边界。

---

## Phase 2：安全与可识别性审核（强制）

跑 `safety/recognizability_review.md` 全流程（指纹扫描 → 不通过则提炼 → 删除指纹 → 转化 → 再扫）。mode C 额外核对 `safety/archetype_conversion_protocol.md` 的必须删除清单。

结果：`PASS` 或 `safe_conversion`。`real_figure_clone` 不允许存在。

---

## Phase 3：persona 构建（六层）

读取 `templates/persona_template.yaml`（mode A/C）或叠加 `templates/historical_archetype_conversion.yaml`（mode B/C），按层填入：

1. 身份层 identity
2. 人性核心层 human_core（先填）
3. 生活质感层 life_texture
4. 政治职业层 political_core
5. 自我状态层 self_states
6. 内在冲突层 inner_conflicts（至少 2 条，人层 vs 政治层张力）

> Human First：先人层后政治层，最后写冲突。

> Mode C 额外规则：`political_core.ideology` 必须由“稳定人格结构 × 现代社会情况/制度条件/政治约束”推演而来。不要把历史立场、历史敌友、古代制度选择或时代口号直接映射成现代左右翼标签。

---

## Phase 3.5：构建预览确认

向用户展示 5–8 行摘要（身份/人性底色/政治坐标/内在冲突/自我状态/输出模式/安全状态），确认后写入。

---

## Phase 4：写入 persona 文件

写入 `personas/{slug}/` 全部文件：

- `persona.yaml`：六层档案。
- `relationship.json`：用 `templates/relationship_template.json` 初始化（stranger / caution=50）。
- `memory.json`：用 `templates/memory_template.json` 初始化（空记忆 + 隔离字段）。
- `SKILL.md`：内嵌运行时协议（`core/runtime_protocol.md`）+ 角色卡 + 自我状态 + 风格 + 诚实边界，使该 persona 可被宿主直接激活运行。
- `examples.md`：公开/私下/辩论/危机/亲密 五种场合各一例。
- `meta.json`：`source_type / mode / integration_target / safety_status / version / created_at / language`。

---

## Phase 5：质量验证

跑 `validators/`（persona_consistency / recognizability / dialogue_regression 等）：双层完整、一致、场合区分度、安全状态、诚实边界均达标。不达标回 Phase 2/3 迭代。

---

## 交付与进化

- 交付：告知 persona 位置 `personas/{slug}/`，提示可用 `invocation.md` 激活。
- 进化：用户后续追加资料 / 对话纠正 / 修改设定 → 见 `SKILL.md` 第 8 节与 `safety/modification_review.md`（每次修改必审）。
