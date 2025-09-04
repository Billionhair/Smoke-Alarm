import logging
from rich.console import Console
from rich.logging import RichHandler

_console = Console()


def configure(level: int = logging.INFO) -> logging.Logger:
    """Configure and return a Rich-enabled logger.

    The function is idempotent; calling it multiple times will reuse the
    existing configuration. Tests can call ``configure()`` to obtain a logger
    with predictable formatting.
    """
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=level,
            format="%(message)s",
            handlers=[RichHandler(console=_console, rich_tracebacks=True)],
        )
    return logging.getLogger("agent")
