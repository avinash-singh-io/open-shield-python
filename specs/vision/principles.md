# Engineering Principles

1. **Vendor Neutrality** — Core logic must not depend on specific identity providers (Auth0, Cognito, Keycloak) or frameworks. Use adapters for all external integrations.

2. **Fail Closed** — Security checks must default to denying access if validation fails or is ambiguous. No insecure defaults.

3. **No Sensitive Leakage** — Error messages must not expose internal validation details. Use vague messages (e.g., "invalid token" not "invalid signature for key ID xyz").

4. **Clean Architecture** — Domain logic is pure Python, isolated from IO and frameworks. Adapters implement ports. Framework layers are thin delivery mechanisms.

5. **Strict Typing** — All public interfaces must be strictly typed for IntelliSense and safety. Enforce with `mypy --strict`.

6. **Test Everything** — Unit tests for all logic, integration tests for adapters, E2E tests for framework integration. Target >95% coverage.

7. **Conventional Commits** — All commits follow conventional commit format for automated changelog generation.

8. **Standards First** — Implement open standards (OIDC, OAuth 2.0, JWT, JWKS) correctly before adding proprietary features.
