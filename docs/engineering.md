# Engineering Workflow

## Pre-commit
Install and run:

```sh
pre-commit install
pre-commit install --hook-type pre-push
pre-commit run --all-files
```

## Nox
Execute checks:

```sh
nox -s lint typecheck tests sec deps
```

## CI
GitHub Actions runs lint, type checks, tests, security, and dependency reports for Python 3.11 and 3.12 on pushes and pull requests.
