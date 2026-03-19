# Project Rules: open-shield-python

> Claude Code configuration. Agent rules live in `.agent/rules/project.md` — do not modify.

## Navigation (Where to Find Things)

| Question | File |
|----------|------|
| Current state / what phase? | `specs/status.md` |
| What's in the backlog? | `specs/backlog/backlog.md` |
| Phase tasks/progress? | `specs/phases/phase-N-*/tasks.md` |
| Why was X chosen? | `specs/decisions/NNNN-*.md` |
| Overall timeline? | `specs/roadmap/roadmap.md` |
| How this system works? | `docs/developer-guide.md` |

> **First file to read: ALWAYS `specs/status.md`.**

---

## Autonomous Behaviors (Always-On Rules)

### Rule 1: Always Orient First

Before ANY work, read `specs/status.md`. This tells you:
- What phase is active
- What's blocking progress
- What P0 items need attention

### Rule 2: Auto-Update Tracking After Changes

After completing ANY meaningful work, automatically update:

1. **Active phase `tasks.md`** — mark completed `[x]`, in-progress `[/]`
2. **`specs/status.md`** — if phase progress, blockers, or P0 items changed
3. **`specs/changelog/YYYY-MM.md`** — log what changed (one line per change)

Use the built-in **TodoWrite** tool to track in-session task progress. Do NOT wait for the user to ask you to update tracking.

### Rule 3: Auto-Track Discoveries

When you discover a bug, tech debt, or enhancement during work:
- Add it to `specs/backlog/backlog.md` immediately with appropriate priority
- Mention it to the user: "I found [issue] and added it as [ID] to backlog"

### Rule 4: Pre-Phase Bug Check

Before starting work on a new phase:
- Scan `specs/backlog/backlog.md` for P0/P1 bugs
- If any exist, recommend addressing them first
- Present: "N open bugs (X critical), recommend fixing before proceeding"

### Rule 5: Phase Boundary Awareness

When completing the last task in a phase:
- Prompt the user: "All tasks in Phase N are complete. Run `/complete_phase` to verify and release?"
- Do NOT auto-complete a phase without user confirmation

### Rule 6: Git Lifecycle (Automatic)

#### Starting Work
- **Before ANY code change**, check current branch
- If on `main` or `staging`, **auto-create a feature branch**:
  - Phase work: `phase-N-shortname`
  - Bug fix: `fix/BUG-NNN-short-desc`
  - Feature: `feat/short-desc`
  - Tech debt: `refactor/TD-NNN-short-desc`

#### During Work
- **Auto-commit** after each logical unit with conventional commits:
  - `feat(scope):` | `fix(scope):` | `infra(scope):` | `docs:` | `refactor(scope):` | `chore:`
- Keep commits atomic — one logical change per commit
- Push to remote after significant milestones

#### Completing Work
- Commit all remaining changes, push branch
- **ASK the user** before merging to `staging` or `main` — never auto-merge to protected branches

| Action | Auto? | Requires Approval? |
|--------|-------|-------------------|
| Create feature branch | Yes | No |
| Commit to feature branch | Yes | No |
| Push feature branch | Yes | No |
| Merge to `staging` | No | **Yes** |
| Merge to `main` | No | **Yes** |
| Tag a release | No | **Yes** |
| Delete branch after merge | Yes | No |

### Rule 7: Plan Before Implementing

For any non-trivial implementation (new module, phase start, architectural change):
- Use built-in plan mode to design the approach first
- Present the plan for user approval before writing code

### Rule 8: Record Phase History

During any active phase, after making a meaningful change, append an entry to the phase's history file (`specs/phases/<active-phase>/history.md`).

**What counts as meaningful:**
- An ADR was created or its status/decision changed → `[DECISION]`
- Phase scope was added to or reduced → `[SCOPE_CHANGE]`
- A bug, tech debt, or enhancement was added to backlog → `[DISCOVERY]`
- A new feature was added to the phase plan → `[FEATURE]`
- An architectural pattern or integration approach changed → `[ARCH_CHANGE]`

**Entry format (APPEND ONLY — never edit existing entries):**
```
### [TYPE] YYYY-MM-DD — Short title
Topics: topic-1, topic-2
Affects-phases: phase-N-name (or "none")
Affects-docs: path/to/doc.md#section (or "none")
Detail: One to three sentences describing what changed and why.

---
```

**After writing the entry**, check `specs/decisions/impact-map.json` — if the entry's topics aren't there, add them.

> The hook (`scripts/check-history-reminder.sh`) will also remind you if you forget.

### Rule 9: Doc Sync Protocol — Never Mid-Phase, Always at Completion

- **During a phase**: Do NOT update other docs to reflect changes. Just record to history. Stay focused on implementation.
- **Exception**: Direct doc-only tasks (user explicitly asked to update a doc) are fine.
- **At phase completion**: Run `/sync-docs` BEFORE running `/complete-phase`. This propagates all history-recorded changes to relevant docs in a single targeted pass.

---

## Naming Conventions

### Backlog IDs
| Type | Prefix | Example |
|------|--------|---------|
| Bug | `BUG-` | `BUG-001` |
| Feature | `FEAT-` | `FEAT-003` |
| Tech Debt | `TD-` | `TD-002` |
| Enhancement | `ENH-` | `ENH-001` |

### Priorities
| Level | Meaning | SLA |
|-------|---------|-----|
| `P0` | Critical — blocks current phase | Address immediately |
| `P1` | High — important | Current/next phase |
| `P2` | Medium | Within 2 phases |
| `P3` | Low — nice to have | When convenient |

### Git Branches
| Type | Pattern | Example |
|------|---------|---------|
| Phase | `phase-N-shortname` | `phase-5-flask-django` |
| Feature | `feat/description` | `feat/opa-integration` |
| Bug fix | `fix/description` | `fix/jwks-cache-ttl` |
| Refactor | `refactor/description` | `refactor/module-cleanup` |

### Git Commits (Conventional)
`feat:` | `fix:` | `docs:` | `refactor:` | `chore:` | `infra:`

---

## Constraints

1. **No secrets in code** — All credentials via environment variables
2. **Never commit to main** — Always use feature/phase branches
3. **Plan before implementing** — Use plan mode for non-trivial work
