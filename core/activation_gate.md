# Persona Activation Gate

> This file is the single activation preflight used by the root skill, persona-local skills, generic invocation, demos, and game-driven activation.

## Canonical Status

`meta.json.latest_review_status` is the canonical activation status. Allowed values are:

- `unconfirmed`: generated or modified; activation is blocked.
- `reviewed`: review completed but user confirmation is still missing; activation is blocked.
- `confirmed`: reviewed and explicitly confirmed by the user; activation is allowed.

Two fields are persisted mirrors for artifact readability:

- `persona.yaml.meta.creation_review_status`
- `persona.yaml.source_provenance.last_review_status`

All three fields use the same enum and must be updated atomically. If a field is missing, invalid, or differs from the canonical value, fail closed as `unconfirmed`.

## Review Validity

User confirmation never substitutes for technical and safety review. Before confirmation can authorize activation, all of these must hold:

```text
review_valid = meta.json.validation_status == passed
            && meta.json.review_invalidated_by_modification == false
            && meta.json.reviewed_artifact_hash is a SHA-256 hash
            && reviewed_artifact_hash == current_artifact_hash
            && meta.json.safety_status in {PASS, safe_conversion}
            && persona.yaml.meta.safety_status == meta.json.safety_status
```

`current_artifact_hash` uses this byte-exact algorithm (reference implementation: `scripts/persona_runtime_contracts.py`):

1. Enumerate every regular file recursively under `persona_dir`, excluding only mutable `memory.json` and `relationship.json`. Reject a symlink or any path resolving outside `persona_dir`.
2. Sort by the UTF-8 byte sequence of the POSIX relative path.
3. For `persona.yaml`, parse YAML and serialize as UTF-8 JSON with sorted keys, no insignificant whitespace, and `ensure_ascii=false` after setting both review-status mirrors to `unconfirmed`.
4. For `meta.json`, parse and serialize the same way after setting `latest_review_status=unconfirmed`, `validation_status=pending`, `review_invalidated_by_modification=true`, and `reviewed_artifact_hash=""`.
5. For every other immutable file, use its raw bytes.
6. Feed SHA-256 the repeated byte framing `relative_path + NUL + content + NUL` in sorted order.

Mutable files are outside review identity but never outside validation: validate their strict schemas, persona identity, enum values, ranges, and record shapes after activation and before every read or write.

## Preflight

Run this before loading roleplay state, emitting a persona disclaimer, continuing a previous persona session, or producing a game action:

```text
compute review_valid
read meta.json.latest_review_status and both persona.yaml mirrors
if the three statuses disagree or a confirmed artifact has review_valid=false:
    atomically invalidate: unconfirmed + pending + invalidated + empty hash
    require technical/safety re-review; do not request confirmation
else if review_valid is false or status == unconfirmed:
    do not enter first-person roleplay
    do not emit the in-character one-time disclaimer
    require technical/safety re-review; do not request confirmation
else if review_valid is true and all three statuses == reviewed:
    present a concise creation_review.md summary
    ask for explicit confirmation or modification
else if review_valid is true and all three statuses == confirmed:
    activation may continue
else:
    fail closed and require re-review
```

Direct skill invocation is not confirmation. A request such as "talk to X now" is an activation request, not approval of the creation review.

The user sees a confirmation question only in the valid `reviewed` state. Invalid or unconfirmed artifacts route to re-review, never directly to confirmation.

## Transitions

- Creation or any persona-affecting modification: set all three activation fields to `unconfirmed`, set `validation_status=pending`, set `review_invalidated_by_modification=true`, and clear `reviewed_artifact_hash`.
- Successful technical/safety review: compute and store `reviewed_artifact_hash`, set `validation_status=passed`, set `review_invalidated_by_modification=false`, and set all three activation fields to `reviewed`.
- Explicit user approval is accepted only from a current `reviewed` state with `review_valid=true`; then transition all three activation fields to `confirmed` as one recoverable transaction. Confirmation does not alter validation or hash fields.
- If any write fails, leave or restore all three as `unconfirmed`; never partially confirm.

Because status mirrors span two files, "transaction" does not mean one filesystem write. Acquire a persona-local lock; write and fsync staged `meta.json` and `persona.yaml` files plus a transaction marker; atomically rename each staged file; fsync the directory; then remove the marker. On startup, a marker, a missing staged target, or mirror disagreement invalidates all statuses to `unconfirmed` before any activation. Hosts without equivalent crash-recovery semantics must not persist a confirmation transition.

`validation_status=passed` does not authorize activation by itself; it establishes review readiness. User confirmation is still required.
