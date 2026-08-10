# Testing Layers

The repository separates structural validation from semantic model execution.

## Structural Validation

```bash
uv run python scripts/validate_repo.py
```

This checks parseability, required files, cross-file persona fields, activation-state mirrors, runtime-card sections, scene/cache contracts, prompt shape, and deterministic game payloads. It does **not** invoke or grade an LLM and must not be cited as semantic dialogue evidence.

Validate one managed or explicit external persona with the shared artifact contract:

```bash
uv run python scripts/validate_persona.py <persona_id> --persona-dir <external-path>
```

For live game execution, use the full transaction gate, not the output-only helper:

```bash
uv run python scripts/validate_game_transaction.py --input event.json --output generated.json --persona-dir <external-path>
```

## Semantic Execution

`scripts/run_semantic_tests.py` is a provider-neutral command-adapter harness. Generator and judge commands are JSON arrays, receive JSON on stdin, and write to stdout. The judge must return:

```json
{"pass": true, "score": 90, "findings": []}
```

Example shape:

```bash
uv run python scripts/run_semantic_tests.py \
  --generator-command '["your-generator-adapter"]' \
  --judge-command '["your-judge-adapter"]' \
  --model-id exact-generator-model \
  --judge-model-id exact-judge-model \
  --runtime-id exact-host-version \
  --seed 0 \
  --category scene_aware
```

Each run writes an independent JSONL file under `quality/semantic-runs/` with timestamp, HEAD revision, full porcelain worktree status, repository content hash, prompt-suite hash, platform, exact commands, model/runtime identifiers, seed, prompts, referenced validator contents, raw outputs, stderr, return codes, durations, judge result, and summary. Adapters run with the repository root as their working directory. A run is semantic evidence only when those records exist; prompt definitions and historical Markdown reports alone are not execution evidence.

Use `--list` without adapters to inspect selected cases:

```bash
uv run python scripts/run_semantic_tests.py --list --category scene_aware
```
