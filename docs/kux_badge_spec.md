# K-UX Compliance Badge Specification

## Badge Name

**K-UX v1 — Deterministic Projection Certified**

## Scope

Badge attests that a K-UX projection implementation is replay-safe and projection-only under `kux://schema/v1`.

## Certification Requirements

1. Valid against `docs/kux.schema.json`.
2. `source.entropy == 0.21`.
3. `projection.layout == "deterministic"`.
4. `replay.replay_identity_required == true`.
5. `replay.hash_projection` reproducible from canonical projection inputs.
6. No async animation authority (`projection.animation.async == false` when present).
7. No runtime injection authority (`projection.styling.no_runtime_injection == true`).
8. No collapse modification fields or behavior.

## Badge Levels

### Bronze — Schema Conformant

- Schema-valid K-UX document.
- Deterministic projection declared.

### Silver — Replay Verified

- Projection hash reproducible across 3+ environments.

### Gold — Enforcement Sealed

- No animation authority.
- No projection mutation authority.
- Invariant surface displayed.
- Collapse trace integrity preserved.

## Badge Manifest

```json
{
  "badge": "KUX_v1_GOLD",
  "schema_version": "kux://schema/v1",
  "entropy_verified": true,
  "projection_hash_verified": true,
  "replay_identity_verified": true,
  "deterministic_render_verified": true
}
```
