"""
Si el índice funciona bien, debería pasar esto:

query "installation"
→ primer resultado: chunk de installation

query "configuration"
→ primer resultado: chunk de configuration

query "OpenAI server"
→ primer resultado: chunk de OpenAI/server
"""
from models import Chunk
from retrieval import TfidfRetriever, SearchResult


def print_results(query: str, results: list[SearchResult]) -> None:
    """Print search results in a readable format."""
    print("=" * 60)
    print(f"Query: {query}")
    print("-" * 60)

    for rank, result in enumerate(results, start=1):
        chunk = result.chunk
        print(f"{rank}. score={result.score:.4f}")
        print(f"   file_path: {chunk.file_path}")
        print(
            f"   range: {chunk.first_character_index}-"
            f"{chunk.last_character_index}"
        )
        print(f"   content: {repr(chunk.content)}")
        print()


def main() -> None:
    """Run a minimal TF-IDF retrieval demo."""
    chunks = [
        Chunk(
            file_path="intro.md",
            first_character_index=0,
            last_character_index=43,
            content="# Intro\n\nAlpha paragraph about installation.",
        ),
        Chunk(
            file_path="guide.md",
            first_character_index=0,
            last_character_index=42,
            content="# Guide\n\nBeta paragraph about configuration.",
        ),
        Chunk(
            file_path="server.md",
            first_character_index=0,
            last_character_index=40,
            content="# Server\n\nOpenAI compatible server usage.",
        ),
    ]

    retriever = TfidfRetriever(chunks)
    retriever.build_index()

    queries = [
        "installation",
        "configuration",
        "OpenAI server",
        "paragraph",
    ]

    for query in queries:
        results = retriever.search(query, k=3)
        print_results(query, results)


if __name__ == "__main__":
    main()
