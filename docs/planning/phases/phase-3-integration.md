# Phase 3: Framework Integration (API)

## Goal
Implement the Delivery Mechanism (API Layer) to expose the Domain Services to web frameworks.

## Scope
- [ ] **FastAPI Integration** (`src/open_shield/api/fastapi`):
    - [ ] `Middleware`: Intercepts requests, extracts tokens, calls `TokenService`.
    - [ ] `Dependencies`: Injectable `UserContext` and `TenantContext`.
    - [ ] `ExceptionHandlers`: Maps `DomainError` to HTTP 401/403.
- [ ] **Generic WSGI/ASGI Helpers**:
    - [ ] Reusable logic for extraction from WSGI/ASGI scopes.

## Deliverables
- [ ] `src/open_shield/api` package.
- [ ] Example FastAPI app.
- [ ] End-to-End tests using `TestClient`.
