---
id: "0002"
title: "Modern Python Tooling Stack"
status: accepted
date: 2026-02-12
deciders: Engineering Team
---

# ADR-0002: Modern Python Tooling Stack

## Status

`accepted`

## Context

We need a robust, fast, and standard way to manage dependencies, enforce code quality, and ensure type safety for `open-shield-python`. The Python ecosystem has many tools (`pip`, `poetry`, `flake8`, `black`, `isort`), leading to fragmentation and slow CI pipelines.

**Decision Drivers:**
- Speed: CI and local install times should be minimal
- Consistency: Linting and formatting should be uniform
- Type Safety: The SDK is a library; strict typing is essential for user experience (IntelliSense)

## Decision

Adopt the **Modern Stack**: `uv` for dependency management, `ruff` for all-in-one linting/formatting, `mypy` for type checking.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| Legacy Stack (pip + requirements.txt, flake8, black) | Widely known | Slow, fragmented config |
| Poetry Stack (poetry, black, isort) | Good dependency resolution | Slower than uv, multiple tools |
| Modern Stack (uv, ruff, mypy) | Fastest, single config, future-proof | uv is relatively new |

## Consequences

**Good:**
- **Performance**: `uv` is significantly faster than pip/poetry. `ruff` replaces 10+ linting tools with extreme speed
- **Simplicity**: Fewer config files (`pyproject.toml` handles almost everything)
- **Future-proof**: Aligns with modern Python engineering standards

**Bad:**
- **Newness**: `uv` is relatively new, though rapidly maturing and stable for our needs

## References

- [uv](https://github.com/astral-sh/uv)
- [ruff](https://github.com/astral-sh/ruff)
- Config: `pyproject.toml`
