from models import Chunk
from markdown import chunk_markdown_text
from chunking import validate_chunks, ChunkValidationError

def print_chunks(chunks: list[Chunk]) -> None:
    """Print chunks in a readable format."""
    for index, chunk in enumerate(chunks, start=1):
        print(f"Chunk {index}")
        print(f"  range: {chunk.first_character_index}-{chunk.last_character_index}")
        print(f"  text:  {repr(chunk.content)}")
        print()


def check_chunks(
    test_name: str,
    text: str,
    chunks: list[Chunk],
    max_cs: int,
    expected_count: int | None = None,
) -> None:
    """Check common chunking invariants."""
    error, detail = validate_chunks(text, chunks, max_cs)

    if error != ChunkValidationError.NO_ERROR:
        print(f"[FAIL] {test_name}")
        print(f"  Validation error: {error}")
        print(f"  Detail: {detail}")
        print_chunks(chunks)
        return

    if expected_count is not None and len(chunks) != expected_count:
        print(f"[FAIL] {test_name}")
        print(f"  Expected chunks: {expected_count}")
        print(f"  Got chunks:      {len(chunks)}")
        print_chunks(chunks)
        return

    print(f"[OK] {test_name}")
    print_chunks(chunks)


def test_preamble_before_first_heading() -> None:
    """Test Markdown text before the first heading."""
    text = (
        "Project preamble.\n"
        "\n"
        "# Intro\n"
        "\n"
        "Alpha paragraph."
    )

    chunks = chunk_markdown_text(
        file_path="test.md",
        text=text,
        max_cs=2000,
        ovrlp=0,
    )

    check_chunks(
        test_name="preamble before first heading",
        text=text,
        chunks=chunks,
        max_cs=2000,
        expected_count=2,
    )

    assert chunks[0].content == "Project preamble.\n\n"
    assert chunks[1].content == "# Intro\n\nAlpha paragraph."


def test_markdown_without_headings() -> None:
    """Test Markdown text without headings."""
    text = (
        "Alpha paragraph.\n"
        "\n"
        "Beta paragraph."
    )

    chunks = chunk_markdown_text(
        file_path="test.md",
        text=text,
        max_cs=2000,
        ovrlp=0,
    )

    check_chunks(
        test_name="markdown without headings",
        text=text,
        chunks=chunks,
        max_cs=2000,
        expected_count=1,
    )

    assert chunks[0].content == text


def test_large_section_without_overlap() -> None:
    """Test a Markdown section that must be split without overlap."""
    text = (
        "# Intro\n"
        "\n"
        "abcdefghijklmnopqrstuvwxyz"
    )

    chunks = chunk_markdown_text(
        file_path="test.md",
        text=text,
        max_cs=10,
        ovrlp=0,
    )

    check_chunks(
        test_name="large section without overlap",
        text=text,
        chunks=chunks,
        max_cs=10,
    )

    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk.content) <= 10


def test_large_section_with_overlap() -> None:
    """Test a Markdown section that must be split with overlap."""
    text = (
        "# Intro\n"
        "\n"
        "abcdefghijklmnopqrstuvwxyz"
    )

    chunks = chunk_markdown_text(
        file_path="test.md",
        text=text,
        max_cs=10,
        ovrlp=3,
    )

    check_chunks(
        test_name="large section with overlap",
        text=text,
        chunks=chunks,
        max_cs=10,
    )

    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk.content) <= 10

    for previous, current in zip(chunks, chunks[1:]):
        assert current.first_character_index < previous.last_character_index


def test_consecutive_headings() -> None:
    """Test consecutive Markdown headings."""
    text = (
        "# Intro\n"
        "## Empty Section\n"
        "## Details\n"
        "\n"
        "Beta paragraph."
    )

    chunks = chunk_markdown_text(
        file_path="test.md",
        text=text,
        max_cs=2000,
        ovrlp=0,
    )

    check_chunks(
        test_name="consecutive headings",
        text=text,
        chunks=chunks,
        max_cs=2000,
        expected_count=3,
    )

    assert chunks[0].content == "# Intro\n"
    assert chunks[1].content == "## Empty Section\n"
    assert chunks[2].content == "## Details\n\nBeta paragraph."


def main() -> None:
    """Run Markdown chunking tests."""
    test_preamble_before_first_heading()
    test_markdown_without_headings()
    test_large_section_without_overlap()
    test_large_section_with_overlap()
    test_consecutive_headings()


if __name__ == "__main__":
    main()