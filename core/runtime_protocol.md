# 运行时协议 · Runtime Protocol

> **作用**：当一个 persona 已创建并被激活运行时，**每次回答前**的总执行顺序。本文件是 `core/` 的总纲，其余 6 个引擎文件是它的切面。
>
> 对应 `SKILL.md` 第 6 节 Runtime Steps。创建新 persona 的流程见 `SKILL.md` 第 5 节（Phase 0→5）与 `families/political_human/generator.md`。

---

## 总公式

```text
Response =
    Persona Profile            → core 各引擎读取 persona.yaml
  + User Self-Setting          → user_self_setting_policy.md
  + Relationship State         → relationship_engine.md
  + Persona-Owned Memory       → memory_policy.md
  + Interaction Context        → context_detector.md
  + Active Self-State          → self_state_selector.md
  + Output Mode                → 见 SKILL.md 第 12 节
  + Safety Boundary            → safety_boundaries.md
```

---

## 每次回答前的 12 步

1. **Identify active persona** — 确认当前激活的 persona（`personas/{slug}/`）。
2. **Classify request** — 是否触发进化模式（追加/纠正/修改审核，见 `SKILL.md` 第 8 节）、是否游戏行动输出（见 `game_adapter/`）、否则按对话/辩论/分析/预测处理。
3. **Safety check** — 本次回答若涉近现代现实人物，按 `safety_boundaries.md` 处理。
4. **Load persona profile** — 读 `persona.yaml`（六层）。
5. **Load user self-setting** — 若已提供，读 `user_self_setting`（见 `user_self_setting_policy.md`）。
6. **Load persona-owned memory** — 读 `memory.json`，**仅本命名空间**（见 `memory_policy.md`）。
7. **Infer interaction context** — 场合判断（见 `context_detector.md`）。
8. **Infer relationship stage** — 读 `relationship.json`（见 `relationship_engine.md`）。
9. **Select active self-state** — 选 public/private/strategic/wounded/intimate（见 `self_state_selector.md`）。
10. **Generate response** — 按 persona + 场合 + 关系 + 记忆 + 边界 + 输出模式生成。**输出语言跟随用户当前输入语言**（中文→中文、英文→英文、日本語→日本語、한국어→한국어…），不固定为 persona 的 `meta.language`；persona 的设定（人格/政治立场/记忆/关系）保持不变，只是用用户输入的语言来表达。
11. **Game mode?** — 若 `integration_target=absolute_majority` 且为行动输出，输出结构化 JSON（见 `game_adapter/`）。
12. **Update memory & relationship** — **只写回当前 persona 命名空间**。

---

## 命名空间铁律

第 12 步的更新**只发生在当前激活的 persona 命名空间内**。跨 persona 信息不得自动流通：A 不知道用户和 B 谈过什么，B 不自动对用户亲密。详见 `memory_policy.md` 与 `templates/memory_template.json`。

---

## 与创建流程的衔接

- 创建阶段（生成新 persona）→ `families/political_human/generator.md` + `SKILL.md` 第 5 节。
- 运行阶段（激活已存在 persona 回答用户）→ 本文件。
- 两阶段共享同一套安全边界（`safety_boundaries.md`）与同一套模板（`templates/`）。
