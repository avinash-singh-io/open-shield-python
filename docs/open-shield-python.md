# open-shield-python — Vision & Architecture

> Master plan document for the open-shield-python SDK.

## Vision

open-shield-python is a vendor-agnostic authentication and authorization enforcement SDK for Python-based services. It acts as a resource-server security layer implementing open standards for token validation and access enforcement, without performing identity management or login flows.

## Target Use Cases

- SaaS platforms
- Self-hosted deployments
- Open-source products
- Microservice architectures
- Multi-tenant systems

## Architecture

### High-Level Overview

open-shield-python sits between the request ingress and the application logic, intercepting requests to validate tokens/keys and enforce authorization policies.

### Core Components

1. **Token Validator**: Validates JWTs, checks signatures (JWKS), expiration, issuer, and audience
2. **Context Extractor**: Extracts identity and tenant information from the validated token
3. **Authorization Engine**: Enforces scope-based and role-based access control
4. **Framework Adapters**: Integration layers for frameworks (FastAPI, Flask, Django)
5. **Configuration Manager**: Handles configuration via environment variables and files

### Data Flow

1. **Request Interception**: Adapter intercepts incoming HTTP request
2. **Token Extraction**: Auth header extraction
3. **Validation**: Token Validator checks validity against JWKS/Config
4. **Context Creation**: User/Tenant context is built
5. **Authorization**: Policy check (scopes/roles)
6. **Handover**: Request passed to application with injected context

### Clean Architecture Layers

```
src/open_shield/
├── domain/          # Pure business logic (no dependencies)
│   ├── entities.py  # User, Token, TenantContext
│   ├── exceptions.py
│   ├── ports/       # Abstract interfaces (KeyProvider, TokenValidator, TenantResolver)
│   └── services/    # TokenService, AuthorizationService, ClaimMapping
├── adapters/        # Concrete implementations (IO, crypto, config)
│   ├── config.py    # Pydantic-settings based configuration
│   ├── token_validation.py  # PyJWT validator
│   └── key_provider.py      # OIDC Discovery + JWKS
└── api/             # Framework delivery mechanisms
    └── fastapi/     # Middleware, dependencies, exception handlers
```

## Standards Compliance

- OpenID Connect (OIDC) — discovery, JWKS
- OAuth 2.0 — resource server perspective
- JSON Web Tokens (JWT) — RS256+ validation
- JSON Web Key Set (JWKS) — key retrieval and caching

## User Experience

The SDK is designed to be developer-friendly, offering a simple and intuitive API. The "User" is the developer integrating the SDK — there is no direct UI component.

## Specification Reference

For the full functional and non-functional requirements specification, see the original spec in `specs/vision/project-charter.md` and the detailed spec archived at `docs/project-bootstrap.md`.

## Future Considerations

- ABAC (Attribute-Based Access Control)
- External policy engine integration (OPA)
- Distributed authorization service
- Audit log export modules
- Service-to-service token helpers
- Cython optimization for critical paths
- Cross-language spec alignment
