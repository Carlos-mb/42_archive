from src.markdown import chunk_markdown_files
from src.cli_models import (IndexCliArgs, AnswerCliArgs,
                            SearchDatasetCliArgs, SearchCliArgs,
                            AnswerDatasetCliArgs)
from src.models import (StudentSearchResultsAndAnswer,
                        MinimalAnswer, MinimalSearchResults,
                        StudentSearchResults, MinimalSource,
                        RagDataset, Chunk)
from src.tfidf import TfidfRetriever
from src.retrieval import build_rag_prompt, build_context, retrieve_sources
import logging
from src.functions import fname
from src.storage import save_chunks
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM
import json
from pathlib import Path
import sys
from typing import Any
from tqdm import tqdm
from src.python import chunk_py_files

"""CLI execution helpers for indexing, searching and answering.

This module contains functions used by the command-line interface to
index documents and code, perform retrieval, and generate model-based
answers. Docstrings follow a Google-style convention describing
parameters and return values.
"""

MAX_NEW_TOKENS = 600


def run_index(args: IndexCliArgs) -> None:
    """Run the indexing pipeline.

    Processes markdown and Python source files under `args.root_path`,
    creates chunked documents, saves them to the `args.save_directory`,
    and builds TF-IDF indices for documents, code, and a combined index.

    Args:
        args: `IndexCliArgs` containing `root_path`, `max_chunk_size`,
            `overlap`, and `save_directory` used by the indexing pipeline.

    Returns:
        None
    """

    logging.info(f"{fname()}: Creating chunks\n"
                 f"Root path: {args.root_path.as_posix()}\n"
                 f"Max cs: {args.max_chunk_size}\n"
                 f"Overlap: {args.overlap}\n")

    chunks = chunk_markdown_files((args.root_path).as_posix(),
                                  args.max_chunk_size,
                                  args.overlap)

    if len(chunks) == 0:
        logging.info(f"{fname()}: no chunks created for documents.")
    else:

        processed_file = (args.save_directory /
                          "chunks" / "documents.json").as_posix()

        logging.info(f"{fname()}: saving document chunks in {processed_file}")
        save_chunks(chunks, processed_file)
        retriever = TfidfRetriever(chunks)
        retriever.build_index(args.save_directory / "tfid_documents_index")

    chunks_code = chunk_py_files((args.root_path).as_posix(),
                                 args.max_chunk_size,
                                 args.overlap)

    if len(chunks_code) == 0:
        logging.info(f"{fname()}: no chunks created for code.")
    else:

        processed_file = (args.save_directory /
                          "chunks" / "code.json").as_posix()

        logging.info(f"{fname()}: saving code chunks in {processed_file}")
        save_chunks(chunks_code, processed_file)
        retriever = TfidfRetriever(chunks_code)
        retriever.build_index(args.save_directory / "tfid_code_index")

    chunks_code.extend(chunks)
    if len(chunks_code) != 0:
        retriever = TfidfRetriever(chunks_code)
        retriever.build_index(args.save_directory / "tfid_all_index")

        print("Code ingestion complete! Indices saved under "
              f"{args.save_directory.as_posix()}")


def run_search_dataset(args: SearchDatasetCliArgs) -> None:
    """Run retrieval for all questions in a dataset.

    Reads a JSON RAG dataset from `args.dataset_path`, validates it, and
    runs retrieval for every question using `build_search_result`. The
    aggregated `StudentSearchResults` are written to
    `args.save_directory / <dataset_stem>.json`.

    Args:
        args: `SearchDatasetCliArgs` containing `dataset_path`,
            `index_directory`, `k`, `save_directory`, and `debug`.

    Returns:
        None

    Errors:
        Prints to stderr and returns early on file I/O or JSON
        validation errors.
    """

    if args.debug:
        logging.basicConfig(level=logging.INFO)

    try:
        args.save_directory.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Error: creating save directory {e}", file=sys.stderr)
        return

    try:
        with open(args.dataset_path, "r", encoding="utf-8") as f:
            dataset = json.load(f)
    except OSError as e:
        print(f"Error: opening questions {e}", file=sys.stderr)
        return
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON dataset {e}", file=sys.stderr)
        return

    try:
        rag_dataset = RagDataset.model_validate(dataset)
    except Exception as e:
        print(f"Error: invalid RAG dataset format {e}", file=sys.stderr)
        return

    search_results: list[MinimalSearchResults] = []

    for q in tqdm(
        rag_dataset.rag_questions,
        desc="Searching questions",
        unit="question",
        file=sys.stderr,
        disable=not sys.stderr.isatty(),
    ):
        question = q.question
        question_id = q.question_id
        logging.info(f"{fname()}: Processing {question}")

        result = build_search_result(
            question_id=question_id,
            question=question,
            k=args.k,
            index_directory=args.index_directory,
        )

        search_results.append(result)

    payload = StudentSearchResults(
        search_results=search_results,
        k=args.k,
    )

    output_path = (
        args.save_directory
        / f"{args.dataset_path.stem}.json"
    )

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(payload.model_dump_json(indent=2))
    except OSError as e:
        print(f"Error: writing search results {e}", file=sys.stderr)
        return


