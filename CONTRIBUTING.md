# Contributing to Open Shield

Thank you for your interest in contributing to Open Shield! We welcome contributions from the community.

## Development Setup

1. **Install uv**: We use `uv` for dependency management.
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/avinash-singh-io/open-shield-python.git
   cd open-shield-python
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Run tests**:
   ```bash
   uv run pytest
   ```

## Code Standards

- **Linting**: We use `ruff`. Run `uv run ruff check .` before committing.
- **Typing**: We use `mypy`. Run `uv run mypy .` to ensure type safety.
- **Architecture**: Please respect the Clean Architecture layers (`domain`, `adapters`, `api`).
- **Commits**: Follow [Conventional Commits](https://www.conventionalcommits.org/).

## Pull Requests

1. Fork the repo and create your branch (`feat/amazing-feature`).
2. Commit your changes.
3. Push to your fork and verify CI passes.
4. Open a Pull Request.

## License

This project is licensed under the MIT License.
