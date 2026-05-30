import storage
import markdown
import retrieval
from pprint import pprint
from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]
from enum import Enum
import logging

class special_tokens (Enum):
    END_OF_TEXT = 151643
    IM_START = 151644
    IM_END = 151645
    THINK_START = 151667
    THINK_END = 151668


def main():
    chunks = markdown.chunk_markdown_files(root_path="vllm-0.10.1",
                                           max_cs=500,
                                           overlap=50)
    storage.save_chunks(chunks, "borrame")
    chunks = []
    storage.load_chunks("borrame", chunks)
    retriever = retrieval.TfidfRetriever(chunks)
    retriever.build_index()

    question = "How can I run the OpenAI compatible server?"

    results: list[retrieval.SearchResult] = retriever.search(question, 5)
    context: str = retrieval.build_context([r.chunk for r in results])
    prompt: str = retrieval.build_rag_prompt(question, context)

    print(f"Testing: {prompt}")

    my_ai = Small_LLM_Model()
    tensor2d = my_ai.encode(prompt)
    prompt_ids: list[int] = []
    out: str = ""

    for tensor in tensor2d:
        for token_id_tensor in tensor:
            prompt_ids.append(int(token_id_tensor))

    generated_ids: list[int] = []
    output_ids: list[int] = []
    my_logits = my_ai.get_logits_from_input_ids(prompt_ids)
    thinking: bool = False

    ordered = []

    for _ in range(100):
        ordered = sorted(enumerate(my_logits),
                         key=lambda item: item[1], reverse=True)

        generated_ids.append(ordered[0][0])
        my_logits = my_ai.get_logits_from_input_ids(prompt_ids + generated_ids)

        if ordered[0][0] == special_tokens.THINK_START.value:
            thinking = True
            continue

        if ordered[0][0] == special_tokens.THINK_END.value:
            thinking = False
            continue

        if ordered[0][0] in [special_tokens.END_OF_TEXT.value,
                             special_tokens.IM_END.value]:
            break

        # token = my_ai.decode([ordered[0][0]])
        # if token == "<think>":
        #     print(ordered[0][0])
        # if token == "</think>":
        #     print(ordered[0][0])            
        # if token == "":
        #     print(f"Empty: -{ordered[0][0]}-")
        #  <think>      151667
        # \n\n          271
        # </think>      151668

        if not thinking:
            output_ids.append(ordered[0][0])
        logging.debug(my_ai.decode(output_ids))
        print(".", end="", flush=True)

    out = my_ai.decode(output_ids)
    print(out)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()

