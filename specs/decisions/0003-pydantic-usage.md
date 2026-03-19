---
id: "0003"
title: "Pydantic for Configuration and Validation"
status: accepted
date: 2026-02-12
deciders: Engineering Team
---

# ADR-0003: Pydantic for Configuration and Validation

## Status

`accepted`

## Context

The SDK configuration (Issuer URL, Audience, Algorithms) must be validated at startup to fail fast. We also need to parse and validate tokens and internal data structures reliably.

**Decision Drivers:**
- Validation: Need strong runtime validation of configuration and data
- DX: Python developers expect Pydantic models in modern libraries
- Env Var Support: Easy loading of settings from environment variables

## Decision

Use **Pydantic** and **pydantic-settings** for all configuration and data validation.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| Standard Library (os.getenv, dataclasses) | No dependencies | Manual validation, error-prone |
| marshmallow | Mature, flexible | Less common in modern Python, no env var support |
| Pydantic + pydantic-settings | Auto validation, type coercion, env vars, ecosystem standard | Adds runtime dependency |

## Consequences

**Good:**
- **Robustness**: Automatic type coercion and validation
- **Settings**: `pydantic-settings` handles env var loading out of the box
- **Ecosystem**: Defacto standard in modern Python (FastAPI, etc.)

**Bad:**
- **Dependency**: Adds a runtime dependency to the SDK (though it is lightweight and common)

## References

- [Pydantic](https://docs.pydantic.dev/)
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- Config: `src/open_shield/adapters/config.py`
