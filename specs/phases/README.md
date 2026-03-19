# Phases Index

> Quick reference for all phases. See [roadmap](../roadmap/roadmap.md) for timeline.

| Phase | Name | Status | Directory |
|-------|------|--------|-----------|
| 0 | Initialization | Complete | [phase-0-init/](phase-0-init/) |
| 1 | Domain Logic (Core) | Complete | [phase-1-core/](phase-1-core/) |
| 2 | Infrastructure Adapters | Complete | [phase-2-adapters/](phase-2-adapters/) |
| 3 | Framework Integration | Complete | [phase-3-integration/](phase-3-integration/) |
| 4 | Polish & Release | Complete | [phase-4-release/](phase-4-release/) |
| 5 | Flask & Django Adapters | Not Started | — |
| 6 | Advanced Authorization (OPA) | Not Started | — |
| 7 | Performance Optimization | Not Started | — |

## Phase Structure

Each phase directory contains:

| File | Purpose |
|------|---------|
| `overview.md` | Goal, scope, deliverables, acceptance criteria, exit criteria |
| `plan.md` | Implementation approach, module structure, risks |
| `tasks.md` | Detailed checklist with verification steps |
| `history.md` | Append-only log of decisions, scope changes, discoveries (drives /sync-docs) |
| `retrospective.md` | Post-completion review (created by /complete-phase) |

## Dependencies

```
Phase 0 (Initialization)
  └── Phase 1 (Domain Logic)
       └── Phase 2 (Adapters)
            └── Phase 3 (Framework Integration)
                 └── Phase 4 (Polish & Release)
                      ├── Phase 5 (Flask & Django)
                      ├── Phase 6 (Advanced Authorization)
                      └── Phase 7 (Performance)
```
