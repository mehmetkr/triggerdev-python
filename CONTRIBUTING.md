# Contributing

Thanks for your interest in contributing to triggerdev-python.

## Bug reports and feature requests

Use the [issue templates](https://github.com/mehmetkr/triggerdev-python/issues/new/choose) to file bug reports or feature requests. Please search existing issues first to avoid duplicates.

For security vulnerabilities, see [SECURITY.md](SECURITY.md).

## Development setup

This project requires Python 3.10 or later and uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
git clone https://github.com/mehmetkr/triggerdev-python.git
cd triggerdev-python
uv sync --frozen --all-extras
```

## Running checks

The CI pipeline runs these checks. Run them locally before opening a PR:

```bash
uv run ruff check src/ tests/           # lint
uv run ruff format --check src/ tests/   # format
uv run mypy src/                         # type check (mypy strict)
uv run pyright --pythonpath .venv/bin/python src/  # type check (pyright strict)
uv run pytest -q                         # tests
```

To auto-fix lint and format issues:

```bash
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/
```

## Code style

- **Type annotations** on all functions and variables. The project enforces pyright strict and mypy strict with zero errors.
- **Ruff** handles linting and formatting. No additional configuration needed.
- **American English** in all documentation and comments.

## Pull requests

1. Fork the repository and create a branch from `main`.
2. Make your changes, ensuring all checks pass locally.
3. Write or update tests for your changes.
4. Use [Conventional Commits](https://www.conventionalcommits.org/) for your commit messages (e.g., `feat: add batch cancel`, `fix: handle empty response`).
5. Open a pull request using the provided template.

Pull requests require all CI checks to pass before merging.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
