import nox
from nox import Session

PY_VER = ["3.11", "3.12"]


@nox.session(python=PY_VER)  # type: ignore[misc]
def lint(session: Session) -> None:
    """Run Ruff lint and format."""
    session.install("ruff")
    session.run("ruff", "check", ".", "--fix")
    session.run("ruff", "format", ".")


@nox.session(python=PY_VER)  # type: ignore[misc]
def typecheck(session: Session) -> None:
    """Run mypy type checks."""
    session.install("mypy")
    session.run("mypy", ".")


@nox.session(python=PY_VER)  # type: ignore[misc]
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install("pytest", "pytest-xdist", "coverage", "pytest-cov", "hypothesis")
    session.run("pytest", "-n", "auto", "--cov=agent", "--cov-report=xml", "--cov-report=term")


@nox.session(python=PY_VER)  # type: ignore[misc]
def sec(session: Session) -> None:
    """Run security checks."""
    session.install("bandit", "pip-audit")
    session.run("bandit", "-q", "-r", "agent", "-x", "tests")
    session.run("pip-audit", "-r", "requirements.txt", "--strict")


@nox.session(python=PY_VER)  # type: ignore[misc]
def deps(session: Session) -> None:
    """Report dependency information."""
    session.install("deptry", "pipdeptree")
    session.run("deptry")
    session.run("pipdeptree")
