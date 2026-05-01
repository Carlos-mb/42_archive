import os
import sys
from pprint import pprint
from typing import Any


def printd(*args: Any, **kwargs: Any) -> None:
    """Print to stderr only when debug mode is enabled."""

    if os.getenv("CALLME_DEBUG") == "ON":
        print(*args, file=sys.stderr, **kwargs)


def pprintd(*args: Any, **kwargs: Any) -> None:
    """Pretty-print values only when debug mode is enabled."""

    if os.getenv("CALLME_DEBUG") == "ON":
        kwargs["stream"] = sys.stderr
        pprint(*args, **kwargs)


def printrepd(string: str) -> None:
    """Print to stderr only when debug mode is enabled."""

    if os.getenv("CALLME_DEBUG") == "ON":
        print(repr(string), file=sys.stderr)
