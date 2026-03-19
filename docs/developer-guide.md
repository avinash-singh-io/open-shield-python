# Developer Guide

> How the spec-driven development system works for open-shield-python.

## Overview

This project uses a **spec-driven development system** where:

- Every phase of work is planned before coding starts
- Agents and developers share the same source of truth (`specs/`)
- The backlog, changelog, decisions, and status are always up to date
- Phase history captures decisions and discoveries as they happen
- Git discipline is automatic and consistent

## Quick Start

1. **Read `specs/status.md`** — always start here to understand current state
2. **Check `specs/backlog/backlog.md`** — for P0/P1 items before starting work
3. **Use slash commands** — `/start-phase`, `/complete-phase`, `/sync-docs`, `/log`, `/track`, `/review`

## Directory Structure

```
specs/
├── status.md           ← Current phase, blockers, P0 items (READ THIS FIRST)
├── backlog/            ← All bugs, features, tech debt, enhancements
├── changelog/          ← Monthly changelogs for phase work
├── decisions/          ← Architecture Decision Records (ADRs) + impact-map.json
├── phases/             ← Per-phase plans, tasks, history, retrospectives + index.json
├── roadmap/            ← Timeline and milestones
└── vision/             ← Charter, principles, success criteria
```

## The Development Cycle

```
1. DISCOVER    → Read status.md + backlog.md
2. PLAN        → Create/read phase plan.md
3. IMPLEMENT   → Write code, auto-update tasks + append to history.md
4. VERIFY      → Tests, validation, checks
5. SYNC        → /sync-docs (at phase completion)
6. RELEASE     → /complete-phase → tag → GitHub Release
```

## Slash Commands

| Command | Purpose |
|---------|---------|
| `/start-phase` | Begin a new implementation phase |
| `/complete-phase` | Verify, finalize, and release a completed phase |
| `/sync-docs` | Propagate phase history to relevant documents |
| `/log <message>` | Record a manual entry in phase history |
| `/track <item>` | Add a backlog item (bug, feature, tech debt, enhancement) |
| `/review` | Groom the backlog between phases |

## Phase History System

During implementation, changes are captured in `specs/phases/<phase>/history.md` as append-only entries. At phase completion, `/sync-docs` reads the history and propagates changes to relevant documents using two indexes:

- **`specs/phases/index.json`** — maps phases to topic keywords
- **`specs/decisions/impact-map.json`** — maps topics to affected documents

This ensures docs stay in sync without interrupting implementation flow.

## Naming Conventions

| Type | Prefix | Example |
|------|--------|---------|
| Bug | `BUG-` | `BUG-001` |
| Feature | `FEAT-` | `FEAT-003` |
| Tech Debt | `TD-` | `TD-002` |
| Enhancement | `ENH-` | `ENH-001` |

## Git Workflow

- Feature branches: `phase-N-shortname`, `feat/desc`, `fix/desc`, `refactor/desc`
- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `infra:`
- Never commit directly to `main` — always use branches
- Merge requires user approval: `phase-branch → staging → main → tag`
