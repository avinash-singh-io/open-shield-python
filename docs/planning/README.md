# Project Planning

This directory is the **Source of Truth** for all planning, architectural decisions, and tracking for `open-shield-python`.

## 📂 Structure

### [Specs](specs.md)
Detailed product specifications, functional and non-functional requirements.

### [Tasks](tasks.md)
**Active Task List**. This file tracks the granular progress of the project.
- [Phase 0: Initialization](phases/phase-0-init.md)
- [Phase 1: Domain Logic](phases/phase-1-core.md)
- [Phase 2: Infrastructure Adapters](phases/phase-2-authz.md)
- [Phase 3: Framework Integration](phases/phase-3-integration.md)
- [Phase 4: Polish & Release](phases/phase-4-publish.md)

### [Decisions (ADRs)](decisions/)
Architecture Decision Records explaining *why* we made certain choices.
- [001. Clean Architecture Adoption](decisions/001-clean-architecture.md)
- [002. Modern Tooling (uv, ruff)](decisions/002-modern-tooling.md)
- [003. Pydantic Usage](decisions/003-pydantic-usage.md)

### [Roadmap](roadmap.md)
High-level timeline and future milestones.

### [Tech Debt](tech-debt.md)
Tracked technical debt and cleanup items.
