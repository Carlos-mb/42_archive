"""Retrieval helpers for building prompts and collecting source chunks."""

import logging
from src.functions import fname
from src.models import Chunk, MinimalSource
from src.storage import load_chunks
import src.tfidf
from pathlib import Path

retriever_cache: src.tfidf.TfidfRetriever | None = None
chunks_docs: list[Chunk] = []
chunks_code: list[Chunk] = []
index_type_cache: str = "all"

MAX_K = 5


def retrieve_sources(
    question: str,
    k: int,
    index_directory: Path,
    index_type: str = "all",
) -> tuple[list[MinimalSource], list[Chunk]]:
    """Retrieve source metadata and chunks for one question."""

    global retriever_cache
    global chunks_docs
    global chunks_code
    global index_type_cache

    if k <= 0:
        return [], []

    if not retriever_cache:
        chunks_docs = (load_chunks(
                (index_directory / "chunks" / "documents.json").as_posix()
            ))
        chunks_code = (load_chunks(
                (index_directory / "chunks" / "code.json").as_posix()
                ))
        chunks_all = chunks_code + chunks_docs
        logging.info(f"{fname()}: retrieving combined index")
        retriever = src.tfidf.TfidfRetriever(chunks_all)
        retriever.load_index(index_directory / "tfid_all_index")
        retriever_cache = retriever
        index_type_cache = "all"
    elif index_type == "documents":
        logging.info(f"{fname()}: retrieving documents index")
        retriever = src.tfidf.TfidfRetriever(chunks_docs)
        retriever.load_index(index_directory / "tfid_documents_index")
        retriever_cache = retriever
        index_type_cache = "documents"
    elif index_type == "code":
        logging.info(f"{fname()}: retrieving code index")
        retriever = src.tfidf.TfidfRetriever(chunks_code)
        retriever.load_index(index_directory / "tfid_code_index")
        retriever_cache = retriever
        index_type_cache = "code"
    else:
        retriever = retriever_cache

    results = retriever.search(question, min(k, MAX_K))

    if (results[0].chunk.file_path.lower().endswith(".md") or
        results[0].chunk.file_path.lower().endswith(".txt")) and\
       index_type_cache != "documents":
        retrieve_sources(question, k, index_directory, "documents")
        retriever = retriever_cache
        results = retriever.search(question, min(k, MAX_K))

    elif results[0].chunk.file_path.endswith(".py") and\
            index_type_cache != "code":
        retrieve_sources(question, k, index_directory, "code")
        retriever = retriever_cache
        results = retriever.search(question, min(k, MAX_K))

    retrieved_chunks = [result.chunk for result in results]

    retrieved_sources = [
        MinimalSource(
            file_path=chunk.file_path,
            first_character_index=chunk.first_character_index,
            last_character_index=chunk.last_character_index,
        )
        for chunk in retrieved_chunks
    ]

    return retrieved_sources, retrieved_chunks


def build_rag_prompt(question: str, context: str) -> str:
    """Build the prompt template used to query the answer model."""

    out: str = """<|im_start|>system
You are a technical assistant answering questions about the vLLM repository.

Use only the provided context.
Do not use external knowledge.
Ignore sources that are not directly relevant to the question.
Do not infer that something is required unless """ + \
        """the provided context explicitly says it.

Give exactly one answer.
Use at most 2 sentences.
Do not repeat the answer.
Do not provide alternative phrasings.
Do not include a separate source list.
Do not explain what each source contains.

Your output must be exactly one short answer.
The answer must end with one or more citations """ + \
        """in this exact format: [Source N].
Do not write an answer without a citation.
Do not include a separate source list.
If the context does not contain the answer, write exactly: """ + \
        """The provided context is insufficient.
<|im_end|>
<|im_start|>user
"""

# - Every factual claim must include a source citation.
# - If the context does not contain enough information, say:
#   "The provided context is insufficient."
# - Do not show reasoning or thinking.
# - Do not invent details that are not supported by the context.
# - Do not continue the conversation.
# - Do not write a new Human, User, Assistant, Question, or Answer turn.
# - Do not explain your reasoning.
# - Return only the final answer.

    out += "Context:\n" + context + "\n"
    # out += "Answer the question and list sources used to answer:\n"
    out += "Question:\n" + question + "\n"
    out += "Required answer format:\n<answer text>. [Source N]"
    out += "\n\n/no_think\n"
    # out += "\nCite the sources you use with [Source N].\n"
    out += "<|im_end|>\n"
    # out += "Answer:\n"
    out += "<|im_start|>assistant\n"
    return out


def build_context(chunks: list[Chunk]) -> str:
    """Serialize retrieved chunks into a numbered context block."""

    if len(chunks) == 0:
        logging.warning(f"{fname()}: No chunks in list")

    # out: str = "-------------------------------------------\n"
    out: str = ""
    for i, chunk in enumerate(chunks, start=1):

        out += f"[Source {i}]\n"
        out += f"Source: {chunk.file_path}\n"
        # out += f"Range: {chunk.first_character_index}-"\
        #        f"{chunk.last_character_index}\n"
        out += f"{chunk.content}\n"
        out += "-------------------------------------------\n"

    return out
