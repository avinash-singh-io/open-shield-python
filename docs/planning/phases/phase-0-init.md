# Phase 0: Initialization

## Goal
Set up the project repository, build system, and CI/CD pipeline using modern Python tooling (`uv`) and Clean Architecture structure.

## Scope
- [ ] Initialize Python project with `uv init`
- [ ] Configure `pyproject.toml` with:
    - [ ] Python 3.12+ requirement
    - [ ] `ruff` for linting
    - [ ] `mypy` for typing
- [ ] Create folder structure:
    - [ ] `src/open_shield/domain` (Entities, Ports, Services)
    - [ ] `src/open_shield/adapters` (Implementations)
    - [ ] `src/open_shield/api` (Framework integrations)
- [ ] Set up GitHub Actions for CI (lint, test)

## Deliverables
- [ ] `uv` managed project structure.
- [ ] Clean Architecture directories established.
- [ ] CI pipeline running.
