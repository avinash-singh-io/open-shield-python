# Changelog

All notable changes to this project will be documented in this file.

## [v0.1.0] - 2026-02-12

### Added
- **Core Domain**: Implemented `TokenService`, `AuthorizationService`, and core entities (`User`, `Token`).
- **Adapters**: Added `PyJWTValidator` for token validation and `OIDCDiscoKeyProvider` for JWKS fetching.
- **FastAPI Integration**: Added `OpenShieldMiddleware` and dependencies (`get_user_context`, `RequireScope`, `RequireRole`).
- **Configuration**: `Pydantic` based configuration loading from environment variables.
- **Documentation**: Comprehensive `README.md` and `CONTRIBUTING.md`.
- **Testing**: Integration tests for adapters and API layer.
