# Persona Path Resolver

Every workflow resolves a persona identifier to one explicit `persona_dir` before reading or writing files. Downstream code receives that directory and must not reconstruct a path from the slug.

## Canonical Roots

- Built-in read-only examples: `personas/examples/<persona_id>/`
- New user-generated personas: `user_generated/personas/<persona_id>/`

Managed `persona_id` values must match `[a-z0-9][a-z0-9_-]*`. They identify one direct child only; separators, `..`, absolute paths, symlinks, and ambiguous IDs present in both roots are rejected.

`personas/examples/` is never a generation target. `personas/generated/` and bare `personas/{slug}/` are not supported generation roots.

An embedding host may supply an explicit external `persona_dir` outside these roots. That is a supported host-managed mode, not a path inferred from `persona_id`. The host must enforce the same required-file, review, hash, and activation contracts; repository-wide validation cannot discover external directories automatically.

## Resolution

```text
if caller supplies persona_dir:
    require an existing non-symlink directory containing regular meta.json and persona.yaml files
else if persona_id exists under user_generated/personas:
    require one direct, contained, non-symlink child and use it
else if persona_id exists under personas/examples:
    require one direct, contained, non-symlink child and use it
else:
    report persona-not-found; do not guess another root
```

Repository-managed creation always allocates `user_generated/personas/<persona_id>/`. Host-managed creation may allocate an explicit external `persona_dir`. In both cases, pass that exact directory through source collection, generation, review, confirmation, invocation, game output, and writeback.

After resolution, require `persona_id == directory.name == meta.json.persona_id == meta.json.slug == persona.yaml.meta.persona_id == persona.yaml.meta.slug`. The executable reference implementation is `scripts/persona_runtime_contracts.py`; hosts must call it or reproduce its fail-closed behavior.

Validate any managed or external artifact with `uv run python scripts/validate_persona.py <persona_id> [--persona-dir <path>]`. External personas do not participate in repository discovery, so the embedding host must run this check explicitly before activation.
