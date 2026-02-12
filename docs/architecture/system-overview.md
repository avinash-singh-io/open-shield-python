# System Architecture

## High-Level Overview
open-shield-python acts as a resource-server security layer. It sits between the request ingress and the application logic, intercepting requests to validate tokens/keys and enforce authorization policies.

## Core Components
1. **Token Validator**: Validates JWTs, checks signatures (JWKS), expiration, issuer, and audience.
2. **Context Extractor**: extracts identity and tenant information from the validated token.
3. **Authorization Engine**: Enforces scope-based and role-based access control.
4. **Framework Adapters**: Integration layers for frameworks like FastAPI, Flask, etc.
5. **Configuration Manager**: Handles configuration via environment variables and files.

## Data Flow
1. **Request Interception**: Adapter intercepts incoming HTTP request.
2. **Token Extraction**: Auth header extraction.
3. **Validation**: Token Validator checks validity against JWKS/Config.
4. **Context Creation**: User/Tenant context is built.
5. **Authorization**: Policy check (scopes/roles).
6. **Handover**: Request passed to application with injected context.
