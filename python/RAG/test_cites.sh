# ./exams/scripts/exam_answer.sh --student-path . --moulinette-path ./moulinette-ubuntu --questions "What Python packages need to be installed to use vLLM with LangChain?","What runner parameter should be specified to use a model in pooling mode instead of generative mode in vLLM?","What is the CLI command to start vLLM serve?"

# uv run python -m src answer "What runner parameter should be specified to use a model in pooling mode instead of generative mode in vLLM?" --k 2
#  uv run python -m src answer "What runner parameter should be specified to use a model in pooling mode instead of generative mode in vLLM?" --k 2
#uv run python -m src answer "What is the CLI command to start vLLM serve?" --k 10
#uv run python -m src answer "What Python packages need to be installed to use vLLM with LangChain?" --k 10


./exams/scripts/exam_answer.sh --student-path . --moulinette-path ./moulinette-ubuntu --questions "What factors can cause variations in generated outputs when using speculative decoding in vLLM?","How do you profile a vLLM server using nsys with CUDA graph tracing?","Where can I find instructions for building vLLM Docker image from source?"
uv run python -m src answer "What factors can cause variations in generated outputs when using speculative decoding in vLLM?" --k 10 -- debug 