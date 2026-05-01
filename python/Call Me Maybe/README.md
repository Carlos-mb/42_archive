*This project has been created as part of the 42 curriculum by cmelero-.*

# call me maybe

## Description

`call me maybe` is an introduction to function calling with local Large Language Models.

The goal of the project is to translate natural language prompts into structured function calls. The program does not execute the requested operation and does not return the final answer to the user. Instead, it identifies the function that should be called and extracts the arguments required by that function.

For example, given this prompt:

```text
What is the sum of 40 and 2?
```

The expected output is not:

```text
42
```

The expected output is a structured function call:

```json
{
  "prompt": "What is the sum of 40 and 2?",
  "name": "fn_add_numbers",
  "parameters": {
    "a": 40.0,
    "b": 2.0
  }
}
```

The main technical challenge is to make a small local language model produce reliable structured output. The project therefore uses constrained decoding to restrict the generation process so that the produced output is valid JSON and follows the expected schema.

## Project goals

The project focuses on the following goals:

- Load and validate function definitions from JSON.
- Load and validate natural language prompts from JSON.
- Use a local LLM through the provided `llm_sdk` package.
- Select the function to call using the LLM.
- Extract function arguments from natural language.
- Generate a JSON output file with exactly the expected structure.
- Guarantee that the final output is valid JSON.
- Avoid relying only on prompt engineering for structured generation.
- Handle invalid input files and execution errors gracefully.

## Requirements

The project uses Python 3.10 or later.

The required dependencies are managed with `uv`.

Main dependencies:

- `pydantic`
- `numpy`
- `llm_sdk`, provided with the subject

The project intentionally avoids external libraries that would solve the constrained generation problem directly.

Forbidden or intentionally unused packages include:

- `transformers`
- `torch`
- `huggingface`
- `dspy`
- `outlines`
- similar structured-generation frameworks

## Repository structure

The expected repository structure is:

```text
.
├── data/
│   └── input/
│       ├── functions_definition.json
│       └── function_calling_tests.json
├── llm_sdk/
├── src/
│   ├── __init__.py
│   ├── __main__.py
│   ├── functions.py
│   └── models.py
├── pyproject.toml
├── uv.lock
├── Makefile
├── README.md
├── BACKLOG.md
├── ITERATIONS.md
└── CHECKLIST.md
```

The `data/output/` directory is generated at runtime and should not be committed to the repository.

## Input files

The program reads two input files.

### Function definitions

By default:

```text
data/input/functions_definition.json
```

This file contains the list of functions available to the system.

Each function definition includes:

- function name
- function description
- parameter names
- parameter types
- return type

Example:

```json
[
  {
    "name": "fn_add_numbers",
    "description": "Add two numbers together and return their sum.",
    "parameters": {
      "a": {
        "type": "number"
      },
      "b": {
        "type": "number"
      }
    },
    "returns": {
      "type": "number"
    }
  }
]
```

### Prompt input file

By default:

```text
data/input/function_calling_tests.json
```

This file contains the natural language prompts to process.

Example:

```json
[
  {
    "prompt": "What is the sum of 2 and 3?"
  },
  {
    "prompt": "Reverse the string 'hello'"
  }
]
```

## Output file

By default, the program writes:

```text
data/output/function_calling_results.json
```

The output file contains a JSON array. Each item contains exactly these keys:

- `prompt`
- `name`
- `parameters`

Example:

```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {
      "a": 2.0,
      "b": 3.0
    }
  },
  {
    "prompt": "Reverse the string 'hello'",
    "name": "fn_reverse_string",
    "parameters": {
      "s": "hello"
    }
  }
]
```

The output must not contain comments, trailing commas, explanations, debug text, or extra keys.

## Instructions

### Install dependencies

```bash
uv sync
```

### Run with default paths

```bash
uv run python -m src
```

Default input paths:

```text
data/input/functions_definition.json
data/input/function_calling_tests.json
```

Default output path:

```text
data/output/function_calling_results.json
```

### Run with custom paths

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calls.json
```

### Run with debug output

Debug messages are controlled through the `CALLME_DEBUG` environment variable.

```bash
CALLME_DEBUG=ON uv run python -m src
```

Debug information is written to standard error so that the JSON output file is not polluted.

### Run linting

```bash
make lint
```

The lint target is expected to run:

```bash
flake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

### Clean temporary files

```bash
make clean
```

## Makefile targets

The project Makefile contains the following targets:

- `install`: install project dependencies.
- `run`: run the main program.
- `debug`: run the main program in debug mode.
- `clean`: remove temporary Python and tooling files.
- `lint`: run flake8 and mypy with the required flags.

## Data validation

The project uses Pydantic models to validate input and output data.

The main validation models are:

