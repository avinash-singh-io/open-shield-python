# Open Shield Python SDK

[![CI](https://github.com/prayog-ai-labs/open-shield-python/actions/workflows/ci.yml/badge.svg)](https://github.com/prayog-ai-labs/open-shield-python/actions/workflows/ci.yml)

Vendor-agnostic authentication and authorization enforcement SDK for Python.

Open Shield allows you to enforce authentication (AuthN) and authorization (AuthZ) in your Python applications without tightly coupling your code to a specific identity provider (like Auth0, Keycloak, or Cognito).

## Features

- **Vendor Neutral**: Works with any OIDC-compliant provider.
- **Framework Agnostic**: Core logic is pure Python; first-class support for **FastAPI**.
- **Clean Architecture**: Domain logic is isolated from infrastructure concerns.
- **Type Safe**: Fully typed and checked with `mypy`.
- **Automatic JWKS Rotation**: Fetches and caches keys from your provider's OIDC discovery endpoint.

## Installation

```bash
pip install open-shield-python
```

## Quick Start (FastAPI)

1. **Configure Environment**

Set the following environment variables:

```bash
OPEN_SHIELD_ISSUER_URL=https://your-auth-domain.com/realms/myrealm
OPEN_SHIELD_AUDIENCE=my-api-identifier
```

2. **Add Middleware**

```python
from fastapi import FastAPI, Depends
from open_shield.api.fastapi import OpenShieldMiddleware, get_user_context, RequireScope, RequireRole
from open_shield.adapters import OpenShieldConfig
from open_shield.domain.entities import UserContext

app = FastAPI()

# Load config from environment
config = OpenShieldConfig()

# Add global authentication middleware
app.add_middleware(OpenShieldMiddleware, config=config)

# Public route (excluded by default: /docs, /openapi.json, /redoc, /health)
@app.get("/health")
def health():
    return {"status": "ok"}

# Protected route (Authentication required)
@app.get("/users/me")
def read_current_user(context: UserContext = Depends(get_user_context)):
    return {
        "id": context.user.id,
        "email": context.user.email,
        "roles": context.user.roles
    }

# Scoped route (Authorization required)
@app.get("/admin/dashboard")
def admin_dashboard(context: UserContext = Depends(RequireScope("read:admin"))):
    return {"data": "secret admin data"}

# Role-based route
@app.get("/manager/reports")
def reports(context: UserContext = Depends(RequireRole(["manager", "admin"]))):
    return {"reports": []}
```

## Architecture

This SDK follows **Clean Architecture** principles:

- **Domain Layer**: Pure Python logic, entities, and interfaces (Ports). Zero external dependencies.
- **Adapters Layer**: Concrete implementations of Ports (e.g., `PyJWT` for validation, `httpx` for JWKS).
- **API Layer**: Framework specific glue code (e.g., FastAPI Middleware).

## configuration

| Environment Variable | Description | Default |
|----------------------|-------------|---------|
| `OPEN_SHIELD_ISSUER_URL` | OIDC Issuer URL (required) | - |
| `OPEN_SHIELD_AUDIENCE` | Expected audience (`aud` claim) | None |
| `OPEN_SHIELD_ALGORITHMS` | Allowed signing algorithms | `["RS256"]` |
| `OPEN_SHIELD_REQUIRE_SCOPES` | Enforce scope presence | `True` |

## Development

This project uses `uv` for dependency management.

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Lint and Format
uv run ruff check .
```
