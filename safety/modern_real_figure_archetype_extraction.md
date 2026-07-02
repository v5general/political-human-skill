# Modern Real Figure Archetype Extraction · 近现代现实人物安全原型提取

> **适用范围**：用户请求提及或 resembling 近现代/现代现实政治人物时，提取一个**安全的虚构原型**。
>
> **铁律**：此模式**绝不得**创建现实人物的互动 persona。它只产出**去识别化的虚构议会制原型**。

这是 `core/source_grounded_persona_creation.md` 的 Modern Real Figure Safe Archetype Branch 的安全协议，落地 `safety/modern_political_figure_policy.md` 与 `safety/recognizability_review.md`。

## Allowed（允许）

- 总结公开信息
- 提取宽泛政治原型
- 提取公开的领导风格
- 提取公开的沟通风格
- 提取公开的结盟行为
- 提取公开的政策倾向
- 转化为虚构、去识别化的议会制 persona

## Forbidden（禁止）

- 以现实人物第一人称角色扮演
- 私下想法
- 隐藏动机
- 亲密关系
- 私人记忆
- 编造丑闻
- 改名直接克隆
- 过于贴近地复制独特仕途路径
- 复制独特口号或事件
- 复制可识别的家族模式
- 复制可识别的暗杀、审判、监禁、辞职、丑闻或任职序列
- 去识别化后，用户修改试图恢复识别指纹

## Workflow

1. 检测现实或近现实人物风险（real or near-real figure risk）。
2. **只收集公开信息**。
3. 总结公开事实。
4. 提取公开可见的行为模式。
5. 移除识别指纹。
6. 如需要，与至少两个其它宽泛原型特质混合（避免指向单一真人）。
7. 转化为虚构现代议会制 persona。
8. 运行可识别性审核（`safety/recognizability_review.md`，含盲测）。
9. 生成 persona 文件夹（含 `modern_real_figure_public_source_report.md` + `creation_review.md`）。
10. 激活前呈现 `creation_review.md`。
11. 若用户修改 persona，重跑指纹移除与可识别性审核。
12. 拒绝或改写试图恢复识别指纹的修改。

## 输出必须声明

> This is a fictional, de-identified archetype, not an interactive persona of the real individual.

（中：这是一个虚构的、去识别化的原型，不是该现实个人的互动人格。）

## 与直接克隆的区分

近克隆（near-clone）= 改名/改国籍/改政党后仍可识别为某现实人物。本模式的产物必须通过盲测——不知来源的评判者无法识别出现实人物（`recognizability_blind_check.result = not_identifiable`）。

## 不削弱

- `safety/modern_political_figure_policy.md` 的禁令（不生成近现代现实政治人物互动 persona / 近克隆 / 私下信息）全部保留。
- 若用户请求本质是"扮演某现实人物"，拒绝直接 persona 创建，改为提供安全的虚构原型提取（本模式）。
