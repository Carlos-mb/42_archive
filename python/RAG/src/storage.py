"""Persistent storage helpers for chunk JSON files.

Provides `save_chunks` and `load_chunks` helpers to serialize and
deserialize lists of `Chunk` objects to disk. Functions handle common
file I/O errors and log using the project's `fname()` helper.
"""

import json
import logging
from pathlib import Path
from typing import Any

from src.functions import fname
from src.models import Chunk


def save_chunks(chunks: list[Chunk], output_path: str) -> bool:
    """Save chunks to a JSON file.

    The output file will contain a root object with a ``chunks`` key. Parent
    directories are created automatically when needed.

    Args:
        chunks: List of chunks to serialize.
        output_path: Destination JSON file path.

    Returns:
        True if chunks were saved successfully, False otherwise.
    """

    path = Path(output_path)

    if path.exists() and path.is_dir():
        logging.error(f"{fname()}: output_path points to a directory.")
        return False

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logging.error(f"{fname()}: failed to create parent folder: {e}")
        return False

    out: dict[str, list[dict[str, Any]]] = {"chunks": []}

    for chunk in chunks:
        out["chunks"].append(chunk.model_dump())

    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
    except OSError as e:
        logging.error(f"{fname()}: failed to write chunks file: {e}")
        return False
    except TypeError as e:
        logging.error(f"{fname()}: failed to create json chunks: {e}")
        return False

    return True


def load_chunks(input_path: str) -> list[Chunk]:

    chunks: list[Chunk] = []

    path = Path(input_path)

    if path.exists() and path.is_dir():
        logging.error(f"{fname()}: input_path points to a directory.")
        return []

    if len(chunks) != 0:
        logging.error(f"{fname()}: chunks list must be empty")
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            json_chunks = json.load(f)
    except OSError as e:
        logging.error(f"{fname()}: failed to open chunks file: {e}")
        return []
    except TypeError as e:
        logging.error(f"{fname()}: failed to read chunks from file: {e}")
        return []
    except Exception as e:
        logging.error(f"{fname()}: failed to read/import chunks{e}")
        return []

    try:
        for json_chunk in json_chunks["chunks"]:
            chunk = Chunk.model_validate(json_chunk)
            chunks.append(chunk)
    except Exception as e:
        logging.error(f"{fname()}: failed to import chunks: {e}")
        return []

    return chunks
