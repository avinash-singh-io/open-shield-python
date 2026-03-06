# Open Shield Python SDK

[![CI](https://github.com/avinash-singh-io/open-shield-python/actions/workflows/ci.yml/badge.svg)](https://github.com/avinash-singh-io/open-shield-python/actions/workflows/ci.yml)

Vendor-agnostic authentication and authorization enforcement SDK for Python.

Open Shield lets you enforce authentication (AuthN) and authorization (AuthZ) in your Python applications without coupling to a specific identity provider. Works with **Logto**, **Keycloak**, **Auth0**, **Entra ID**, **Cognito**, or any OIDC-compliant provider.

## Features

- **Vendor Neutral** — Works with any OIDC-compliant identity provider
- **Configurable Claim Mapping** — Map any JWT claim to user/tenant/role fields
- **3-Step Tenant Cascade** — Correct isolation for individual users, SaaS orgs, and M2M clients
- **Actor Type Inference** — Automatically detect users, agents, and service accounts
- **Framework Agnostic** — Core logic is pure Python; first-class FastAPI support
- **Clean Architecture** — Domain ↔ Adapters ↔ API layers with strict dependency inversion
- **Type Safe** — Fully typed, checked with `mypy`
- **Automatic JWKS Rotation** — Fetches and caches keys from OIDC discovery

## Installation

```bash
pip install open-shield-python
```

## Quick Start (FastAPI)

### 1. Configure Environment

```bash
OPEN_SHIELD_ISSUER_URL=https://your-auth-domain.com/oidc
OPEN_SHIELD_AUDIENCE=my-api-identifier
```

### 2. Add Middleware

```python
from fastapi import FastAPI, Depends
from open_shield.api.fastapi import (
    OpenShieldMiddleware,
    get_user_context,
    get_optional_user_context,
    RequireScope,
    RequireRole,
)
from open_shield.adapters import OpenShieldConfig
from open_shield.domain.entities import UserContext

app = FastAPI()
config = OpenShieldConfig()  # Reads from env vars

app.add_middleware(OpenShieldMiddleware, config=config)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users/me")
def read_current_user(ctx: UserContext = Depends(get_user_context)):
    return {
        "id": ctx.user.id,
        "email": ctx.user.email,
        "actor_type": ctx.user.actor_type,
        "tenant": ctx.tenant.tenant_id if ctx.tenant else None,
        "scopes": ctx.user.scopes,
        "roles": ctx.user.roles,
    }

@app.get("/admin/dashboard")
def admin_dashboard(ctx: UserContext = Depends(RequireScope("read:admin"))):
    return {"data": "secret"}

@app.get("/manager/reports")
def reports(ctx: UserContext = Depends(RequireRole(["manager", "admin"]))):
    return {"reports": []}
```

---

## Configurable Claim Mapping

Different identity providers use different JWT claim names. Open Shield lets you configure which claims map to which identity fields — **zero code changes** when switching providers.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPEN_SHIELD_ISSUER_URL` | OIDC Issuer URL **(required)** | — |
| `OPEN_SHIELD_AUDIENCE` | Expected `aud` claim | `None` |
| `OPEN_SHIELD_ALGORITHMS` | Allowed signing algorithms | `["RS256"]` |
| `OPEN_SHIELD_USER_ID_CLAIM` | Claim for user ID | `sub` |
| `OPEN_SHIELD_EMAIL_CLAIM` | Claim for email | `email` |
| `OPEN_SHIELD_TENANT_ID_CLAIM` | Claim for tenant/org ID | `tid` |
| `OPEN_SHIELD_SCOPE_CLAIM` | Claim for scopes | `scope` |
| `OPEN_SHIELD_ROLES_CLAIM` | Claim for roles | `roles` |
| `OPEN_SHIELD_TENANT_FALLBACK` | Fallback when tenant claim missing | `none` |

### Provider Examples

<details>
<summary><strong>Logto</strong></summary>

```bash
OPEN_SHIELD_ISSUER_URL=https://my-logto.com/oidc
OPEN_SHIELD_AUDIENCE=https://my-api.com
OPEN_SHIELD_TENANT_ID_CLAIM=organization_id
OPEN_SHIELD_TENANT_FALLBACK=sub    # Individual users get isolation
```
</details>

<details>
<summary><strong>Keycloak</strong></summary>

```bash
OPEN_SHIELD_ISSUER_URL=https://keycloak.com/realms/myrealm
OPEN_SHIELD_AUDIENCE=my-client-id
OPEN_SHIELD_TENANT_ID_CLAIM=tenant     # Custom claim from mapper
OPEN_SHIELD_ROLES_CLAIM=roles          # Keycloak realm_access also supported
```
</details>

<details>
<summary><strong>Auth0</strong></summary>

```bash
OPEN_SHIELD_ISSUER_URL=https://my-tenant.auth0.com/
OPEN_SHIELD_AUDIENCE=https://my-api
OPEN_SHIELD_TENANT_ID_CLAIM=org_id
OPEN_SHIELD_SCOPE_CLAIM=permissions    # Auth0 uses 'permissions' for RBAC
```
</details>

<details>
<summary><strong>Azure Entra ID</strong></summary>

```bash
OPEN_SHIELD_ISSUER_URL=https://login.microsoftonline.com/{tenant-id}/v2.0
OPEN_SHIELD_AUDIENCE=api://my-api
OPEN_SHIELD_TENANT_ID_CLAIM=tid
OPEN_SHIELD_ROLES_CLAIM=roles
```
</details>

### Programmatic Configuration

```python
from open_shield.adapters import OpenShieldConfig

config = OpenShieldConfig(
    ISSUER_URL="https://my-auth.com/oidc",
    AUDIENCE="https://my-api",
    TENANT_ID_CLAIM="organization_id",
    TENANT_FALLBACK="sub",
)
```

---

## Tenant Resolution Cascade

Tenant isolation is critical for data security. Open Shield uses a **3-step cascade** to resolve the tenant for every request — supporting individual users, SaaS organizations, and M2M service accounts.

### How It Works

```
Step 1: M2M client (sub == client_id)  → TenantResolverPort.resolve_tenant()
Step 2: Organization claim              → OPEN_SHIELD_TENANT_ID_CLAIM
Step 3: Sub fallback                    → sub (when TENANT_FALLBACK=sub)
```

| Use Case | Tenant Source | Config |
|----------|---------------|--------|
| Individual user | `sub` | `TENANT_FALLBACK=sub` |
| SaaS with orgs | `organization_id` | `TENANT_ID_CLAIM=organization_id` |
| M2M service | Registry lookup | Implement `TenantResolverPort` |
| No tenant needed | None | `TENANT_FALLBACK=none` (default) |

### When to Use Each Strategy

**Individual users (OSS, personal tools):**
```bash
OPEN_SHIELD_TENANT_FALLBACK=sub
```
Each user = separate dataset. Simple. Works immediately.

**SaaS with organizations (teams, billing per org):**
```bash
OPEN_SHIELD_TENANT_ID_CLAIM=organization_id
OPEN_SHIELD_TENANT_FALLBACK=none        # Don't fall back to sub
```
Multiple users share org data. Required for team features.

**M2M / AI agents (client_credentials flow):**
```python
from open_shield.domain.ports import TenantResolverPort

class MyTenantResolver(TenantResolverPort):
    """Look up tenant for machine clients from your registry."""

    def resolve_tenant(self, client_id: str) -> str | None:
        # Query your DB, config, or IdP management API
        return db.get_tenant_for_client(client_id)

# Pass resolver to middleware
config = OpenShieldConfig(...)
app.add_middleware(
    OpenShieldMiddleware,
    config=config,
    tenant_resolver=MyTenantResolver(),
)
```

### Resolution Metadata

Every resolved tenant includes traceability:

```python
ctx.tenant.metadata["resolution"]  # "m2m_lookup" | "claim" | "sub_fallback"
```

---

## Actor Type Inference

Open Shield automatically classifies the caller:

| Actor Type | Detection | Example |
|------------|-----------|---------|
| `user` | Default for human tokens | Normal login flow |
| `service` | `sub == client_id` | M2M client_credentials |
| `agent` | `sub == client_id` + `"agent"` role | AI agent with agent role |

```python
ctx.user.actor_type  # "user" | "service" | "agent"
```

---

## Architecture

Open Shield sits as a **thin, powerful layer** between your identity provider and your Python backend — handling all the complexity of token validation, claim extraction, tenant resolution, and authorization enforcement so you don't have to.

![How Open Shield Works](https://raw.githubusercontent.com/avinash-singh-io/open-shield-python/main/docs/images/architecture.png)

### How It Works

1. **Any OIDC Identity Provider** (Logto, Auth0, Keycloak, Azure Entra ID, AWS Cognito, or your own) issues a JWT token when a user or service authenticates.
2. **Open Shield SDK** intercepts the incoming request in your Python application and:
   - **Validates the token** — verifies the signature using auto-fetched JWKS keys from the provider's OIDC discovery endpoint.
   - **Maps claims** — extracts user ID, email, tenant, scopes, and roles from the JWT using your configurable claim mapping (every provider names claims differently — Open Shield normalizes them).
   - **Resolves the tenant** — determines tenant isolation using the 3-step cascade (M2M lookup → org claim → sub fallback).
   - **Detects actor type** — classifies the caller as `user`, `service`, or `agent`.
   - **Enforces authorization** — checks scopes and roles before the request reaches your handler.
3. **Your Python service** receives a clean, verified `UserContext` object — ready to use. No JWT parsing, no OIDC plumbing, no provider-specific code.

### Request Authentication Flow

![Request Authentication Flow](https://raw.githubusercontent.com/avinash-singh-io/open-shield-python/main/docs/images/sequence-flow.png)

### Why This Matters

- **Works with any OIDC provider** — Switch from Auth0 to Keycloak? Change two environment variables. Zero code changes.
- **Works with any Python framework** — First-class FastAPI support today, with Django and Flask coming soon. The core logic is pure Python with no framework dependency.
- **Built on Clean Architecture** — The domain layer has zero external dependencies. All I/O (JWT decoding, OIDC discovery) happens through abstract ports implemented by swappable adapters.
- **Easy to test** — Mock the `TokenValidatorPort` for fast unit tests without any HTTP calls.
- **Easy to extend** — Implement `TenantResolverPort` to wire in your own database for M2M tenant lookups.

---

## Optional Authentication

For routes that work with or without auth (e.g., public APIs with enhanced features for logged-in users):

```python
from open_shield.api.fastapi import get_optional_user_context

@app.get("/search")
def search(ctx: UserContext | None = Depends(get_optional_user_context)):
    if ctx:
        return personalized_results(ctx.user.id)
    return public_results()
```

---

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Lint and format
uv run ruff check .

# Type check
uv run mypy src/
```

## License

MIT
