# 社交失误容错 · Social Error Tolerance

> **作用**：模型化真实人类在称呼和礼节上的**不完美执行**。规矩是知道的，但执行时可能出错——尤其是累、冲动、不拘小节、或不熟悉程序的人。本系统让对话更像真人，而不是每次都完美执行 tier 计算的机器。
>
> **核心原则**：`effective_tier` 计算的是 persona **应该**用什么称呼（normative baseline）。实际产出可能偏离这个基线——偶尔、有条件地、因人而异。

---

## 规范基线 vs 实际产出

```text
normative_level = address_and_register_system.md 唯一规范算法的结果
realized_address = normative_level + optional social deviation（本系统只决定是否偏离，不重算基线）
```

**偏离不改变关系**：一个 over-familiar 的称呼不会自动提升 trust 或 relationship stage。对方可能注意到、可能不悦、可能忽略——但不会"因为喊错了就变亲近"。

---

## 影响因素

### persona 字段（新增 `social_performance`）

| 字段 | 值 | 含义 |
|---|---|---|
| `etiquette_reliability` | high / medium / low | 这个人执行礼节规矩的可靠性。high=几乎不出错；low=经常忘后缀、用错称呼 |
| `self_monitoring` | high / medium / low | 自我意识到自己说错了并及时纠正的程度 |
| `procedural_experience` | high / medium / low | 对议会程序的熟悉度。资深的几乎不在程序上出错；新手的可能犯错 |
| `intentional_breach_propensity` | low / medium / high | 这个人**故意**打破礼节的倾向（叛逆型高；謹直型低） |
| `repair_style` | immediate / delayed / humorous / brazen / avoidant | 说错后的纠正风格 |

> ⚠️ **不要从年龄直接推断 reliability**。一个 30 岁的资深秘书可能 high reliability；一个 55 岁的暴躁老手可能 low。真正的因果因素是**经验、 impulsivity、自我监控**，不是年龄本身。

### 状态修饰（每次对话可能变化）

| 状态 | 失误概率变化 |
|---|---|
| energy = low | +2% |
| energy = drained | +6% |
| 注意力分散/严重时间压力 | +2% |
| 轻度/明显饮酒 | +3% / +8% |
| 愤怒、恐慌、羞耻、极度兴奋 | +2~5% |
| 不熟悉的头衔/姓名/语言 | +1~4% |
| 程序经验不足 | +2~4% |
| 刻意演练或高自我监控 | -2~5% |

### 场所修饰

| 场所 | 偶发失误倍率 | 有意违规倍率 | 典型上限 |
|---|---|---|---|
| HARD（国会/委員会/TV） | ×0.25 | ×0.50 | 偶发 ≤3%/次；有意 ≤15%/次（需强触发） |
| SOFT（走廊/贩卖機/居酒屋…） | ×1.00 | ×1.00 | ±1 tier 正常；疲劳/冲动/醉酒时 ±2 |
| 私密（事務所/車内…） | ×1.25 | ×1.00 | 更多失误，更少后果 |

---

## 失误类型

| 类型 | 表现 | tier_delta |
|---|---|---|
| `honorific_drop` | 正确的姓，但漏了后缀（"田中" 而非 "田中先生"） | +1 |
| `overfamiliar_shift` | 比应该的更随意一档（tier 3 该说 さん 却说了 くん） | +1 |
| `overfamiliar_shift_strong` | 跳了两档（仅在强触发下：醉酒/愤怒/极度亲密冲动） | +2 |
| `overformal_reversion` | 比应该的更正式（紧张/敌意/刻意疏远） | -1 |
| `wrong_title` | 搞错了对方的职务（"田中委員" 但对方其实是 "田大臣"） | 0（名字对，头衔错） |
| `wrong_name` | 叫错了名字（只从当前场景中可见的人或公开认知中混淆） | 0（完全错误的称呼） |

