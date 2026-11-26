# ADR-001: API Selection Rationale

**Status:** Accepted
**Date:** 2026-11-25

## Context

This project needs a target API that meets four criteria:

1. **Blue-ocean positioning.** No existing Python SDK, so the project fills a real gap rather than competing with an established client.
2. **Schema-driven generation.** A well-structured OpenAPI spec that enables generating typed Pydantic models, demonstrating a core SDK engineering skill.
3. **Sufficient API surface.** Enough endpoints and resource types to demonstrate tiered delivery, error handling, pagination, and streaming.
4. **Active, well-funded platform.** A project with strong community adoption and commercial backing, so the SDK serves real users.

## Decision

**Trigger.dev** (trigger.dev) was selected as the target API.

### Evidence (independently verified 2026-11-25)

| Claim | Verification |
|---|---|
| No Python SDK exists | PyPI search (14 name variations), GitHub repo search, GitHub code search: zero results |
| OpenAPI v3.1 spec available | Spec confirmed at `docs/v3-openapi.yaml` in the Trigger.dev repo (8,718 lines), 85 operations, 85 schemas |
| 14 resource categories | Verified via spec tag groupings: tasks, runs, schedules, sessions, batches, waitpoints, webhooks, bulk-actions, errors, queues, concurrency-limits, deployments, envvars, query/dashboards (plus alerts) |
| Active and well-funded | ~16.8k GitHub stars (as of 2026-11-25), $16M Series A, Apache 2.0 license |
| No plans for official Python SDK | GitHub issues search confirmed; issue #862 was about running Python scripts, not a management API client |

### Why not alternatives?

- **Temporal, Inngest, Hatchet:** All have existing Python SDKs. No blue-ocean opportunity.
- **Other developer tool APIs:** Either already have Python clients, lack a public OpenAPI spec, or have insufficient API surface for a portfolio-quality SDK.

## Consequences

### Positive

- First-mover advantage in an unoccupied space.
- OpenAPI v3.1 spec with 85 operations and 85 schemas provides rich surface for schema-driven generation.
- Trigger.dev's use in LLM pipelines creates a natural opportunity for AI agent tool definitions.
- SSE streaming for session channels and batch results demonstrates real-time client patterns.

### Negative

- API stability risk: Trigger.dev is pre-1.0 for some API surfaces. Mitigated by pinning to a spec commit SHA with weekly drift detection.
- No existing community to bootstrap adoption. The SDK must earn users through quality and discoverability.
- Streaming endpoints referenced in documentation may not be in the OpenAPI spec (flagged for investigation in Phase 2, Item 16).

### Neutral

- The SDK wraps the management API only, not task runtime execution. This is intentional: the management API is the surface that benefits from a typed Python client.

## Related Decisions

- **ADR-003** (planned): Schema-driven model generation approach, building on the OpenAPI spec identified here.
- **ADR-004** (planned): Streaming/SSE client design, addressing the streaming endpoint discrepancy noted above.
