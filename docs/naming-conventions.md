# File & Folder Naming Convention

| Location | Convention | Examples |
|----------|-----------|---------|
| `specs/` — folders | `kebab-case` | `phase-0-init/`, `phase-5-flask-django/` |
| `specs/` — files | `kebab-case` | `0001-clean-architecture.md` |
| `docs/` — files | `kebab-case` | `developer-guide.md`, `naming-conventions.md` |
| `.claude/commands/` — files | `kebab-case` | `start-phase.md`, `sync-docs.md` |
| `.agent/` — files | `snake_case` or `kebab-case` | `project.md` |
| Root config files | `UPPERCASE` or tool default | `README.md`, `CLAUDE.md` |
| ADR files | `NNNN-kebab-title.md` | `0001-clean-architecture.md` |
| Phase directories | `phase-N-shortname` | `phase-0-init` |
| Date/changelog files | `YYYY-MM.md` | `2026-03.md` |
| Scripts | `kebab-case` | `check-history-reminder.sh` |
