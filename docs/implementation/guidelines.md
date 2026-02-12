# Implementation Guidelines

## Standards
- Follow the "Global Agent Rules" in `task.md` or system prompt.
- Use strict typing for all public interfaces.
- Write unit tests for all logic.
- Use conventional commits.

## Project Specifics
- **Vendor Neutrality**: Do not couple core logic with specific providers (e.g., Auth0, Cognito) or frameworks. Use adapters.
- **Fail Closed**: Security checks must default to denying access if validation fails or is ambiguous.
- **Error Handling**: Do not leak sensitive information in error messages (e.g., "invalid signature" vs "invalid token").