- `PromptInput`: validates each prompt item.
- `TypeDefinition`: validates JSON type definitions.
- `FunctionDefinition`: validates each available function.
- `FunctionCallResult`: validates each generated function call before writing the output file.

The program validates:

- missing files
- malformed JSON
- JSON root elements that are not arrays
- invalid prompt objects
- invalid function definitions
- unsupported parameter types
- invalid generated output objects
- output paths that cannot be written

The program is designed to terminate cleanly with a clear error message instead of crashing with an unhandled exception.

## LLM interaction

The project uses the provided `Small_LLM_Model` class from `llm_sdk`.

The explored public SDK methods are:

- `encode(text)`
- `decode(token_ids)`
- `get_logits_from_input_ids(input_ids)`
- `get_path_to_tokenizer_file()`

The general LLM interaction flow is:

1. Build a prompt from the user request and the available function definitions.
2. Encode the text into token IDs.
3. Send the token IDs to the model.
4. Retrieve logits for the next token.
5. Select the next valid token according to the constrained decoding state.
6. Append the selected token to the generated output.
7. Repeat the process until the complete JSON object has been generated.
8. Parse and validate the result before writing it to the output file.

## Algorithm explanation: constrained decoding

The project does not rely on asking the model to "please return valid JSON".

Prompt-only JSON generation is not reliable enough with small language models. A small model may produce extra text, invalid commas, wrong keys, missing parameters, or arguments with incorrect types.

The constrained decoding approach used in this project treats generation as a controlled state machine.

At each generation step:

1. The current partial output is inspected.
2. The decoder determines which part of the JSON object is currently being generated.
3. A set of valid next token candidates is built.
4. Tokens that would break the JSON structure or the expected schema are rejected.
5. The LLM logits are used only to choose among the currently valid candidates.
6. The selected token is appended to the output.
7. The state machine advances to the next generation state.

The generated object must follow this structure:

```json
{
  "name": "<function_name>",
  "parameters": {
    "<parameter_name>": "<parameter_value>"
  }
}
```

The final program then combines the generated function call with the original prompt to produce the required output item:

```json
{
  "prompt": "<original_prompt>",
  "name": "<function_name>",
  "parameters": {
    "<parameter_name>": "<parameter_value>"
  }
}
```

### Function name constraint

The `name` field is restricted to the names present in `functions_definition.json`.

The model can influence which function is selected, but it cannot generate an arbitrary function name that does not exist in the input schema.

### Parameter name constraint

After the function name has been selected, the allowed parameter names are restricted to the parameters defined for that specific function.

For example, if the selected function is:

```json
{
  "name": "fn_add_numbers",
  "parameters": {
    "a": {
      "type": "number"
    },
    "b": {
      "type": "number"
    }
  }
}
```

then only `a` and `b` are valid parameter keys.

No extra parameter names are allowed.

### Parameter type constraint

Each generated parameter value must match the type declared in the function definition.

Supported types include:

- `string`
- `number`
- `boolean`

The decoder enforces these constraints during generation and the final result is validated again with Pydantic before being written to disk.

### JSON structure constraint

The decoder only allows tokens that keep the output compatible with valid JSON.

This prevents:

- extra prose
- missing braces
- invalid commas
- invalid quotes
- unexpected keys
- malformed objects
- text before or after the JSON object

The final output file is produced with Python's `json` module to ensure that the file written to disk is valid JSON.

## Design decisions

### Python package entry point

The project is executed with:

```bash
uv run python -m src
```

For that reason, the main execution flow is placed in:

```text
src/__main__.py
```

The file:

```text
src/__init__.py
```

is intentionally kept empty. It only marks `src` as a Python package.

### Pydantic validation

Pydantic is used for structured validation because the project receives external JSON files and must fail cleanly when the input format is invalid.

The models forbid unexpected fields where appropriate. This helps detect incorrect input early and prevents invalid structures from silently propagating through the pipeline.

### Output validation before writing

Generated results are validated as `FunctionCallResult` objects before being written to the output file.

This creates a final safety layer between generation and file writing.

### Debug output separated from JSON output

Debug helpers write to standard error and are enabled only when:

```text
CALLME_DEBUG=ON
```

This avoids contaminating the JSON output with diagnostic text.

### No interactive overwrite confirmation

The program does not ask for interactive confirmation before overwriting the output file.

This is intentional because the project must run automatically during evaluation.

### Local SDK isolation

The LLM exploration was done separately before being integrated into the final pipeline.

This avoided mixing experimental LLM code with the stable JSON input/output pipeline too early.

### No private SDK methods

The project uses only public methods exposed by `llm_sdk`.

Private attributes and private methods are avoided to keep the implementation compatible with the evaluation environment.

## Performance analysis

The expected project targets are:

