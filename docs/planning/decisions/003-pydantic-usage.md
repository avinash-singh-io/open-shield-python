# 003. Pydantic for Configuration and Validation

* Status: Accepted
* Date: 2026-02-12
* Deciders: Engineering Team

## Context and Problem Statement
The SDK configuration (Issuer URL, Audience, Algorithms) must be validated at startup to fail fast. We also need to parse and validate tokens and internal data structures reliably.

## Decision Drivers
* **Validation**: Need strong runtime validation of configuration and data.
* **DX**: Python developers expect Pydantic models in modern libraries.
* **Env Var Support**: Easy loading of settings from environment variables.

## Considered Options
* **Option 1**: Standard Library (`os.getenv`, `dataclasses`).
* **Option 2**: Validation Libraries (`marshmallow`).
* **Option 3**: `pydantic` and `pydantic-settings`.

## Decision Outcome
Chosen option: **Option 3 (Pydantic)**.

### Consequences
* **Good**:
    * **Robustness**: Automatic type coercion and validation.
    * **Settings**: `pydantic-settings` handles env var loading out of the box.
    * **Ecosystem**: Defacto standard in modern Python (FastAPI, etc.).
* **Bad**:
    * **Dependency**: Adds a runtime dependency to the SDK (though it is lightweight and common).
