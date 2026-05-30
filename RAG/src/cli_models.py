"""Pydantic models validating CLI arguments for the RAG commands.

This module defines `BaseModel` subclasses used to validate and
coerce command-line inputs for the `index`, `search`, `answer`, and
`evaluate` CLI entry points. Validators ensure paths exist and fields
meet simple bounds checks.
"""

from pathlib import Path
from pydantic import BaseModel, ConfigDict
from pydantic import Field, field_validator, model_validator


class IndexCliArgs(BaseModel):
    """Validated CLI arguments for the index command."""

    model_config = ConfigDict(extra="forbid")

    root_path: Path
    save_directory: Path
    max_chunk_size: int = Field(ge=1, le=2000)
    overlap: int | None = Field(ge=0)
    debug: bool = False

    @field_validator("root_path")
    @classmethod
    def validate_root_path(cls, value: Path) -> Path:
        if not value.exists():
            raise ValueError(f"root_path does not exist: {value}")
        if not value.is_dir():
            raise ValueError(f"root_path is not a directory: {value}")
        return value

    @model_validator(mode="after")
    def validate_overlap(self) -> "IndexCliArgs":
        if self.overlap is not None and self.overlap >= self.max_chunk_size:
            raise ValueError("overlap must be lower than max_chunk_size")
        return self


class SearchCliArgs(BaseModel):
    """Validated CLI arguments for the search command."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    k: int = Field(default=4, ge=1, le=20)
    index_directory: Path
    max_context_length: int = Field(ge=1)
    debug: bool = Field(default=False)

    @field_validator("index_directory")
    @classmethod
    def validate_index_directory(cls, value: Path) -> Path:
        if not value.exists():
            raise ValueError(f"index_directory does not exist: {value}")
        if not value.is_dir():
            raise ValueError(f"index_directory is not a directory: {value}")
        return value


class SearchDatasetCliArgs(BaseModel):
    """Validated CLI arguments for the search_dataset command."""

    model_config = ConfigDict(extra="forbid")

    dataset_path: Path
    k: int = Field(default=10, ge=1, le=20)
    index_directory: Path = Field(default=Path("data/processed"))
    save_directory: Path = Field(default=Path(
                                            "data/datasets/AsweredQuestions"))
    debug: bool = Field(default=False)

    @field_validator("dataset_path")
    @classmethod
    def validate_dataset_path(cls, value: Path) -> Path:
        if not value.exists():
            raise ValueError(f"dataset_path does not exist: {value}")
        if not value.is_file():
            raise ValueError(f"dataset_path is not a file: {value}")
        return value

    @field_validator("index_directory")
    @classmethod
    def validate_index_directory(cls, value: Path) -> Path:
        if not value.exists():
            raise ValueError(f"index_directory does not exist: {value}")
        if not value.is_dir():
            raise ValueError(f"index_directory is not a directory: {value}")
        return value


class AnswerCliArgs(BaseModel):
    """Validated CLI arguments for the answer command."""

    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=1)
    k: int = Field(default=4, ge=0, le=20)
    index_directory: Path = Field(default=Path("data/processed"))
    max_context_length: int = Field(ge=1)
    model_name: str = Field(default="Qwen/Qwen3-0.6B", min_length=1)
    debug: bool

    @field_validator("index_directory")
    @classmethod
    def validate_index_directory(cls, value: Path) -> Path:
        if not value.exists():
            raise ValueError(f"index_directory does not exist: {value}")
        if not value.is_dir():
            raise ValueError(f"index_directory is not a directory: {value}")
        return value


class AnswerDatasetCliArgs(BaseModel):
    """Validated CLI arguments for the answer_dataset command."""

    model_config = ConfigDict(extra="forbid")

    student_search_results_path: Path = Field(
        default=Path("data/output/search_results/dataset_docs_public.json")
    )
    save_directory: Path = Field(
        default=Path("data/output/search_results_and_answer")
    )
    model_name: str = Field(default="Qwen/Qwen3-0.6B", min_length=1)
    debug: bool = Field(default=False)

    @field_validator("student_search_results_path")
    @classmethod
    def validate_student_search_results_path(cls, value: Path) -> Path:
        if not value.exists():
            raise ValueError(
                f"student_search_results_path does not exist: {value}"
            )
        if not value.is_file():
            raise ValueError(
                f"student_search_results_path is not a file: {value}"
            )
        return value


class EvaluateCliArgs(BaseModel):
    """Validated CLI arguments for the evaluate command."""

    model_config = ConfigDict(extra="forbid")

    student_answer_path: Path
    dataset_path: Path
    k: int = Field(default=10, ge=1, le=20)
    max_context_length: int = Field(ge=1)

    @field_validator("student_answer_path")
    @classmethod
    def validate_student_answer_path(cls, value: Path) -> Path:
        if not value.exists():
            raise ValueError(f"student_answer_path does not exist: {value}")
        if not value.is_file():
            raise ValueError(f"student_answer_path is not a file: {value}")
        return value

    @field_validator("dataset_path")
    @classmethod
    def validate_dataset_path(cls, value: Path) -> Path:
        if not value.exists():
            raise ValueError(f"dataset_path does not exist: {value}")
        if not value.is_file():
            raise ValueError(f"dataset_path is not a file: {value}")
        return value