def run_search(args: SearchCliArgs) -> None:
    """Run retrieval for one question.

    Performs retrieval for the provided `args.query` and prints a
    `StudentSearchResults` JSON payload to stdout.

    Args:
        args: `SearchCliArgs` containing `query`, `k`, `index_directory`,
            and `debug`.

    Returns:
        None
    """

    if args.debug:
        logging.basicConfig(level=logging.INFO)

    result = build_search_result(
        question_id="None",
        question=args.query,
        k=args.k,
        index_directory=args.index_directory,
    )

    payload = StudentSearchResults(
        search_results=[result],
        k=args.k,
    )

    print(payload.model_dump_json(indent=2))


def build_search_result(
    question_id: str | None,
    question: str,
    k: int,
    index_directory: Path,
) -> MinimalSearchResults:
    """Build a `MinimalSearchResults` payload for a single question.

    This function calls `retrieve_sources` to fetch the top-`k`
    retrieved sources and wraps them into the `MinimalSearchResults`
    model used by the CLI output.

    Args:
        question_id: Optional identifier for the question.
        question: The natural-language question string to search for.
        k: Number of top sources to retrieve.
        index_directory: Path to the TF-IDF index directory.

    Returns:
        A `MinimalSearchResults` instance containing the question id,
        question string, and the retrieved sources.
    """

    retrieved_sources, _ = retrieve_sources(
        question=question,
        k=k,
        index_directory=index_directory,
    )

    return MinimalSearchResults(
        question_id=question_id,
        question_str=question,
        retrieved_sources=retrieved_sources,
    )


def clean_answer_text(answer_text: str) -> str:
    """Normalize and clean raw model-generated answer text.

    The function strips internal thinking markers (e.g. `<think>`) and
    surrounding whitespace. If the cleaned text is empty, a user-facing
    fallback message is returned.

    Args:
        answer_text: Raw string produced by the language model.

    Returns:
        A cleaned, human-readable answer string. If the cleaned result
        is empty, returns a default message indicating insufficient
        context.
    """

    answer_text = answer_text.replace("<think>\n</think>", "")
    answer_text = answer_text.replace("<think>", "")
    answer_text = answer_text.replace("</think>", "")
    answer_text = answer_text.strip()

    if not answer_text:
        return "The provided context is insufficient."

    return answer_text


def load_answer_model(model_name: str) -> tuple[Any, Any]:
    """Load a tokenizer and causal LM for answer generation.

    This helper loads `AutoTokenizer`, `AutoConfig`, and
    `AutoModelForCausalLM` from Hugging Face for the given
    `model_name`. It disables sampling-related generation parameters
    on the model's `generation_config` and places the model in
    evaluation mode.

    Args:
        model_name: The pretrained model identifier or local path.

    Returns:
        A tuple `(tokenizer, model)` where `tokenizer` is an
        `AutoTokenizer` instance and `model` is an
        `AutoModelForCausalLM` loaded onto the appropriate device.
    """

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    config = AutoConfig.from_pretrained(model_name)

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        config=config,
        device_map="auto",
    )

    if model.generation_config:
        model.generation_config.temperature = None
        model.generation_config.top_p = None
        model.generation_config.top_k = None

    model.eval()

    return tokenizer, model


def generate_answer_with_model(
    prompt: str,
    tokenizer: Any,
    model: Any,
    max_new_tokens: int
) -> str:
    """Generate text from `prompt` using a loaded tokenizer and model.

    Tokenizes the prompt, runs a deterministic generation (sampling is
    disabled), and decodes the generated token ids back into text.

    Args:
        prompt: The full prompt string to feed the model.
        tokenizer: A tokenizer compatible with `model`.
        model: A causal language model supporting `.generate()`.
        max_new_tokens: Maximum number of tokens to generate beyond the
            prompt length.

    Returns:
        The cleaned generated answer string.
    """

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    generated = model.generate(
        **inputs,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        max_new_tokens=max_new_tokens
    )

    prompt_length = inputs["input_ids"].shape[1]
    output_ids = generated[0][prompt_length:]

    answer_text = tokenizer.decode(
        output_ids,
        skip_special_tokens=True,
    )

    return clean_answer_text(answer_text)


