# open-shield-python

open-shield-python is a vendor-agnostic authentication and authorization SDK for Python services.

It provides a unified security layer for modern microservices, supporting:

- OpenID Connect (OIDC)
- OAuth2
- JWT validation
- Scope and role enforcement
- Multi-tenant context handling
- Framework integrations (FastAPI, Flask, Django)

open-shield-python allows services to integrate with any standards-compliant identity provider
such as Logto, Keycloak, Auth0, Azure AD, or custom OIDC systems — without vendor lock-in.

The SDK focuses on:

- Secure token verification
- Config-driven identity provider support
- Clean middleware integration
- Consistent access enforcement across services
- Separation of identity management and service logic

It is designed for SaaS platforms, self-hosted deployments, and distributed systems.
