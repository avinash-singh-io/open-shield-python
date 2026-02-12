# Phase 1: Domain Logic (Core)

## Goal
Implement the pure business logic, entities, and interfaces (Ports) without any external dependencies or framework code.

## Scope
- [ ] Define **Entities** (Immutable `@dataclass`):
    - [ ] `User`, `Token`, `TenantContext`
- [ ] Define **Ports** (Abstract Base Classes):
    - [ ] `KeyProviderPort` (for JWKS retrieval)
    - [ ] `TokenValidatorPort` (for crypto validation)
- [ ] Implement **Domain Services**:
    - [ ] `TokenService`: Orchestrates validation using Ports.
    - [ ] `AuthorizationService`: Enforces Scope/Role policies.
- [ ] Define Domain Exceptions hierarchy.

## Deliverables
- [ ] `src/open_shield/domain` package populated.
- [ ] 100% test coverage for domain logic (using mocks for ports).
