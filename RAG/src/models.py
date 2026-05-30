"""Data models used by the chunking utilities.

This module defines simple Pydantic models that represent text chunks
with their source file and character index metadata. Using Pydantic keeps
the models lightweight while providing validation and convenient dict
serialization.
"""

from pydantic import BaseModel, Field, model_validator
from enum import Enum
from dataclasses import dataclass
from typing import Any


class Chunk(BaseModel):
    """A text chunk with source and index metadata.

    Attributes:
        file_path: Path or identifier of the original document.
        first_character_index: Inclusive start index of the chunk in the
            original document, zero-based.
        last_character_index: Exclusive end index of the chunk in the
            original document.
        content: The substring of the original document represented by
            this chunk.
    """

    file_path: str = Field(min_length=1)
    first_character_index: int = Field(ge=0)
    last_character_index: int = Field(ge=0)
    content: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_character_range(self) -> "Chunk":
        """Validate that the character range matches the chunk content."""

        if self.last_character_index <= self.first_character_index:
            raise ValueError(
                "last_character_index must be greater than "
                "first_character_index"
            )

        expected_length = (
            self.last_character_index - self.first_character_index
        )

        if len(self.content) != expected_length:
            raise ValueError(
                "content length must match the character index range"
            )

        return self


class ChunkValidationError(Enum):
    """Validation result codes for chunk lists.

    Each enum member describes a specific failure mode that can be returned
    by :func:`validate_chunks`. Consumers can use the enum value and the
    accompanying message to understand and report why validation failed.
    """

    NO_ERROR = 0
    CHUNK_SIZE = 1
    GAP = 2
    FIRST_CHAR = 3
    LAST_CHAR = 4
    MAX_CHUNK = 5
    LAST_CHAR_LEN = 6
    TEXT_MATCH = 7
    LAST_END_LEN = 8
    NOT_SORTED = 9


class UnansweredQuestion(BaseModel):
    """A question from a RAG dataset without a reference answer."""

    question_id: str | None = None
    question: str = Field(min_length=1)


class AnsweredQuestion(UnansweredQuestion):
    """A question from a RAG dataset with a reference answer."""

    answer: str = Field(min_length=1)
    sources: list[Any] = Field(default_factory=list)


class RagDataset(BaseModel):
    """Input dataset containing RAG questions."""

    rag_questions: list[UnansweredQuestion]


class MinimalSource(BaseModel):
    """A minimal source reference returned by the retrieval system."""

    file_path: str
    first_character_index: int = Field(ge=0)
    last_character_index: int = Field(ge=0)


class MinimalSearchResults(BaseModel):
    """Search results for a single question."""

    question_id: str | None
    question_str: str
    retrieved_sources: list[MinimalSource]


class StudentSearchResults(BaseModel):
    """Complete search-results payload submitted by the student."""

    search_results: list[MinimalSearchResults]
    k: int = Field(gt=0)


class MinimalAnswer(MinimalSearchResults):
    """Search results plus generated answer for a single question."""

    answer: str


class StudentSearchResultsAndAnswer(BaseModel):
    """Complete answer payload submitted by the student."""

    search_results: list[MinimalAnswer]


@dataclass
class SearchResult:
    """A ranked retrieval result."""

    chunk: Chunk
    score: float
