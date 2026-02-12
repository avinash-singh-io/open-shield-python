# Open Shield Python SDK

[![CI](https://github.com/prayog-ai-labs/open-shield-python/actions/workflows/ci.yml/badge.svg)](https://github.com/prayog-ai-labs/open-shield-python/actions/workflows/ci.yml)

Vendor-agnostic authentication and authorization enforcement SDK for Python.

## Features

- **Vendor Neutral**: Works with Auth0, Keycloak, or any OIDC compliant provider.
- **Framework Agnostic**: Core logic is pure Python; adapters provided for FastAPI.
- **Clean Architecture**: Domain logic is isolated from infrastructure concerns.
- **Type Safe**: Fully typed and checked with `mypy`.

## Installation

```bash
pip install open-shield-python
```

## Usage

(Coming Soon)

## Development

This project uses `uv` for dependency management.

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Lint
uv run ruff check .
```