- valid JSON rate: 100%
- schema-compliant output rate: 100%
- correct function and argument extraction: at least 90%
- total runtime for the provided test prompts: under 4 minutes on standard hardware

Current validation strategy focuses on two different reliability levels:

1. Structural reliability:
   The output must always be valid JSON and must follow the required schema.

2. Semantic accuracy:
   The selected function and extracted arguments must match the natural language request.

The most expensive part of the application is the interaction with the local language model. The rest of the pipeline is comparatively lightweight: loading JSON files, validating data with Pydantic, building the constrained decoding state, filtering valid candidates, and writing the final output file do not introduce significant delays.

During execution, the only point where the application noticeably stops is when it calls the LLM through `get_logits_from_input_ids()`. This method performs the actual model inference and therefore requires a large amount of CPU time.

A major performance improvement was achieved by reducing the size of the prompt. Since every inference call depends on the amount of context sent to the model, long prompts caused a significant slowdown. I spent a considerable amount of effort simplifying the prompt as much as possible while still preserving enough information for the model to choose the correct function and extract the required arguments.

With the optimized prompt, the application reaches:

- 100% success rate in function selection for the provided test prompts.
- 100% success rate in generating a valid output JSON file.
- 100% schema-compliant output for the tested cases.

The total execution time is approximately 5 minutes on a virtual machine with 32 GB of RAM and 16 CPU cores. This runtime is still high, even though the constrained decoding process only requires a limited number of LLM inference steps.

Based on my own measurements and comparison with other students working with similar hardware, running this project significantly faster with the current CPU-based resources does not appear to be realistic. The main bottleneck is not the Python control logic, but the cost of repeatedly invoking the local LLM.

The final implementation therefore prioritizes correctness and reliability over aggressive performance optimization. The prompt was reduced to the minimum useful size, the output is structurally constrained, and the generated file is valid and compliant with the expected schema.

### Rejection behavior during constrained decoding

During the official test runs, the number of rejected tokens may be very low or even zero. This does not mean that constrained decoding is disabled. It means that, with the current optimized prompt and the initial generation prefix, the highest-ranked token proposed by the LLM is usually already valid.

The generation currently starts from this partial JSON prefix:

```python
evolution = '{"name":"'
```

This prefix intentionally places the model directly inside the expected JSON structure. As a result, many invalid continuations are avoided before the first LLM inference step.

The prompt also includes this instruction:

```text
JSON has to be compacted and no extra spaces.
```

This reduces formatting variability and helps the model produce tokens that match the constrained decoder path.

The number of rejected tokens can be increased for demonstration purposes by making the generation less guided. For example:

```python
evolution = ""
```

or by removing this prompt instruction:

```text
JSON has to be compacted and no extra spaces.
```

When these constraints are relaxed, the model is more likely to propose tokens such as extra spaces, explanatory text, alternative field names, or malformed JSON fragments. In those cases, the constrained decoder rejects invalid candidates and continues searching for the best valid token.

For the final implementation, the optimized version is preferred because it keeps the model on the correct path, improves execution speed, and still validates every generated token before appending it to the output.

## Challenges faced

### Understanding the role of the LLM

A key challenge was separating what the LLM should decide from what the program should guarantee.

The LLM should help choose the function and infer argument values, but the program must guarantee the output structure.


### Handling invalid JSON input files

Input files may be missing, malformed, or structurally invalid.

The project therefore validates the JSON root type and each item inside the input arrays.

### Keeping debug output away from the final JSON file

The output file must contain only JSON.

For that reason, debug information is written to standard error and controlled by an environment variable.

### Understanding tokenizer behavior

The tokenizer does not split text like a normal string split operation. Tokens may include leading spaces, punctuation, or subword fragments.

This matters for constrained decoding because valid JSON fragments may correspond to one token or to several tokens.

### SDK method differences

During exploration, the SDK method available for accessing tokenizer data was `get_path_to_tokenizer_file()`.

The tokenizer JSON contains the vocabulary information needed to inspect token-to-text mappings.


### Input validation tests

Test cases:

- missing `functions_definition.json`
- missing `function_calling_tests.json`
- malformed JSON
- root JSON value is not an array
- prompt item without `prompt`
- prompt item with extra fields
- function definition without `name`
- function definition with invalid parameter type
- function definition with extra fields
- tests provided by the project
- extra extreme cases in function_calling_test_extreme.json

### Output validation tests

Test cases:

- output root is a JSON array
- each output item contains `prompt`
- each output item contains `name`
- each output item contains `parameters`
- no extra keys are present
- output can be parsed again with `json.load`
- generated parameters match the selected function definition

### LLM interaction tests

Test cases:

- model can be instantiated
- text can be encoded
- token IDs can be decoded
- logits can be retrieved
- logits shape is understood
- no private SDK methods are used

