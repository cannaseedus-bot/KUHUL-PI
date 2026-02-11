# KUHUL π Canonical Merge Note (v1.1)

## Current Layers

- **π-1.0.0**: Minimal collapse calculus (pure execution grammar).
- **v1.1 canonical grammar**: Architectural boundary and enforcement partition.

These layers are compatible because they operate at different abstraction depths.

## What v1.1 Adds

v1.1 does not extend π execution semantics. It adds:

1. Architectural separation law.
2. Micronaut / KUHUL π orthogonality formalization.
3. Extrapolator quarantine.
4. Explicit enforcement-domain boundary.

## Invariant Compatibility

The v1.1 grammar preserves the π-1.0.0 invariants:

- `collapse_only`
- `field_perception`
- `compression_law`
- `unreachable_states`
- `entropy_constancy` (`0.21`)

No execution power is added (no branching, mutation, loops, dynamic dispatch, or authority escalation).

## Frozen Constraints

The following must remain frozen after merge:

- No branching keywords.
- No conditional constructs.
- No loops.
- No dynamic dispatch.
- No runtime authority injection.
- No cross-domain execution.

Domain constraints:

- **Micronaut** remains orchestration-only (non-enforcing, non-collapsing).
- **KUHUL π** remains enforcement and collapse only.
- **Extrapolator** remains read-only, non-authoritative, and outcome-agnostic.

## Formal Canonical Statement

> KUHUL π is a deterministic collapse enforcement layer.  
> Micronaut is a non-authoritative orchestration layer.  
> Extrapolator is a non-authoritative expansion layer.  
> These domains are orthogonal and irreversible.

Invariant continuation:

> Execution collapse is singular and immune to orchestration or extrapolation.

## Kernel Source Link

For full kernel context (Micronaut + KHL), use `sw.khl` in this repository.

External source reference:
`https://raw.githubusercontent.com/cannaseedus-bot/KUHUL-PI/refs/heads/main/sw.khl`

