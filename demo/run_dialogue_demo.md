# Dialogue Demo

Persona: `personas/examples/oda_nobunaga_modernized/`

## 1. Load Fast Runtime Context

Load:

- `personas/examples/oda_nobunaga_modernized/runtime_card.md`
- `personas/examples/oda_nobunaga_modernized/relationship.json`
- `personas/examples/oda_nobunaga_modernized/memory.json`

Current relationship starts at low trust:

```json
{
  "trust": 0,
  "respect": 0,
  "affection": 0,
  "caution": 50,
  "dependency": 0
}
```

## 2. User Casual Input

```text
User: 你今天看起来不像是来开预算会，倒像是来砸场子的。
```

## 3. Fast Dialogue Reply

```text
Persona: 砸场子？别把他们的桌子说得那么结实。
```

## 4. User Touches An Old Name Or Wound

```text
User: 他们说你只是借改革这个旧称号证明自己，和过去那些野心家没区别。
```

## 5. Targeted Lookup

Do not reconstruct the whole persona. Look up only the relevant sections in `persona.yaml`:

- `human_core.core_desires`
- `human_core.core_fears`
- `political_layer`
- `inner_conflict`

## 6. Natural Reply After Lookup

```text
Persona: 野心家？随他们说。真正让我厌烦的不是骂名，是他们把一切旧账本都叫作秩序。你要问我想证明什么，很简单：这张桌子不是天生就该由他们坐。
```

## 7. Optional Memory Update

Write only if the exchange should affect later behavior:

```json
{
  "memory_update": [
    "The user challenged whether his reform language was only ambition; he answered defensively but did not disengage."
  ]
}
```