### Constrained decoding tests

Test cases:

- generated JSON cannot contain prose
- function names are restricted to available functions
- parameter names are restricted to the selected function
- string parameters are generated as JSON strings
- number parameters are generated as JSON numbers
- boolean parameters are generated as JSON booleans
- invalid tokens are rejected
- partial invalid JSON is not accepted as a final result

### Manual end-to-end test

Run:

```bash
rm -rf data/output
uv run python -m src
python -m json.tool data/output/function_calling_results.json
```

Expected result:

- the command finishes cleanly
- `data/output/function_calling_results.json` exists
- the file is valid JSON
- the file contains an array
- each item follows the required schema

## Example usage

### Default execution

```bash
uv run python -m src
```

### Custom input and output files

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calls.json
```

### Validate generated JSON manually

```bash
python -m json.tool data/output/function_calling_results.json
```

### Debug execution

```bash
CALLME_DEBUG=ON uv run python -m src
```

## Example input and output

Input prompt:

```json
{
  "prompt": "Greet john"
}
```

Available function:

```json
{
  "name": "fn_greet",
  "description": "Generate a greeting message for a person by name.",
  "parameters": {
    "name": {
      "type": "string"
    }
  },
  "returns": {
    "type": "string"
  }
}
```

Expected output item:

```json
{
  "prompt": "Greet john",
  "name": "fn_greet",
  "parameters": {
    "name": "john"
  }
}
```

## Error handling

The program is designed to report errors clearly and terminate cleanly.

Examples of handled errors:

- input file does not exist
- input file contains malformed JSON
- input JSON root is not an array
- prompt object is invalid
- function definition is invalid
- output path is invalid
- output file cannot be written
- generated function call does not match the expected schema

The program should not crash with an unhandled traceback during normal error scenarios.

## Resources

Resources used to understand and implement the project:

- Python documentation: `json`
- Python documentation: `argparse`
- Python documentation: `pathlib`
- Python documentation: `typing`
- Pydantic documentation
- uv documentation
- flake8 documentation
- mypy documentation
- The provided `llm_sdk` package
- The `call me maybe` subject PDF

## Use of AI

AI was used as a learning and planning assistant during the project.

It was used for:

- clarifying the project requirements
- organizing the work into iterations
- reviewing the project checklist
- discussing the role of constrained decoding
- understanding the interaction between tokenizer, token IDs, logits, and next-token selection
- planning tests and validation strategy
- drafting documentation

## Notes for evaluation

The repository should include:

- `src/`
- `pyproject.toml`
- `uv.lock`
- `llm_sdk/`
- `data/input/`
- `README.md`
- any additional files required to run the solution

The repository should not include:

```text
data/output/
```

The output directory is generated when the program runs.

Before submission, run:

```bash
uv sync
uv run python -m src
python -m json.tool data/output/function_calling_results.json
make lint
```

## Optional: using external storage for uv and model cache

This project can be kept on the local disk while moving the heavy generated files to another storage location. This is useful on systems where the local disk has limited free space.

The repository itself only needs to contain the source code, configuration files, `llm_sdk/`, input examples, and documentation. The virtual environment, uv cache, temporary files, and downloaded model cache can be stored outside the repository.

Example setup using `/home/userlogin/sgoinfre`:

```bash
mkdir -p /home/userlogin/sgoinfre/callme/{uv-cache,venv,huggingface,tmp,python,xdg-cache}
```

Create a local file named `local-env.sh` at the root of the project:

```bash
export CALLME_STORAGE="/home/userlogin/sgoinfre/callme"

export UV_CACHE_DIR="$CALLME_STORAGE/uv-cache"
export UV_PROJECT_ENVIRONMENT="$CALLME_STORAGE/venv"
export UV_PYTHON_INSTALL_DIR="$CALLME_STORAGE/python"

export HF_HOME="$CALLME_STORAGE/huggingface"
export HF_HUB_CACHE="$HF_HOME/hub"

export TMPDIR="$CALLME_STORAGE/tmp"
export XDG_CACHE_HOME="$CALLME_STORAGE/xdg-cache"
```

Before installing dependencies or running the project, load the environment variables:

```bash
source ./local-env.sh
uv sync
uv run python -m src
```

To verify that uv is using the external storage location:

```bash
uv cache dir
uv run python -c "import sys; print(sys.prefix)"
echo "$HF_HOME"
```

The output should point to paths under:

```text
/home/userlogin/sgoinfre/callme
```

The `local-env.sh` file is machine-specific and must not be committed to the repository. Add it to `.gitignore`:

```text
local-env.sh
```

This setup does not change the project logic. It only changes where uv, the virtual environment, temporary files, and the local model cache are stored.