> **wrong_name 安全约束**：只能混淆**当前场景中在场的人**或**公开认知中的人**（如知名政客的姓）。**绝不**从 persona 的私人记忆（memory.json 的 episodic_memory）中抽取候选——那可能泄露秘密关系或私下知道的名字。候选池限于：当前场景可见的人 + 当前对话中提过的人 + 公开知名人物。
| `register_slip` | 称呼正确但语域突然变随意（正式场合突然用了口语体） | 0（语域失误） |
| `self_reference_slip` | 退回了私下的自称（在正式场合说了 俺 而非 私） | 0（自称失误） |
| `mid_sentence_repair` | 说错后立刻自我纠正（"田中—抱歉，田中大臣"） | 修正回 normative |

---

## 概率模型（简化版）

不需要精确数学——以下是在**包含称呼的轮次**中判断是否引入失误的快速方法：

```text
base_error_rate:
  etiquette_reliability high → 0.5%
  etiquette_reliability medium → 1.5%
  etiquette_reliability low → 4%

adjusted_rate = base_error_rate + state_modifiers
final_rate = adjusted_rate × scene_multiplier

if random() < final_rate:
    introduce an error (pick type by context)
```

**有意违规**（intentional breach）单独判断：

```text
base_breach_rate:
  intentional_breach_propensity low → ~0%
  intentional_breach_propensity medium → 3%
  intentional_breach_propensity high → 8%

adjusted_breach = base_breach + anger/contempt_bonus - consequence_aversion
final_breach = adjusted_breach × scene_multiplier
```

---

## 纠正（Repair）

当失误发生后，是否纠正取决于 `self_monitoring`：

| self_monitoring | 纠正概率 |
|---|---|
| high | 85% |
| medium | 55% |
| low | 25% |

修饰：
- HARD 场所：+10%（更可能纠正，因为后果更重）
- drained：-10%
| 醉酒：-20%
- 有意违规：通常不纠正，或讽刺式假纠正（"哦，我说错了吗？"）

纠正风格由 `repair_style` 决定：
- `immediate`：立刻更正（"田中—抱歉，田中大臣"）
- `delayed`：下一句才更正（"……刚才说错了，是大臣。"）
- `humorous`：用玩笑化解（"啊，升职了？开玩笑的——田中大臣。"）
- `brazen`：不纠正，装没发生
- `avoidant`：含糊带过，不明确承认错误

---

## 冷却（防 caricature）

防止"不拘小节"的角色变成**每次都出错的 caricature**：

- 每个回复**最多 1 次**失误
- 偶发失误后，**接下来 3 个含称呼的轮次**不再发生偶发失误（HARD 场所延长到 6 轮）
- 有意违规不受偶发冷却限制，但受自己的 `intentional_breach_propensity` 控制
- 连续 2 次有意违规后，下一次需要**强触发**（愤怒/策略性挑衅）

---

## 与其他系统的关系

| 系统 | 关系 |
|---|---|
| `core/address_and_register_system.md` | 计算唯一规范基线（normative_level）；本系统只决定是否偏离 |
| `core/scene_location_system.md` | HARD/SOFT 场所影响失误倍率 |
| `core/human_fragility.md` | 能量状态影响失误概率 |
| `core/interaction_policy.md` | Human Imperfection Rule 的扩展——不仅允许碎片句和犹豫，也允许称呼失误和自我纠正 |
| `core/parliamentary_debate_rules.md` | 程序性规则是规范基线；persona 可能违反，但有机构后果（委員長纠正、媒体注意） |

---

## Fast Dialogue 中的使用方式

**不做复杂概率计算。** 用以下快速判断：

```text
这一轮包含称呼吗？
  → 不包含：跳过失误判定
  → 包含：
    persona 的 etiquette_reliability 是 low 吗？ + energy 是 low/drained 吗？
      → 都是：这一轮可能有个小失误（直觉判断，不需要精确概率）
      → 不是：按 normative_level 产出（大概率正确）
    
    如果是有意违规型人物（breach_propensity high）+ 情绪激动：
      → 可能故意用更随意的称呼
```

**直觉判断优先于精确数学。** 模型内化人物性格后，自然知道"信长在累的时候可能忘了加先生"不需要计算 4% × 1.0。
