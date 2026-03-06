# Changelog

All notable changes to this project will be documented in this file.

## [v0.2.6] - 2026-03-06

### Added
- **Architecture Diagram**: High-level architecture image showing how Open Shield SDK sits between identity providers and Python backends.
- **Sequence Diagram**: Request authentication flow diagram illustrating the step-by-step processing of each incoming request.

### Changed
- **Documentation**: Completely overhauled the Architecture section in README with visual diagrams and detailed explanations.
- **Images**: Organized documentation images into `docs/images/` directory.

### Project Maintenance
- **Git Identity Cleaned**: Rewrote entire repository history to unify all commits under the `avinash-singh-io` identity with a verified email.
- **Collaborator Cleanup**: Pruned legacy collaborator access and stale remote tracking branches.
- **Release Synchronization**: Synchronized GitHub tags and releases with the new clean history.


## [v0.2.0] - 2026-02-16

### Added
- **Configurable Claim Mapping**: Map any JWT claim to user/tenant/role fields via environment variables — zero code changes when switching providers.
- **3-Step Tenant Resolution Cascade**: Support for individual users (`sub` fallback), SaaS organizations (org claim), and M2M service accounts (`TenantResolverPort`).
- **Actor Type Inference**: Automatic detection of `user`, `service`, and `agent` actor types.
- **Tenant Resolution Metadata**: Every resolved tenant includes traceability (`m2m_lookup`, `claim`, `sub_fallback`).
- **Optional Authentication**: `get_optional_user_context` dependency for routes that work with or without auth.

### Changed
- **Configuration**: Added environment variables for claim mapping (`OPEN_SHIELD_USER_ID_CLAIM`, `OPEN_SHIELD_TENANT_ID_CLAIM`, etc.).
- **Open Source Readiness**: Added `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CONTRIBUTING.md`, and comprehensive project metadata.

## [v0.1.0] - 2026-02-12

### Added
- **Core Domain**: Implemented `TokenService`, `AuthorizationService`, and core entities (`User`, `Token`).
- **Adapters**: Added `PyJWTValidator` for token validation and `OIDCDiscoKeyProvider` for JWKS fetching.
- **FastAPI Integration**: Added `OpenShieldMiddleware` and dependencies (`get_user_context`, `RequireScope`, `RequireRole`).
- **Configuration**: `Pydantic` based configuration loading from environment variables.
- **Documentation**: Comprehensive `README.md` and `CONTRIBUTING.md`.
- **Testing**: Integration tests for adapters and API layer.
