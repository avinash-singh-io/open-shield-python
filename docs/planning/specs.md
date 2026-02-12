🛡 open-shield-python
Initial Specification (v1)
1. Purpose

open-shield-python is a vendor-agnostic authentication and authorization enforcement SDK for Python-based services.

It acts as a resource-server security layer implementing open standards for token validation and access enforcement, without performing identity management or login flows.

The SDK is intended for use in:

SaaS platforms

Self-hosted deployments

Open-source products

Microservice architectures

Multi-tenant systems

2. Scope

The SDK shall provide:

Standards-based token validation

Authorization enforcement

Multi-tenant context extraction

Framework integration layer(s)

Config-driven behavior

Extensibility for future policy engines

The SDK shall not provide:

Identity provider capabilities

User management

Token issuance

Login flows

Password management

Federation management

3. Standards Compliance Requirements

The SDK must support the following standards:

3.1 Authentication Standards

OpenID Connect (OIDC)

OAuth 2.0 (resource server perspective)

JSON Web Tokens (JWT)

JSON Web Key Set (JWKS)

3.2 Token Validation Requirements

The SDK must validate:

Token signature

Issuer (iss)

Audience (aud)

Expiration (exp)

Not-before (nbf)

Issued-at (iat) where applicable

Token type (access tokens only)

The SDK must reject:

Unsigned tokens

Expired tokens

Tokens from untrusted issuers

Tokens with invalid audience

Tokens with unsupported algorithms

4. Functional Requirements (FR)
FR-1: OIDC Discovery

The SDK shall:

Support automatic retrieval of OIDC configuration from a discovery endpoint

Retrieve and cache JWKS keys

Support key rotation handling

FR-2: JWT Validation

The SDK shall:

Validate tokens locally after initial key retrieval

Support asymmetric signature verification (minimum RS256)

Provide configurable required claims

Support configurable issuer and audience validation

FR-3: Authorization Enforcement

The SDK shall support:

Scope-based access control

Role-based access control

Custom claim validation

Access denial on failed authorization checks

Default deny behavior

FR-4: Multi-Tenancy Support

The SDK shall:

Support configurable tenant identifier claim

Extract tenant context from validated tokens

Expose tenant context for application-layer enforcement

Ensure no implicit cross-tenant access is permitted

FR-5: Authentication Modes

The SDK shall support configurable operational modes:

OIDC-based token validation

API key validation

Disabled mode (for development/testing only)

FR-6: API Key Support

If enabled, the SDK shall:

Support API key validation

Support scoped API keys

Support revocation capability

Prevent storage of plaintext keys (hashed storage required)

FR-7: Framework Integration

The SDK shall:

Provide framework integration adapters

Support request lifecycle interception

Support injection of authenticated context

Provide standardized error responses for authentication and authorization failures

Framework integration shall be extensible.

FR-8: Configuration

The SDK shall:

Support configuration via environment variables

Support configuration via structured configuration files

Validate configuration at initialization

Fail fast on invalid configuration

FR-9: Error Handling

The SDK shall:

Provide standardized authentication errors

Provide standardized authorization errors

Avoid leaking sensitive token validation details

Support structured error reporting

FR-10: Extensibility

The SDK shall:

Allow future integration with external policy engines

Support pluggable authorization strategies

Allow future expansion of supported algorithms

5. Non-Functional Requirements (NFR)
NFR-1: Security

Fail closed by default

No insecure defaults

Strict issuer and audience enforcement

No support for insecure algorithms

No acceptance of unsigned tokens

Safe handling of malformed tokens

NFR-2: Performance

No network call per request after JWKS retrieval

JWKS must be cached

Validation must be efficient and scalable

Suitable for high-throughput microservices

NFR-3: Thread Safety

Must support multi-threaded environments

Must support asynchronous execution

Must support multi-worker deployments

NFR-4: Observability

Provide structured logging hooks

Support audit event emission

Avoid logging sensitive token data

Support integration with application logging systems

NFR-5: Reliability

Graceful handling of temporary JWKS retrieval failures

Predictable behavior under misconfiguration

Deterministic validation outcomes

NFR-6: Portability

Must not depend on any specific identity provider

Must remain compatible with any standards-compliant OIDC provider

Must not include vendor-specific logic

NFR-7: Maintainability

Clear separation of core logic and framework adapters

Modular internal architecture

Clean public API surface

Minimal external dependencies

NFR-8: Backward Compatibility

Semantic versioning must be followed

Breaking changes must be clearly documented

Major version increments required for incompatible changes

6. Explicit Non-Goals

The SDK shall not:

Issue tokens

Manage user accounts

Provide UI for authentication

Replace identity providers

Act as an API gateway

Implement rate limiting

Handle billing enforcement

Provide session management

7. Version 1 Boundaries

Version 1 must include:

OIDC discovery support

JWT validation

Scope enforcement

Role enforcement

Multi-tenant extraction

FastAPI adapter

Config-driven setup

Version 1 may exclude:

Advanced policy engines

Distributed authorization graph models

Federation features

Enterprise SSO-specific flows

8. Future Considerations (Non-Binding)

Potential expansion areas:

ABAC (Attribute-Based Access Control)

External policy engine integration

Distributed authorization service

Audit log export modules

Service-to-service token helpers

Cross-language spec alignment

This document defines the baseline specification for open-shield-python v1.

Further architectural design and implementation details shall be derived from this specification during R&D.