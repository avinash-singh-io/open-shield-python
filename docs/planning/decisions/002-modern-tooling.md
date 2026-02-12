# 002. Modern Python Tooling Stack

* Status: Accepted
* Date: 2026-02-12
* Deciders: Engineering Team

## Context and Problem Statement
We need a robust, fast, and standard way to manage dependencies, enforce code quality, and ensure type safety for `open-shield-python`. The Python ecosystem has many tools (`pip`, `poetry`, `flake8`, `black`, `isort`), leading to fragmentation and slow CI pipelines.

## Decision Drivers
* **Speed**: CI and local install times should be minimal.
* **Consistency**: Linting and formatting should be uniform.
* **Type Safety**: The SDK is a library; strict typing is essential for user experience (IntelliSense).

## Considered Options
* **Option 1**: Legacy Stack (`pip` + `requirements.txt`, `flake8`, `black`).
* **Option 2**: Poetry Stack (`poetry` for deps, `black`, `isort`).
* **Option 3**: Modern Stack (`uv` for deps, `ruff` for all-in-one linting, `mypy` for typing).

## Decision Outcome
Chosen option: **Option 3 (Modern Stack: uv, ruff, mypy)**.

### Consequences
* **Good**:
    * **Performance**: `uv` is significantly faster than pip/poetry. `ruff` replaces 10+ linting tools with extreme speed.
    * **Simplicity**: Fewer config files (`pyproject.toml` handles almost everything).
    * **Future-proof**: Aligns with modern Python engineering standards.
* **Bad**:
    * **Newness**: `uv` is relatively new, though rapidly maturing and stable for our needs.
