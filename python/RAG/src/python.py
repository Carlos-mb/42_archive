"""Chunk Python source files for indexing."""

from src.models import Chunk
from src.chunking import chunk_chunks
from src.functions import fname

from pathlib import Path
import logging
import sys
from tqdm import tqdm


def chunk_py_files(root_path: str,
                   max_cs: int,
                   overlap: int | None) -> list[Chunk]:
    """Collect Python files under the project raw data tree as chunks."""

    ignored_dirs: list[str] = [
                                ".git",
                                "__pycache__",
                                ".venv",
                                "venv",
                                "node_modules",
                                "dist",
                                "build",
                                ".mypy_cache",
                                ".pytest_cache",
                                ".ruff_cache"
                            ]
    chunks: list[Chunk] = []
    path: Path = Path(root_path)

    if overlap is None:
        overlap = int(max_cs * .1)
        logging.info(f"{fname()}: setting overlap for code to {overlap}")

    if not (path / "data" / "raw").is_dir():
        logging.error(f"{fname()}: root_path is not a valid folder: "
                      f"{(path / 'data' / 'raw').as_posix()}")
        return []

    # for p in sorted((path / "data" / "raw").rglob("*")):
    files = sorted((path / "data" / "raw").rglob("*"))
    for p in tqdm(
        files,
        desc="Indexing code files",
        unit="file",
        file=sys.stderr,
        disable=not sys.stderr.isatty(),
    ):
        if not p.is_file():
            continue

        relative_path = p.relative_to(path)
        if any(part in ignored_dirs for part in relative_path.parts):
            continue

        if p.suffix.lower() == ".py":
            try:
                logging.info(f"{fname()}: processing {p.as_posix()}")
                with p.open(encoding="utf-8") as f:
                    text = f.read()
                    if len(text) > 0:
                        tmp = [Chunk(file_path=relative_path.as_posix(),
                                     first_character_index=0,
                                     last_character_index=len(text),
                                     content=text,
                                     )]
                        # chunk_chunks(tmp, max_cs, overlap)
                        chunk_chunks(tmp, max_cs, overlap)
                        chunks.extend(tmp)
            except UnicodeDecodeError:
                logging.warning(f"{fname()}: {p.name} is not utf-8")
                continue

    if len(chunks) == 0:
        logging.info(f"{fname()}: no chunks created")

    return chunks
