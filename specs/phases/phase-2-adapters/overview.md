# Phase 2: Infrastructure Adapters

> **Status**: Complete
> **Depends On**: Phase 1 — Domain Logic
> **Release**: v0.1.0

## Goal

Implement the concrete adapters for the ports defined in Phase 1. This layer handles IO, Cryptography, and Environment interactions.

## Scope

### In Scope
- `OIDCDiscoKeyProvider`: Uses `httpx` to fetch JWKS
- `PyJWTValidator`: Uses `PyJWT` for signature verification
- `EnvConfig`: Uses `pydantic-settings` to load configuration
- `InMemoryApiKeyRepo` and hashed storage adapter

### Out of Scope
- Framework integration (Phase 3)
- Advanced policy engines

## Key Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | Key Provider | `OIDCDiscoKeyProvider` with JWKS caching |
| 2 | Token Validator | `PyJWTValidator` with RS256+ support |
| 3 | Config Adapter | `EnvConfig` via pydantic-settings |
| 4 | API Key Adapter | In-memory and hashed storage |

## Acceptance Criteria

- [x] `src/open_shield/adapters` package fully populated
- [x] Integration tests for adapters (mocking external HTTP calls)
- [x] JWKS caching implemented and tested
- [x] Configuration loads from environment variables
