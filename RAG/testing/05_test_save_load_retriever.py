"""
uv run src/05_test_save_load_retriever.py  > test.out
"""
import storage
import markdown
import retrieval
from pprint import pprint


def main():
    chunks = markdown.chunk_markdown_files(root_path="vllm-0.10.1",
                                           max_cs=500,
                                           overlap=50)
    storage.save_chunks(chunks, "borrame")
    chunks = []
    storage.load_chunks("borrame", chunks)
    retriever = retrieval.TfidfRetriever(chunks)
    retriever.build_index()

    tests = ["installation",
             "configuration",
             "OpenAI server",
             "LoRA",
             "Docker",
             "GPU",
             "serving"]

    for test in tests:
        result = retriever.search(test, 5)
        print(f"Testing: {test}")
        for number, result in enumerate(result, start=1):
            print(f"#{number}\n======================")
            pprint(result.chunk.content)
            print("======================")


if __name__=="__main__":
    main()