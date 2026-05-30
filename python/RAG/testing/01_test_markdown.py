from models import Chunk
from markdown import chunk_markdown_text


def print_chunks(chunks: list[Chunk]) -> None:
    """Print chunks with indexes and content."""
    for index, chunk in enumerate(chunks, start=1):
        print(f"Chunk {index}")
        print(f"  path:  {chunk.file_path}")
        print(
            f"  range: "
            f"{chunk.first_character_index}-"
            f"{chunk.last_character_index}"
        )
        print(f"  text:  {repr(chunk.content)}")
        print()


def main() -> None:
    """Run one basic Markdown chunking test."""
    text = (
        "# Intro\n"
        "\n"
        "Alpha paragraph.\n"
        "\n"
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

    print_chunks(chunks)

    assert len(chunks) == 2

    assert chunks[0].file_path == "test.md"
    assert chunks[0].first_character_index == 0
    assert chunks[0].content == (
        "# Intro\n"
        "\n"
        "Alpha paragraph.\n"
        "\n"
    )
    assert text[
        chunks[0].first_character_index:chunks[0].last_character_index
    ] == chunks[0].content

    assert chunks[1].file_path == "test.md"
    assert chunks[1].content == (
        "## Details\n"
        "\n"
        "Beta paragraph."
    )
    assert text[
        chunks[1].first_character_index:chunks[1].last_character_index
    ] == chunks[1].content

    print("[OK] Basic Markdown chunking test passed")


if __name__ == "__main__":
    main()