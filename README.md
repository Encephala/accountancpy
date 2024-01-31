# Accountancpy

[![Test/Lint](https://github.com/Encephala/accountancpy/actions/workflows/test.yml/badge.svg)](https://github.com/Encephala/accountancpy/actions/workflows/test.yml)
![Coverage](media/coverage.svg)

A ~~destined-for-the-graveyard~~ project to create simple personal
bookkeepping software with a Django backend.

Inspired by [HTMX](https://htmx.org/)'s philosophy that simple solutions can be sufficient for neat things.
Accountancpy is built with HTMX for interactivity and [Tabler](https://tabler.io/) for UI.

It won't have full accounting functionality, but the basics of loading expenses
from the bank and assigning them to ledgers should be simple, quick and fun.

## Commit style

I try to prefix commit names as follows:

- `feat`: Adds or changes functionality
- `fix`: Fixes broken behaviour
- `visual`: Changes page style without changing functionality
- `test`: Adds or changes tests
- `style`: Changes code style without changing functionality
- `doc`: Only contains changes to documentation
- `dep`: Updates a dependency
- `dev`: Changes development configuration

## Tooling

Configured in `pyproject.toml` unless stated otherwise.

### Python

Tests using Django's default testing framework.
Test auto-discovery only works if the process working directory is `app/`

```bash
python3 manage.py test
```

Formatted and linted using [Ruff](https://docs.astral.sh/ruff/).

### HTML/templates

Linted using [djLint](https://www.djlint.com/).
No automated formatting.
