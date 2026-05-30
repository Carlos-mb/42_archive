"""Utilities for splitting text into index-linked chunks and validating them.

This module provides helpers to create fixed-size chunks with optional
overlap, validate a list of :class:`models.Chunk` objects against the
original text, and re-chunk already-created chunks when they exceed a
maximum size. The functions are intentionally small and pure so they can
be used by other modules that implement document-specific chunking
strategies.
"""

from src.models import Chunk, ChunkValidationError


def validate_chunks(text: str,
                    chunks: list[Chunk],
                    max_cs: int) -> tuple[ChunkValidationError, str]:
    """Validate a list of chunks against the original text.

    Checks performed:
    - ``max_cs`` must be positive.
    - Chunk indices must be within bounds and in non-decreasing order.
    - There must be no unfilled gaps between chunks: the sequence should
        cover the entire input text.
    - Each chunk's ``content`` must match the corresponding substring of
        ``text`` defined by its indices.

    Returns:
            A tuple ``(ChunkValidationError, message)``. On success the enum
            value is ``ChunkValidationError.NO_ERROR`` and the message is an
            empty string. Otherwise the enum describes the failure mode and
            the message contains additional diagnostic information.
    """

    if max_cs <= 0:
        return ChunkValidationError.CHUNK_SIZE, ""

    # chunks = sorted(chunks_input, key=lambda c: c.first_character_index)
    last_end: int = 0
    previous_start = -1
    for chunk in chunks:

        if chunk.first_character_index < previous_start:
            return (ChunkValidationError.NOT_SORTED,
                    f"{chunk.first_character_index} - {previous_start}")
        previous_start = chunk.first_character_index

        if chunk.last_character_index > len(text):
            return (ChunkValidationError.LAST_CHAR_LEN,
                    f"{chunk.last_character_index}")

        if chunk.first_character_index > last_end:
            return (ChunkValidationError.GAP,
                    f"From: {last_end} to {chunk.first_character_index}")

        if len(chunk.content) > max_cs:
            return ChunkValidationError.MAX_CHUNK, "Chunk bigger than max"

        text1 = text[chunk.first_character_index:chunk.last_character_index]
        if text1 != chunk.content:
            return (ChunkValidationError.TEXT_MATCH,
                    f"{chunk.first_character_index} : "
                    f"{chunk.last_character_index}")

        last_end = max(last_end, chunk.last_character_index)

    if last_end != len(text):
        return (ChunkValidationError.LAST_END_LEN, f"Last end: {last_end} - "
                                                   f"Len: {len(text)}")

    return ChunkValidationError.NO_ERROR, ""


def chunk_text(file_path: str,
               text: str,
               max_cs: int,
               overlap: int,
               offset: int) -> list[Chunk]:
    """Split raw text into fixed-size chunks with optional overlap.

    Args:
        file_path: Identifier for the source file (stored in each Chunk).
        text: The string to split into chunks.
        max_cs: Maximum number of characters in each chunk. Must be
            greater than zero.
        overlap: Number of characters to overlap between consecutive
            chunks. Must be non-negative and smaller than ``max_cs``.
        offset: An integer offset added to the reported character indices.

    Returns:
        A list of :class:`models.Chunk` objects covering the provided text.

    Raises:
        ValueError: If parameters are invalid (non-positive sizes or
            negative overlap/offset).
    """

    out: list[Chunk] = []

    if max_cs <= 0:
        raise ValueError("Chunk size must be int > 0")

    if overlap >= max_cs:
        raise ValueError("Overlap too big for max chunk size")

    if offset < 0:
        raise ValueError("Offset must be >= 0")

    if overlap < 0:
        raise ValueError("Overlap cannot be negative")

    start: int = 0
    end: int = 0
    while start < len(text):
        end = start + max_cs
        if end > len(text):
            end = len(text)

        if end >= len(text):
            overlap = 0
        out.append(
            Chunk(
                file_path=file_path,
                first_character_index=start + offset,
                last_character_index=end + offset,
                content=text[start:end],
                )
            )
        start = end - overlap
    return out


def chunk_chunks(chunks: list[Chunk],
                 max_cs: int,
                 ovrlp: int) -> None:
    """Re-chunk elements of an existing chunk list that exceed ``max_cs``.

    Iterates the provided list of :class:`models.Chunk` instances and
    replaces any chunk whose content length is greater than ``max_cs``
    with smaller chunks produced by :func:`chunk_text`. The function
    mutates the input list in-place.

    Args:
        chunks: Mutable list of :class:`models.Chunk` objects. The list is
            modified in-place to keep chunks within ``max_cs``.
        max_cs: Maximum allowed chunk size.
        ovrlp: Overlap to use when splitting oversized chunks.
    """

    i: int = 0
    j: int = 0

    while i < len(chunks):
        text = chunks[i].content
        if len(text) > max_cs:
            new_chunks = chunk_text(chunks[i].file_path,
                                    text,
                                    max_cs,
                                    ovrlp,
                                    chunks[i].first_character_index)
            chunks[i] = new_chunks[0]
            for chunk in new_chunks[1:]:
                j = j + 1
                chunks.insert(i + j, chunk)

        i += 1 + j
        j = 0
