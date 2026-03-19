---
id: "0001"
title: "Clean Architecture Adoption"
status: accepted
date: 2026-02-12
deciders: Engineering Team
---

# ADR-0001: Clean Architecture Adoption

## Status

`accepted`

## Context

We are building `open-shield-python`, a vendor-agnostic security SDK. It needs to work with various identity providers (Auth0, Keycloak, etc.) and web frameworks (FastAPI, Flask, etc.). Code coupled to specific implementations will make the SDK brittle and hard to extend.

**Decision Drivers:**
- Vendor Neutrality: Core logic must not depend on specific providers
- Framework Independence: Core logic must not depend on FastAPI/Flask
- Testability: Business logic must be testable without network/IO

## Decision

Adopt **Hexagonal / Clean Architecture** (Domain, Ports, Adapters) over traditional layered architecture.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| Traditional Layered (MVC) | Simple, familiar | Tight coupling, hard to swap providers |
| Hexagonal / Clean Architecture | Isolation, flexibility, testability | More boilerplate, higher learning curve |

## Consequences

**Good:**
- **Isolation**: Domain logic (`src/open_shield/domain`) is pure Python and isolated from IO/Frameworks
- **Flexibility**: Swap OIDC providers or Web Frameworks by writing new Adapters (`src/open_shield/adapters`)
- **Testing**: Unit test core logic using mock Adapters without spinning up servers

**Bad:**
- **Boilerplate**: Requires defining Interfaces (Ports) and DTOs, adding initial code volume
- **Complexity**: Slightly higher learning curve for contributors unfamiliar with the pattern

## References

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- Project structure: `src/open_shield/{domain,adapters,api}`
