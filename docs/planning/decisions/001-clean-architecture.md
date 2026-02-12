# 001. Clean Architecture Adoption

* Status: Accepted
* Date: 2026-02-12
* Deciders: Engineering Team

## Context and Problem Statement
We are building `open-shield-python`, a vendor-agnostic security SDK. It needs to work with various identity providers (Auth0, Keycloak, etc.) and web frameworks (FastAPI, Flask, etc.). Code coupled to specific implementations will make the SDK brittle and hard to extend.

## Decision Drivers
* Vendor Neutrality: Core logic must not depend on specific providers.
* Framework Independence: Core logic must not depend on FastAPI/Flask.
* Testability: Business logic must be testable without network/IO.

## Considered Options
* **Option 1**: Traditional Layered Architecture (Models, Views, Controllers mixed).
* **Option 2**: Hexagonal / Clean Architecture (Domain, Ports, Adapters).

## Decision Outcome
Chosen option: **Option 2 (Clean Architecture)**.

### Consequences
* **Good**:
    * **Isolation**: Domain logic (`src/open_shield/domain`) is pure Python and isolated from IO/Frameworks.
    * **Flexibility**: We can swap OIDC providers or Web Frameworks by writing new Adapters (`src/open_shield/adapters`).
    * **Testing**: We can unit test the core logic using mock Adapters without spinning up servers.
* **Bad**:
    * **Boilerplate**: Requires defining Interfaces (Ports) and DTOs, which adds some initial code volume.
    * **Complexity**: Slightly higher learning curve for contributors unfamiliar with the pattern.
