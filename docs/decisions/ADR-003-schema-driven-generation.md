# ADR-003: Schema-Driven Model Generation

**Status:** Accepted
**Date:** 2026-11-26

## Context

The SDK needs Pydantic v2 models for all 85 component schemas in the Trigger.dev OpenAPI v3.1 spec. These models must pass pyright strict and mypy strict with zero `Any` in the public API surface.

Three approaches were evaluated:

1. **datamodel-code-generator** (open-source, purpose-built for OpenAPI to Pydantic)
2. **Custom generation script** (read YAML, emit Python directly)
3. **Manual translation** (hand-write every model from the spec)

Model SDK repos (anthropic-sdk-python, openai-python, stripe-python) all use proprietary generators (Stainless, Codegen) unavailable to us. All three follow a "generate then hand-tune" pattern: generated types live in a types directory, hand-written code lives separately.

## Decision

**Use datamodel-code-generator for baseline generation, then hand-tune for SDK ergonomics.**

### Evidence

datamodel-code-generator v0.102.0 was tested against our pinned spec (`spec/v3-openapi.yaml`):

| Metric | Result |
|---|---|
| Classes generated | 129 (85 component schemas + 44 inline request/response schemas) |
| Lines of code | 2,981 |
| pyright strict | 0 errors |
| mypy strict | 0 errors |
| `dict[str, Any]` occurrences | 13 (all from spec's `additionalProperties: true`, spec-accurate) |
| Bare `Any` | 1 (to be eliminated in hand-tuning) |
| Enum handling | `Literal` types (idiomatic) |
| Union handling | `RootModel` wrappers for type aliases (14 instances, simplifiable) |

### Pipeline

1. **Generate.** Run datamodel-code-generator against the pinned spec with Pydantic v2 output targeting Python 3.10. The generation command is stored in `scripts/generate_models.sh` for reproducibility.

2. **Split.** Reorganize the single output file into per-resource modules under `src/triggerdev/types/` (e.g., `runs.py`, `tasks.py`, `schedules.py`), matching the spec's tag groupings.

3. **Hand-tune.** For each module:
   - Rename models for SDK ergonomics (e.g., `ListRunsResponse` not `ListRunsResponseBody`)
   - Replace `RootModel` wrappers with type aliases where appropriate
   - Eliminate any bare `Any` (replace with `object` or typed alternatives)
   - For `dict[str, Any]` from the spec's `additionalProperties: true`: keep as a scoped exception (see note below under Consequences)
   - Add `__all__` to each module
   - Add re-exports in `src/triggerdev/types/__init__.py`

Hand-tuned models are committed to version control as source code, not regenerated at build time. This matches model repo practice (anthropic-sdk-python commits `src/anthropic/types/`) and ensures reproducible installs without build-time dependencies.

4. **Verify.** Run pyright strict, mypy strict, and ruff against the tuned models. All must pass with zero errors.

5. **On spec updates.** When the pinned spec is updated (via drift detection):
   - Re-generate baseline from the new spec
   - Diff generated output against the current hand-tuned models
   - Merge changes manually, preserving ergonomic adjustments
   - This is expected to take 1-2 hours per update cycle

### File layout

```
src/triggerdev/types/
    __init__.py          # Re-exports all public types
    tasks.py             # Task, TaskListResponse, TriggerTaskRequest, ...
    runs.py              # Run, RunListResponse, RunEvent, ...
    schedules.py         # Schedule, ScheduleListResponse, ...
    shared.py            # Common types used across resources
scripts/
    generate_models.sh   # Reproducible generation command
```

## Consequences

### Positive

- Mechanical schema translation is automated (2,981 lines of model code from one command).
- Type checker compliance is guaranteed at generation time (0 errors from both pyright and mypy).
- Reproducible: any developer can re-generate from the pinned spec.
- Matches the "generate then hand-tune" pattern used by model SDK repos.

### Negative

- Spec updates require a manual merge step (re-generate, diff, merge). This is intentional: hand-tuned ergonomics should not be overwritten by re-generation.
- datamodel-code-generator is a build-time dependency (dev only, not shipped to users).
- Generated output includes inline schemas (44 beyond the 85 component schemas). Some may be unnecessary after hand-tuning.

### Neutral

- **Scoped exception for `dict[str, Any]`:** oss_practices.md specifies "zero `Any` in public API surfaces." The 13 `dict[str, Any]` occurrences are a deliberate exception: they come from the spec's `additionalProperties: true` fields, where the API genuinely accepts arbitrary JSON. Using `dict[str, object]` would force callers to cast every value, degrading ergonomics without adding safety (the API accepts any JSON value). This exception applies only to spec-mandated `additionalProperties` fields; all other `Any` (including the 1 bare occurrence) will be eliminated during hand-tuning.

## Related Decisions

- **ADR-001**: API selection rationale (the spec this generation targets).
- **ADR-002** (planned): Sync/async strategy (how generated models are used by the client).
