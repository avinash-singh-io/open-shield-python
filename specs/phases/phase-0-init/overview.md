# Phase 0: Initialization

> **Status**: Complete
> **Depends On**: Nothing — this is the foundation
> **Release**: v0.1.0

## Goal

Set up the project repository, build system, and CI/CD pipeline using modern Python tooling (`uv`) and Clean Architecture structure.

## Scope

### In Scope
- Initialize Python project with `uv init`
- Configure `pyproject.toml` (Python 3.12+, ruff, mypy)
- Create folder structure (`src/open_shield/domain`, `adapters`, `api`)
- Set up GitHub Actions for CI (lint, test)

### Out of Scope
- Any business logic implementation
- External dependencies beyond build tooling

## Key Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | uv project | Managed project with `pyproject.toml` |
| 2 | Clean Architecture dirs | `domain/`, `adapters/`, `api/` structure |
| 3 | CI pipeline | GitHub Actions for linting and testing |

## Acceptance Criteria

- [x] `uv` project initializes and installs dependencies
- [x] `ruff check` and `mypy` pass with zero errors
- [x] GitHub Actions CI pipeline runs on push
- [x] Directory structure follows Clean Architecture pattern
