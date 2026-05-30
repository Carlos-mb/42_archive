"""Command-line entry points for indexing, retrieval, and answer generation."""

import json
import sys
from pathlib import Path
import logging
import fire
from pydantic import ValidationError
import src.cli_execution

from src.cli_models import (
    AnswerCliArgs,
    AnswerDatasetCliArgs,
    EvaluateCliArgs,
    IndexCliArgs,
    SearchCliArgs,
    SearchDatasetCliArgs,
)

DEFAULT_K = 2
MAX_CONTEXT_LENGTH = 7000
MAX_CHUNK_SIZE = 1800
INDEX_DIRECTORY = "data/processed"


def print_error(message: str) -> None:
    """Print an error message to standard error."""

    print(f"Error: {message}", file=sys.stderr)


def format_validation_error(error: ValidationError) -> str:
    """Format a Pydantic validation error for CLI output."""

    messages: list[str] = []

    for item in error.errors():
        location = ".".join(str(part) for part in item["loc"])
        message = str(item["msg"])

        if message.startswith("Value error, "):
            message = message.removeprefix("Value error, ")

        if location:
            messages.append(f"{location}: {message}")
        else:
            messages.append(message)

    return "\n".join(messages)


def handle_cli_error(error: Exception) -> None:
    """Render a CLI error and exit with a non-zero status."""

    if isinstance(error, ValidationError):
        print_error(format_validation_error(error))
    elif isinstance(error, json.JSONDecodeError):
        print_error(f"Invalid JSON file: {error}")
    else:
        print_error(str(error))

    raise SystemExit(1) from None


def index(
    root_path: str = "",
    save_directory: str = INDEX_DIRECTORY,
    max_chunk_size: int = MAX_CHUNK_SIZE,
    overlap: int | None = None,
    debug: bool = False,
) -> None:
    """Build markdown and code indices from a project root."""

    if debug:
        logging.basicConfig(level=logging.INFO)

    # if overlap == -1:
    #     # overlap = 0
    #     overlap = int(max_chunk_size * .02)
    #     logging.info(f"{fname()}: setting overlap to {overlap}")
    try:
        args = IndexCliArgs(
            root_path=Path(root_path),
            save_directory=Path(save_directory),
            max_chunk_size=max_chunk_size,
            overlap=overlap,
            debug=debug,
        )

        src.cli_execution.run_index(args)
    except (
        ValidationError,
        FileNotFoundError,
        PermissionError,
        json.JSONDecodeError,
        NotImplementedError,
        ValueError,
    ) as error:
        handle_cli_error(error)


def search(
    query: str,
    k: int = DEFAULT_K,
    index_directory: str = INDEX_DIRECTORY,
    max_context_length: int = MAX_CONTEXT_LENGTH,
    debug: bool = False
) -> None:
    """Search the indexed chunks for a single query."""

    try:
        args = SearchCliArgs(
            query=query,
            k=k,
            index_directory=Path(index_directory),
            max_context_length=max_context_length,
            debug=debug,
        )
        src.cli_execution.run_search(args)
    except (
        ValidationError,
        FileNotFoundError,
        PermissionError,
        json.JSONDecodeError,
        NotImplementedError,
        ValueError,
    ) as error:
        handle_cli_error(error)


def search_dataset(
    dataset_path: str = "data/datasets/UnansweredQuestions"
                        "/dataset_docs_public.json",
    k: int = DEFAULT_K,
    save_directory: str = "data/output/search_results/",
    debug: bool = False,
) -> None:
    """Run retrieval over every question in a dataset."""

    try:
        args = SearchDatasetCliArgs(
            dataset_path=Path(dataset_path),
            k=k,
            save_directory=Path(save_directory),
            debug=debug,
        )
        src.cli_execution.run_search_dataset(args)
    except (
        ValidationError,
        FileNotFoundError,
        PermissionError,
        json.JSONDecodeError,
        NotImplementedError,
        ValueError,
    ) as error:
        handle_cli_error(error)


def answer(
    question: str,
    k: int = DEFAULT_K,
    index_directory: str = INDEX_DIRECTORY,
    max_context_length: int = MAX_CONTEXT_LENGTH,
    model_name: str = "Qwen/Qwen3-0.6B",
    debug: bool = False,
) -> None:
    """Generate an answer for a single question."""

    try:
        args = AnswerCliArgs(
            question=question,
            k=k,
            index_directory=Path(index_directory),
            max_context_length=max_context_length,
            model_name=model_name,
            debug=debug,
        )
        src.cli_execution.run_answer(args)
    except (
        ValidationError,
        FileNotFoundError,
        PermissionError,
        json.JSONDecodeError,
        NotImplementedError,
        ValueError,
    ) as error:
        handle_cli_error(error)


def answer_dataset(
    student_search_results_path: str = "data/output/search_results/"
                                       "dataset_docs_public.json",
    save_directory: str = "data/datasets",
    model_name: str = "Qwen/Qwen3-0.6B",
    debug: bool = False,
) -> None:
    """Generate answers for all search results in a dataset."""

    try:
        args = AnswerDatasetCliArgs(
            student_search_results_path=Path(student_search_results_path),
            save_directory=Path(save_directory),
            model_name=model_name,
            debug=debug,
        )
        src.cli_execution.run_answer_dataset(args)
    except (
        ValidationError,
        FileNotFoundError,
        PermissionError,
        json.JSONDecodeError,
        NotImplementedError,
        ValueError,
    ) as error:
        handle_cli_error(error)


def evaluate(
    student_answer_path: str,
    dataset_path: str,
    k: int = DEFAULT_K,
    max_context_length: int = MAX_CONTEXT_LENGTH,
) -> None:
    """Evaluate generated answers against the reference dataset."""

    try:
        args = EvaluateCliArgs(
            student_answer_path=Path(student_answer_path),
            dataset_path=Path(dataset_path),
            k=k,
            max_context_length=max_context_length,
        )
        run_evaluate(args)
    except (
        ValidationError,
        FileNotFoundError,
        PermissionError,
        json.JSONDecodeError,
        NotImplementedError,
        ValueError,
    ) as error:
        handle_cli_error(error)


def run_evaluate(args: EvaluateCliArgs) -> None:
    """Run the evaluation backend for submitted answers."""

    raise NotImplementedError(
        "Connect run_evaluate() to your evaluation implementation."
    )


def main() -> None:
    """Expose the CLI command map to Fire."""

    fire.Fire(
        {
            "index": index,
            "answer": answer,
            "search": search,
            "search_dataset": search_dataset,
            "answer_dataset": answer_dataset,
            "evaluate": evaluate,
        }
    )
