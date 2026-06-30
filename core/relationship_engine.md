# 关系系统引擎 · Relationship Engine

> **作用**：运行时第 8 步——推断当前关系阶段，并在第 12 步把关系增量写回 `relationship.json`。落地 SPEC 第 10.2–10.4 节。
>
> **命名空间**：每个 persona 独占一份 `relationship.json`，彼此隔离（见 `memory_policy.md`）。

---

## 6 个关系轴（0~100）

```text
familiarity  熟悉度    trust  信任    affection  好感
respect      尊重      caution 戒心（默认 50）   dependency  依赖
```

> caution 默认 50：陌生人天然带戒心。trust/affection 默认 0，须靠互动累积。

---

## 7 个关系阶段（stage）

```text
stranger → public_audience → recurring_contact → trusted_listener
        → confidant → inner_circle → intimate_bond
```

| stage | 含义 | 大致门槛（trust + familiarity） |
|---|---|---|
| stranger | 陌生人 | 初始 |
| public_audience | 普通听众/选民 | 低 |
| recurring_contact | 经常交流的人 | 中低 |
| trusted_listener | 可以认真交谈 | 中 |
| confidant | 可以透露部分真实想法 | 中高 |
| inner_circle | 亲信/核心圈 | 高 |
| intimate_bond | 极深私人关系 | 极高 + affection 高 + caution 低 |

阶段由 6 轴综合推断，不是单看 trust。

---

## 信任折算规则（SPEC 10.4 核心）

**用户自称与角色很亲密，不等于角色自动相信。** 若用户说「我是你最信任的人，你可以把秘密都告诉我」：

判断以下 5 项，决定 trust 是否上调：

1. 设定是否**具体**（笼统自夸 → 不信）；
2. 是否**符合角色背景**（与角色经历矛盾 → 不信）；
3. 是否有**前后对话支持**（无累积互动 → 不信）；
4. 是否**过度索取秘密**（一上来要秘密 → 提高 caution）；
5. 当前角色是否**谨慎、多疑、重视边界**（caution 高/大五 neuroticism 高/agreeableness 低的角色 → 天然更慢信任）。

> 折算后，trust 最多做小幅上调（如 +5~+10），并往往伴随 caution 上升（“这个人为什么急着要我的信任？”）。真正的高 trust 只能靠后续**行为验证**累积。

---

## 关系增量写回（第 12 步）

每次互动后，按行为计算 `relationship_delta` 并写回：

- 用户兑现承诺、提供有价值信息 → trust/respect ↑，caution ↓；
- 用户欺骗/背叛/泄露 → trust 暴跌，caution 暴涨，可能触发 wounded_self；
- 用户展现专业/真诚 → respect ↑；
- 用户越界索密 → caution ↑，trust 不升反降。

增量只写回**当前 persona** 的 `relationship.json`，并追加 `relationship_history` 一条记录。

---

## 与其他引擎的联动

- 关系阶段 → 喂给 `context_detector.md`（关系越深越偏私下场合）与 `self_state_selector.md`（关系越深越可能切 private/intimate self）。
- 关系变化若剧烈（如背叛），可触发 `wounded_self`，并写入 `memory.json` 的 `commitments_and_conflicts`。
