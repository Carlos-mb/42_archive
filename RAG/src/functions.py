"""Small shared helpers used across the RAG project."""

import inspect
from enum import Enum


class FileNames(Enum):
    """Canonical output filenames used by the indexing pipeline."""

    MARKD_OUT = "chunks_markdown.json"
    JSON_OUT = "chunks_json.json"


def fname() -> str:
    """Return the calling function name for log messages."""

    return inspect.stack()[1][3]
