# Changelog

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/).

This changelog is managed by [release-please](https://github.com/googleapis/release-please).

### Development history

The following work was completed before the first versioned release:

- Project scaffolding with uv, hatchling, ruff, pyright strict, mypy strict
- CI workflow (lint, typecheck, test matrix across Python 3.10-3.13)
- OpenAPI spec pinned to commit e614f35 (2026-11-21)
- 24 Pydantic v2 models generated from the Trigger.dev OpenAPI spec (Tier 1)
- 16 typed exception classes covering all HTTP status codes
- Sync Client with 22 endpoint methods across tasks, runs, and schedules
- 101 unit tests with full type coverage
- README with installation, quick start, and feature examples
