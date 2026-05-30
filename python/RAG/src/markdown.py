"""Markdown-specific chunking helpers.

This module contains a thin layer that adapts the generic chunking
utilities in :mod:`chunking` to simple markdown documents. The current
implementation identifies document-level titles and then delegates to the
generic chunking machinery. The functions are lightweight and meant to be
expanded with better markdown parsing if needed.
"""

from src.models import Chunk
from src.chunking import chunk_chunks
from src.functions import fname

from pathlib import Path
import logging
import sys
from tqdm import tqdm


def chunk_markdown_files(root_path: str,
                         max_cs: int,
                         overlap: int | None) -> list[Chunk]:
    """Create chunks from Markdown files found under a root directory.

    Recursively scans ``root_path`` for Markdown files, reads each ``.md``
    file as UTF-8 text, computes its path relative to ``root_path``, and
    applies the Markdown chunking strategy to produce ``Chunk`` objects.

    The returned chunks keep file paths relative to the repository root and
    character offsets relative to each original Markdown file.

    Args:
        root_path: Root directory used as the starting point for discovery.
        max_cs: Maximum number of characters allowed in each chunk.
        overlap: Number of characters shared between consecutive fallback
            chunks when a Markdown section must be split.

    Returns:
        A list of chunks generated from all discovered Markdown files.

    """

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
        overlap = int(max_cs * .02)
        # overlap = 0
        logging.info(f"{fname()}: setting overlap for text to {overlap}")

    if not (path / "data" / "raw").is_dir():
        logging.error(f"{fname()}: root_path is not a valid folder: "
                      f"{(path / 'data' / 'raw').as_posix()}")
        return []

    # for p in sorted((path / "data" / "raw").rglob("*")):
    files = sorted((path / "data" / "raw").rglob("*"))
    for p in tqdm(
        files,
        desc="Indexing documens",
        unit="file",
        file=sys.stderr,
        disable=not sys.stderr.isatty(),
    ):
        if not p.is_file():
            continue

        relative_path = p.relative_to(path)
        if any(part in ignored_dirs for part in relative_path.parts):
            continue

        if (p.suffix.lower() == ".md" or p.suffix.lower() == ".txt"):
            try:
                logging.info(f"{fname()}: processing {p.as_posix()}")
                with p.open(encoding="utf-8") as f:
                    text = f.read()
                    if len(text) > 0:
                        chunks.extend(
                            chunk_markdown_text(relative_path.as_posix(),
                                                text, max_cs,
                                                overlap))

            except UnicodeDecodeError:
                logging.warning(f"{fname()}: {p.name} is not utf-8")

    if len(chunks) == 0:
        logging.info(f"{fname()}: no chunks created")

    return chunks


def chunk_markdown_text(file_path: str,
                        text: str,
                        max_cs: int,
                        ovrlp: int) -> list[Chunk]:
    """Create chunks for a markdown document.

    This is a thin adapter that identifies top-level markdown title
    boundaries (lines that start with a `#`) and then ensures each piece
    respects the configured maximum chunk size by delegating to
    :func:`chunking.chunk_chunks`.

    Args:
        file_path: Identifier or path for the source document.
        text: Full markdown text to split into chunks.
        max_cs: Maximum allowed characters per chunk (passed to
            :func:`chunking.chunk_chunks`).
        ovrlp: Overlap in characters used when re-chunking long pieces.

    Returns:
        A list of :class:`models.Chunk` objects covering the document.
    """

    chunks: list[Chunk] = []

    # Create initial chunks split at markdown title boundaries, then
    # re-chunk any pieces that exceed the requested maximum size.
    chunks = chunk_titles(text, file_path)
    chunk_chunks(chunks, max_cs, ovrlp)

    return chunks


def chunk_titles(text: str,
                 file_path: str) -> list[Chunk]:
    """Split markdown text at top-level title boundaries.

    This helper finds occurrences of a newline followed by a `#` (i.e.
    the start of a title on a new line) and uses those positions as
    boundaries to create initial :class:`models.Chunk` instances. It does
    not attempt to fully parse Markdown — it's a simple heuristic that is
    sufficient for coarse-grained splitting.

    Args:
        text: The markdown document as a single string.
        file_path: Identifier or path for the source document.

    Returns:
        A list of :class:`models.Chunk` objects representing the slices
        of the document between detected title boundaries.
    """

    if text == "":
        return []

    chunks: list[Chunk] = []
    titles_pos: list[int] = []

    pos: int = 0

    # pos = 0
    # chunks.append(Chunk(file_path=file_path,
    #                     first_character_index=0,
    #                     last_character_index=len(text),
    #                     content=text
    #                     ))

    # pos = 0
    # while pos >= 0 and pos < len(text):
    #     pos = text.find("\n# ", pos + 1)
    #     if pos != -1:
    #         titles_pos.append(pos + 1)
    # titles_pos.append(len(text))

    # pos = 0
    # for title_pos in titles_pos:
    #     chunks.append(Chunk(file_path=file_path,
    #                         first_character_index=pos,
    #                         last_character_index=title_pos,
    #                         content=text[pos:title_pos]
    #                         ))
    #     pos = title_pos

    pos = 0
    titles_pos = []
    while pos >= 0 and pos < len(text):
        pos = text.find("\n## ", pos + 1)
        if pos != -1:
            titles_pos.append(pos + 1)
    titles_pos.append(len(text))

    pos = 0
    for title_pos in titles_pos:
        chunks.append(Chunk(file_path=file_path,
                            first_character_index=pos,
                            last_character_index=title_pos,
                            content=text[pos:title_pos]
                            ))
        pos = title_pos

    # pos = 0
    # titles_pos = []
    # while pos >= 0 and pos < len(text):
    #     pos = text.find("\n### ", pos + 1)
    #     if pos != -1:
    #         titles_pos.append(pos + 1)
    # titles_pos.append(len(text))

    # pos = 0
    # for title_pos in titles_pos:
    #     chunks.append(Chunk(file_path=file_path,
    #                         first_character_index=pos,
    #                         last_character_index=title_pos,
    #                         content=text[pos:title_pos]
    #                         ))
    #     pos = title_pos

    logging.info(f"{fname()}: found {len(chunks)} chunks in {file_path}")

    return chunks
