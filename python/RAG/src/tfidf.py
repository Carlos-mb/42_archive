"""TF-IDF retrieval utilities.

This module implements a simple TF-IDF based retriever powered by
scikit-learn. It exposes a `TfidfRetriever` class for building and
loading indices, normalizing text for search, and ranking chunks using
cosine similarity.
"""

from src.models import Chunk, SearchResult
#  Mypy doesn't know how to type this:
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
from src.functions import fname
from typing import Any
import joblib
from pathlib import Path


def normalize_for_search(text: str) -> str:
    """Normalize code-like text for lexical retrieval."""

    import re
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", text)

    text = text.replace("/", " ")
    text = text.replace("_", " ")
    text = text.replace(".", " ")
    text = text.replace("-", " ")

    return text.lower()


class TfidfRetriever:
    """TF-IDF based retriever for text chunks."""

    def __init__(self, chunks: list[Chunk]) -> None:
        """Initialize the retriever with the chunks to index.

        Args:
            chunks: Chunks that will be used to build the TF-IDF index.
        """

        self.chunks = chunks
        self.tfidf_matrix: Any = None

    def build_index(self, path: Path) -> None:
        """Build the TF-IDF index from the stored chunks.

        Raises:
            ValueError: If the chunk list is empty or if the corpus cannot
                produce a valid TF-IDF vocabulary.
        """

        if not self.chunks:
            self.tfidf_matrix = None
            logging.warning(f"{fname()}: empty chunk list")
            raise ValueError("Chunk list is empty")
        corpus = []

        for chunk in self.chunks:
            normalized_path = chunk.file_path.replace("/", " ")
            normalized_path = normalized_path.replace("_", " ")
            normalized_path = normalized_path.replace(".", " ")

            corpus.append(
                f"{chunk.file_path}\n"
                f"{normalized_path}\n"
                f"{chunk.content}"
            )

        if not any(text.strip() for text in corpus):
            self.tfidf_matrix = None
            logging.warning(f"{fname()}: empty text corpus")
            raise ValueError("Chunk corpus is empty")

        try:

            # fit() : generates learning model parameters from training data
            # transform() : applied upon model to generate transformed data set
            # fit_transform() -> fit + transform
            # self.vectorizer = TfidfVectorizer(ngram_range=(1, 2),
            #    sublinear_tf=True)
            self.vectorizer = TfidfVectorizer(
                preprocessor=normalize_for_search,
                ngram_range=(1, 2),
                sublinear_tf=True,
                )
            # self.vectorizer = TfidfVectorizer()
            self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

        except ValueError as e:
            self.tfidf_matrix = None
            logging.error(f"{fname()}: failed to build TF-IDF index: {e}")
            raise

        try:
            path.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            logging.error(f"{fname()}: failed to create index dir: {e}")
            raise

        joblib.dump(self.vectorizer, path / "vectorizer.joblib")
        joblib.dump(self.tfidf_matrix, path / "matrix.joblib")

    def load_index(self, path: Path) -> None:
        """Load the TF-IDF index.
        """

        if not self.chunks:
            self.tfidf_matrix = None
            logging.warning(f"{fname()}: empty chunk list")
            raise ValueError("Chunk list is empty")
        try:

            self.vectorizer = joblib.load(path / "vectorizer.joblib")
            self.tfidf_matrix = joblib.load(path / "matrix.joblib")
        except ValueError as e:
            self.tfidf_matrix = None
            logging.error(f"{fname()}: failed to build TF-IDF index: {e}")
            raise

    def search(self, query: str, k: int) -> list[SearchResult]:
        """Search the TF-IDF index and return the top-k ranked chunks.

        Args:
            query: User query to search for.
            k: Maximum number of results to return.

        Returns:
            A list of search results ordered by descending similarity score.

        Raises:
            ValueError: If the query is empty, if k is invalid, or if the
                index has not been built yet.
        """

        if self.tfidf_matrix is None:
            logging.error(f"{fname()}: TF-IDF index has not been built")
            raise ValueError("TF-IDF index has not been built")

        if not query.strip():
            logging.error(f"{fname()}: Empty query")
            raise ValueError("Query must not be empty")

        if k <= 0:
            logging.error(f"{fname()}: k must be greater than 0")
            raise ValueError("k must be greater than 0")

        # transform() instead of fit_transform(), because the vocabulary
        # was already learned from the fragments.
        query_vector = self.vectorizer.transform([query])

        # Calculates how closely the query matches each indexed chunk.
        # cosine returns a 2D matrix. 1 query -> list with 1 element
        scores = cosine_similarity(query_vector, self.tfidf_matrix)[0]

        ranked_indexes: list[int] = sorted(
                                range(len(scores)),
                                key=lambda index: scores[index], reverse=True)

        top_indexes = ranked_indexes[:min(k, len(self.chunks))]

        return [
                SearchResult(
                    chunk=self.chunks[index],
                    score=float(scores[index]),
                            ) for index in top_indexes
                ]
