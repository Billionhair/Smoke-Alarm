# Contributing

Thank you for considering contributing to Smoke Alarm Compliance.

## Getting Started

1. Fork the repository and create a new branch for your feature or bug fix.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt  # if exists
   ```
3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

- Run linters and type checks before committing:
  ```bash
  ruff check agent/src
  mypy agent/src
  ```
- Run the test suite:
  ```bash
  PYTHONPATH=agent/src python -m unittest discover agent/tests -v
  ```
- Ensure your commits have descriptive messages and include tests for any new functionality.

### Resolving merge conflicts

If you encounter conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) after a merge, run the helper script from the repo root to remove them:

```bash
./scripts/strip_conflicts.sh
```

The pre-commit hook will block commits that still contain markers.

## Pull Requests

1. Push your branch and open a pull request.
2. Describe the motivation and provide screenshots or logs if helpful.
3. Ensure CI checks pass before requesting a review.

We appreciate your help in improving the project!
