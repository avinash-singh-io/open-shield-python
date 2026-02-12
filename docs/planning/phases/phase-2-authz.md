# Phase 2: Infrastructure Adapters

## Goal
Implement the concrete adapters for the ports defined in Phase 1. This layer handles IO, Cryptography, and Environment interactions.

## Scope
- [ ] Implement `KeyProviderPort` Adapter:
    - [ ] `OIDCDiscoKeyProvider`: Uses `httpx` to fetch JWKS.
- [ ] Implement `TokenValidatorPort` Adapter:
    - [ ] `PyJWTValidator`: Uses `PyJWT` for signature verification.
- [ ] Implement Configuration Adapter:
    - [ ] `EnvConfig`: Uses `pydantic-settings` to load config.
- [ ] Implement `ApiKeyRepoPort` Adapter:
    - [ ] `InMemoryApiKeyRepo` (for testing/dev).
    - [ ] Hashed storage adapter.

## Deliverables
- [ ] `src/open_shield/adapters` package populated.
- [ ] Integration tests for adapters (mocking external HTTP calls).
