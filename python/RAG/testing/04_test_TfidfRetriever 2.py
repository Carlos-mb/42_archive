import logging

from models import Chunk
from retrieval import TfidfRetriever
from models import Chunk


def make_chunk(file_path: str, content: str) -> Chunk:
    """Create a test chunk.

    Adjust this function if your Chunk model uses different field names.
    """

    return Chunk(
        file_path=file_path,
        content=content,
        first_character_index=0,
        last_character_index=len(content),
    )


def expect_value_error(test_name: str, callback) -> None:
    """Run a test case that is expected to raise ValueError."""

    try:
        callback()
    except ValueError as error:
        print(f"[OK] {test_name}: ValueError raised: {error}")
    else:
        print(f"[FAIL] {test_name}: ValueError was not raised")


def test_empty_chunk_list() -> None:
    """Test that building an index with no chunks fails."""

    retriever = TfidfRetriever([])
    retriever.build_index()


def test_empty_corpus() -> None:
    """Test that building an index with empty chunk content fails."""

    chunks = [
        make_chunk("empty_1.md", ""),
        make_chunk("empty_2.md", "   "),
    ]

    retriever = TfidfRetriever(chunks)
    retriever.build_index()


def test_search_before_build_index() -> None:
    """Test that searching before building the index fails."""

    chunks = [
        make_chunk("intro.md", "# Intro\n\nAlpha paragraph about installation."),
    ]

    retriever = TfidfRetriever(chunks)
    retriever.search("installation", 1)


def test_empty_query() -> None:
    """Test that an empty query fails."""

    chunks = [
        make_chunk("intro.md", "# Intro\n\nAlpha paragraph about installation."),
    ]

    retriever = TfidfRetriever(chunks)
    retriever.build_index()
    retriever.search("", 1)


def test_blank_query() -> None:
    """Test that a blank query fails."""

    chunks = [
        make_chunk("intro.md", "# Intro\n\nAlpha paragraph about installation."),
    ]

    retriever = TfidfRetriever(chunks)
    retriever.build_index()
    retriever.search("   ", 1)


def test_zero_k() -> None:
    """Test that k = 0 fails."""

    chunks = [
        make_chunk("intro.md", "# Intro\n\nAlpha paragraph about installation."),
    ]

    retriever = TfidfRetriever(chunks)
    retriever.build_index()
    retriever.search("installation", 0)


def test_negative_k() -> None:
    """Test that negative k fails."""

    chunks = [
        make_chunk("intro.md", "# Intro\n\nAlpha paragraph about installation."),
    ]

    retriever = TfidfRetriever(chunks)
    retriever.build_index()
    retriever.search("installation", -1)


def main() -> None:
    """Run manual error-case tests for TfidfRetriever."""

    logging.basicConfig(level=logging.CRITICAL)

    print("=" * 60)
    print("TF-IDF retriever error-case tests")
    print("=" * 60)

    expect_value_error(
        "empty chunk list",
        test_empty_chunk_list,
    )

    expect_value_error(
        "empty corpus",
        test_empty_corpus,
    )

    expect_value_error(
        "search before build_index",
        test_search_before_build_index,
    )

    expect_value_error(
        "empty query",
        test_empty_query,
    )

    expect_value_error(
        "blank query",
        test_blank_query,
    )

    expect_value_error(
        "k equals zero",
        test_zero_k,
    )

    expect_value_error(
        "negative k",
        test_negative_k,
    )


if __name__ == "__main__":
    main()