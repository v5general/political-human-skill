# Dialogue Samples · 织田信长（现代转化版）

> 本目录存放转化后现代信长的多场景对话样本，供 generator / 调试 / 校验使用。
> 全部为虚构转化设定，不对应任何现实政治人物。
> 由 historical source-grounded workflow 重新生成（见 ../historical_source_report.md）。

## 文件说明

| 文件 | 场景 | 关系 | 自我状态 |
|---|---|---|---|
| `casual_private.md` | 私下闲聊 | trusted_listener | private_self |
| `public_interview.md` | 电视采访 | public_audience | public_self |
| `strategy_room.md` | 选战策略室 | inner_circle | strategic_self |
| `confrontation.md` | 正面交锋 | recurring_contact（低信任） | wounded_self 边缘 |
| `trust_low.md` | 低信任对话 | recurring_contact，caution 高 | strategic_self |
| `trust_high.md` | 高信任对话 | confidant | intimate_self 边缘 |
| `game_action.json` | 《绝对多数》游戏决策样本 | — | strategic_self |

## 对话规则遵守

所有样本遵守以下 Fast Dialogue 规则（见 ../../../core/）：

- **One-Pass Dialogue**：每轮一个回复形状，不内部起草多版。
- **Anti-Manifesto**：用具体政治对象（委员会/法案/预算/选区/补贴）而非空洞口号；金句只在辩论与绝境出现。
- **No Constant Testing**：锋利 ≠ 每轮审问。普通对话在具体指导、干纠正、缩小问题、干玩笑、场景推进之间轮流；测试只在真正的门槛时刻出现，且测试后转具体任务。
- **Conversational Realism**：回复可短、可平、可带半句，不追求每句都是金句。
