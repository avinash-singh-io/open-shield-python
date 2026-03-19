# Phase 1: Domain Logic (Core)

> **Status**: Complete
> **Depends On**: Phase 0 — Initialization
> **Release**: v0.1.0

## Goal

Implement the pure business logic, entities, and interfaces (Ports) without any external dependencies or framework code.

## Scope

### In Scope
- Define Entities (immutable dataclasses): `User`, `Token`, `TenantContext`
- Define Ports (Abstract Base Classes): `KeyProviderPort`, `TokenValidatorPort`
- Implement Domain Services: `TokenService` (orchestrator), `AuthorizationService`
- Define Domain Exceptions hierarchy

### Out of Scope
- Any IO, network calls, or framework code
- Concrete adapter implementations

## Key Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | Entities | `User`, `Token`, `TenantContext` dataclasses |
| 2 | Ports | `KeyProviderPort`, `TokenValidatorPort` ABCs |
| 3 | Services | `TokenService`, `AuthorizationService` |
| 4 | Exceptions | Domain exception hierarchy |

## Acceptance Criteria

- [x] `src/open_shield/domain` package fully populated
- [x] 100% test coverage for domain logic (using mocks for ports)
- [x] No external dependencies in domain layer
- [x] All ports defined as abstract base classes