def generate_answer_text(
    question: str,
    retrieved_chunks: list[Chunk],
    max_context_length: int,
    model_name: str,
) -> str:
    """Generate an answer string from retrieved chunks using a model.

    The function builds a textual context from `retrieved_chunks`,
    truncates it to `max_context_length` if necessary, constructs a
    RAG prompt, loads the model, and returns the model-generated
    answer text.

    Args:
        question: The user question to answer.
        retrieved_chunks: List of `Chunk` objects retrieved for the
            question.
        max_context_length: Maximum number of characters of context to
            include in the prompt.
        model_name: The pretrained model identifier to load for
            generation.

    Returns:
        The generated answer string.
    """

    if not retrieved_chunks:
        return "The provided context is insufficient."

    context = build_context(retrieved_chunks)

    if len(context) > max_context_length:
        logging.info(
            f"{fname()}: context truncated from "
            f"{len(context)} to {max_context_length}"
        )
        context = context[:max_context_length]
        logging.info(f"{fname()}: context: {context}")

    prompt = build_rag_prompt(question, context)
    logging.info(f"{fname()}: prompt: \n{prompt}\n")

    tokenizer, model = load_answer_model(model_name)

    answer_text = generate_answer_with_model(
        prompt=prompt,
        tokenizer=tokenizer,
        model=model,
        max_new_tokens=MAX_NEW_TOKENS,
    )

    return answer_text


def build_answer_result(
    question_id: str,
    question: str,
    k: int,
    index_directory: Path,
    max_context_length: int,
    model_name: str,
) -> MinimalAnswer:
    """Build a `MinimalAnswer` payload for a single question.

    Retrieves top-`k` sources, generates an answer based on the
    retrieved chunks, and returns a `MinimalAnswer` object that
    includes the question, retrieved sources, and the generated
    answer text.

    Args:
        question_id: Identifier for the question.
        question: The question text.
        k: Number of top sources to retrieve.
        index_directory: Path to the TF-IDF index directory.
        max_context_length: Maximum context length (characters) to
            include when constructing the prompt.
        model_name: The pretrained model identifier for generation.

    Returns:
        A `MinimalAnswer` instance containing the question id,
        question string, retrieved sources, and generated answer.
    """

    retrieved_sources, retrieved_chunks = retrieve_sources(
        question=question,
        k=k,
        index_directory=index_directory,
    )

    answer_text = generate_answer_text(
        question=question,
        retrieved_chunks=retrieved_chunks,
        max_context_length=max_context_length,
        model_name=model_name,
    )

    result = MinimalAnswer(
        question_id=question_id,
        question_str=question,
        retrieved_sources=retrieved_sources,
        answer=answer_text,
    )

    return result


def run_answer(args: AnswerCliArgs) -> None:
    """Run retrieval and answer generation for one question.

    Uses `build_answer_result` to create an answer payload and
    prints a `StudentSearchResultsAndAnswer` JSON document to stdout.

    Args:
        args: `AnswerCliArgs` containing `question`, `k`,
            `index_directory`, `max_context_length`, `model_name`, and
            `debug`.

    Returns:
        None
    """

    if args.debug:
        logging.basicConfig(level=logging.INFO)

    result = build_answer_result(
        question_id="None",
        question=args.question,
        k=args.k,
        index_directory=args.index_directory,
        max_context_length=args.max_context_length,
        model_name=args.model_name,
    )

    payload = StudentSearchResultsAndAnswer(
        search_results=[result],
    )

    print(payload.model_dump_json(indent=2))


