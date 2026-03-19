# Phase 3: Framework Integration

> **Status**: Complete
> **Depends On**: Phase 2 — Infrastructure Adapters
> **Release**: v0.1.0

## Goal

Implement the Delivery Mechanism (API Layer) to expose the Domain Services to web frameworks, starting with FastAPI.

## Scope

### In Scope
- FastAPI Middleware: Intercepts requests, extracts tokens, calls `TokenService`
- FastAPI Dependencies: Injectable `UserContext` and `TenantContext`
- Exception Handlers: Maps `DomainError` to HTTP 401/403 responses
- Generic WSGI/ASGI helpers for reusable logic

### Out of Scope
- Flask and Django adapters (Phase 5)
- Advanced authorization policies (Phase 6)

## Key Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | FastAPI Middleware | `OpenShieldMiddleware` for request interception |
| 2 | Dependencies | `get_user_context`, `RequireScope`, `RequireRole` |
| 3 | Exception Handlers | Domain exceptions → HTTP 401/403 mapping |
| 4 | Example App | Working FastAPI example with full auth flow |

## Acceptance Criteria

- [x] `src/open_shield/api` package populated
- [x] Example FastAPI app working end-to-end
- [x] End-to-End tests using `TestClient`
- [x] Domain exceptions correctly mapped to HTTP responses
