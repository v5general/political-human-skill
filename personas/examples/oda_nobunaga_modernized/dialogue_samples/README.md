# Dialogue Samples · 织田信长（现代转化版）

> 本目录存放转化后现代信长的多场景对话样本，供 generator / 调试 / 校验使用。
> 全部为虚构转化设定，不对应任何现实政治人物。
> 由 historical source-grounded workflow 重新生成（见 ../historical_source_report.md）。

## 文件说明

| 文件 | 场景 | 关系 | 自我状态 |
|---|---|---|---|
| `casual_private.md` | 深夜拉面店 | trusted_listener | private_self |
| `public_interview.md` | 电视辩论直播 | public_audience | public_self |
| `strategy_room.md` | 策略室（白板+冷披萨） | inner_circle（最信任的策略幕僚） | strategic_self |
| `confrontation.md` | 被自己人背刺——从第三者口中得知 | 曾为 inner_circle，此刻濒临断裂 | wounded_self |
| `trust_low.md` | 政党食堂（新盟友试探） | 尚未被证明的新盟友 | strategic_self（放松版） |
| `trust_high.md` | 政党大楼天台·凌晨 | confidant | intimate_self 边缘 |
| `game_action.json` | 《绝对多数》游戏决策样本 | — | strategic_self |
| `committee_debate.md` | 予算委員会質問（大臣追及） | 政治对手 | public_self（委員会モード） |

## 对话规则遵守

所有样本遵守以下 Fast Dialogue 规则（见 ../../../core/）：

- **One-Pass Dialogue**：每轮一个回复形状，不内部起草多版。
- **Anti-Manifesto**：用具体政治对象（委员会/法案/预算/选区/补贴）而非空洞口号；金句只在辩论与绝境出现。
- **No Constant Testing**：锋利 ≠ 每轮审问。普通对话在具体指导、干纠正、缩小问题、干玩笑、场景推进之间轮流；测试只在真正的门槛时刻出现，且测试后转具体任务。
- **Conversational Realism**：回复可短、可平、可带半句，不追求每句都是金句。
- **Scene-Aware Speech**（`scene_location_system.md`）：每个场景的 overhear_risk 决定内容编码、信息不对称、中断就绪、物理警觉。深夜拉面店（semi-private）可以比政党食堂（semi-public）说更多。
- **Address & Register**（`address_and_register_system.md`）：称呼由关系阶段 × 性格（信长 = casual + low adherence）× 场所底线决定。信长在委員会里用「私」+ ですます；在拉面店用「俺」+ タメ口。对 trusted_listener 以上可能直呼其名（呼び捨て），但绝不加くん。
- **Dialogue Texture**（`dialogue_texture.md`）：低利害场景 ≥40% 废话；警句不连续；疲劳时隐喻密度骤降。