def run_answer_dataset(args: AnswerDatasetCliArgs) -> None:
    """Run retrieval and answer generation for all questions in a dataset.

    Given a `StudentSearchResults` JSON file produced by
    `run_search_dataset`, this function validates and iterates over the
    search results, generating answers for each item. Results are
    written to `args.save_directory / <input_stem>.json`.

    Args:
        args: `AnswerDatasetCliArgs` containing
            `student_search_results_path`, `save_directory`, `model_name`,
            and `debug`.

    Returns:
        None
    """

    if args.debug:
        logging.basicConfig(level=logging.INFO)

    try:
        args.save_directory.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Error: creating save directory {e}", file=sys.stderr)
        return

    try:
        with open(args.student_search_results_path, "r",
                  encoding="utf-8") as f:
            dataset = json.load(f)
    except OSError as e:
        print(f"Error: opening questions {e}", file=sys.stderr)
        return
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON dataset {e}", file=sys.stderr)
        return

    try:
        search_payload = StudentSearchResults.model_validate(dataset)
    except Exception as e:
        print("\nError: invalid search results format")
        print("Remember: answer_dataset expects a StudentSearchResults JSON "
              "file generated by search_dataset,"
              " not a raw rag_questions dataset.\n"
              f" {e}", file=sys.stderr)
        return

    tokenizer = None
    model = None
    answer_results: list[MinimalAnswer] = []

    # for search_result in search_payload.search_results:
    for search_result in tqdm(
        search_payload.search_results,
        desc="Generating answers",
        unit="answer",
        file=sys.stderr,
        disable=not sys.stderr.isatty(),
    ):
        logging.info(f"{fname()}: Processing {search_result.question_str}")

        answer_text, tokenizer, model = generate_answer_from_sources(
            question=search_result.question_str,
            retrieved_sources=search_result.retrieved_sources,
            root_path=Path(""),
            model_name=args.model_name,
            tokenizer=tokenizer,
            model=model,
        )

        answer_results.append(
                        MinimalAnswer(
                            question_id=search_result.question_id,
                            question_str=search_result.question_str,
                            retrieved_sources=search_result.retrieved_sources,
                            answer=answer_text,
                        )
                    )

    answer_payload = StudentSearchResultsAndAnswer(
        search_results=answer_results,
    )

    output_path = (args.save_directory /
                   f"{args.student_search_results_path.stem}.json")

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(answer_payload.model_dump_json(indent=2))
    except OSError as e:
        print(f"Error: writing answer results {e}", file=sys.stderr)
        return


def build_context_from_sources(
    retrieved_sources: list[MinimalSource],
    root_path: Path,
) -> str:
    """Construct a textual context by reading slices from source files.

    For each `MinimalSource` in `retrieved_sources`, the function reads
    the corresponding file from `root_path`, extracts the substring
    between `first_character_index` and `last_character_index`, and
    formats the result into a numbered context block.

    Args:
        retrieved_sources: List of `MinimalSource` objects describing
            file paths and character ranges.
        root_path: Base path prepended to each `MinimalSource.file_path`.

    Returns:
        A single string containing all formatted context blocks. If a
        file cannot be read, that source is skipped and an error is
        logged.
    """

    context_parts: list[str] = []

    for source_number, source in enumerate(retrieved_sources, start=1):
        source_path = root_path / source.file_path

        try:
            text = source_path.read_text(encoding="utf-8")
        except OSError as e:
            logging.error(f"{fname()}:Error reading source {source_path}: {e}")
            continue

        chunk_text = text[
            source.first_character_index:source.last_character_index
        ]

        context_parts.append(
            f"[Source {source_number}]\n"
            f"File_path: {source.file_path}\n"
            f"Range: "
            f"{source.first_character_index}-"
            f"{source.last_character_index}\n"
            f"Content: {chunk_text}\n"
        )

    context = "\n\n".join(context_parts)

    return context


def generate_answer_from_sources(
    question: str,
    retrieved_sources: list[MinimalSource],
    root_path: Path,
    model_name: str,
    tokenizer: Any | None,
    model: Any | None,
) -> tuple[str, Any | None, Any | None]:
    """Generate an answer string using pre-retrieved sources.

    This function builds a context from the `retrieved_sources`, loads
    a tokenizer and model if they are not provided, and returns the
    generated answer together with the (possibly newly loaded)
    tokenizer and model so subsequent calls can reuse them.

    Args:
        question: The question text to answer.
        retrieved_sources: List of `MinimalSource` items used to build
            the context.
        root_path: Base path used to resolve `file_path` entries in the
            `retrieved_sources` list.
        model_name: Model identifier used when loading the model.
        tokenizer: Existing tokenizer instance or `None` to load one.
        model: Existing model instance or `None` to load one.

    Returns:
        A tuple `(answer_text, tokenizer, model)` where `answer_text` is
        the generated string, and `tokenizer` and `model` are the
        tokenizer/model used for generation (may be the same objects
        passed in or newly loaded instances).
    """

    if not retrieved_sources:
        return "The provided context is insufficient.", tokenizer, model

    context = build_context_from_sources(
        retrieved_sources=retrieved_sources,
        root_path=root_path,
        )

    if not context:
        return "The provided context is insufficient.", tokenizer, model

    prompt = build_rag_prompt(question, context)
    logging.info(f"{fname()}: prompt: \n{prompt}\n")

    if tokenizer is None or model is None:
        tokenizer, model = load_answer_model(model_name)

    answer_text = generate_answer_with_model(
        prompt=prompt,
        tokenizer=tokenizer,
        model=model,
        max_new_tokens=MAX_NEW_TOKENS,
    )

    return answer_text, tokenizer, model
