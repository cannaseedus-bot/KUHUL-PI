# K-UX v1 Canonical Layer

**Identifier:** `kux://schema/v1`  
**Status:** `CANONICAL` + `FROZEN`  
**Authority:** Projection-only  
**Mutation:** Forbidden

## 1) Architectural Position

K-UX is above KUHUL π collapse and below host rendering surfaces.

```text
Micronaut  →  KUHUL π  →  K-UX  →  Host Surface
             (collapse)   (projection)
```

Directionality is one-way. K-UX does not feed authority back into Micronaut or KUHUL π.

## 2) Definition

> K-UX is the projection and interaction surface for KUHUL π collapse events,
> without altering enforcement semantics.

K-UX is a projection membrane, not an execution runtime.

## 3) Core Invariants

1. Read-only collapse consumption.
2. No authority escalation.
3. No mutation of execution state.
4. Projection-only operations.
5. Replay-identical rendering from identical collapse artifacts.

## 4) K-UX Formal Layer

```ebnf
KUX ::= "KUX" "{" ProjectionRules "}"

ProjectionRules ::=
      "render" CollapseResult
    | "display" CollapseTrace
    | "surface" Proof
    | "visualize" Entropy
```

No authority verbs are allowed.

## 5) Source Contract (Read-only)

K-UX consumes collapse artifacts only:

- `collapse_result_hash`
- `collapse_trace_hash`
- `entropy` (fixed at `0.21`)
- `invariants`
- `compression_ratio`

Constraints:

- Hashes must match KUHUL π output.
- Entropy must equal `0.21`.
- Invariants must be a subset of canonical invariants.
- No mutable references are permitted.

## 6) Projection Rules

Allowed projection modes:

- `svg`
- `dom`
- `css`
- `terminal`
- `canvas`

Rules:

- No async behavior.
- No timers.
- No state transitions.
- No user-triggered execution mutation.
- Animation disabled unless strictly derived from collapse trace timestamps.

## 7) SVG-3D Tensor Handling

SVG has two roles in the KUHUL ecosystem:

1. Execution geometry (headless computation substrate).
2. Optional projection overlay (explicitly requested).

Hard invariant:

> SVG defaults to computation. Rendering is explicit.

## 8) K-UX ↔ Micronaut Handshake

Micronaut may pass presentation context only:

- Theme (`dark | light | neutral`)
- Surface (`dashboard | panel | overlay`)
- Viewport dimensions

Micronaut may not pass:

- Collapse overrides
- Invariant toggles
- Entropy modifications
- Projection mutation flags
- Runtime scripts

Boundary conditions:

- Micronaut may SELECT / ARRANGE / CHOOSE presentation context.
- Micronaut may not alter collapse artifacts.
- Handshake is stateless per render.

## 9) Replay Identity Law

For identical collapse artifacts, K-UX must produce identical projection hashes.

Let:

- `C = collapse_result_hash`
- `T = collapse_trace_hash`
- `E = entropy`
- `I = invariant_set`

If:

```text
(C₁ == C₂) ∧ (T₁ == T₂) ∧ (E₁ == E₂) ∧ (I₁ == I₂)
```

Then:

```text
ProjectionHash₁ == ProjectionHash₂
```

Deterministic rendering requirements:

- No random numbers.
- No wall-clock timestamps.
- No viewport-driven layout drift.
- No host-dependent rendering variance.
- No nondeterministic CSS properties.

## 10) Projection Hash Definition

`ProjectionHash` is computed from canonical projection inputs only:

```text
hash(
  collapse_result_hash +
  projection.mode +
  canonical_layout +
  canonical_styles +
  invariant_surface
)
```

Host environment data must not be included.

## 11) Domain Boundary Summary

| Layer        | Can              | Cannot         |
|--------------|------------------|----------------|
| Micronaut    | Arrange context  | Enforce law    |
| KUHUL π      | Enforce collapse | Orchestrate    |
| K-UX         | Project output   | Modify collapse |
| Extrapolator | Expand narrative | Alter collapse |

All layers are orthogonal by law.

## 12) Canonical Statements

K-UX v1 is:

- Deterministic
- Replay-identical
- Projection-only
- Enforcement-sealed
- Micronaut-safe
- Extrapolator-compatible

K-UX adds no execution authority. It adds projection clarity.

## 13) Conformance + Badge Artifacts

- Authoritative schema: `docs/kux.schema.json`
- Deterministic reference verifier: `tools/kux_verify.py`
- Compliance badge specification: `docs/kux_badge_spec.md`

