from .functions import printd, pprintd
import argparse
import pathlib
import json
from typing import Any
from pydantic import ValidationError
from .models import FunctionDefinition, PromptInput, FunctionCallResult
from .call_llm import call_llm


def check_inputfile(filename: pathlib.Path, name: str) -> list[Any] | None:
    """Load a JSON file and ensure its root element is a list."""

    try:
        with open(filename, mode="r") as f:
            data = json.load(f)

    except json.JSONDecodeError:
        print(f"Error: malformed json in {filename}")
        return None

    except FileNotFoundError:
        print(f"Does not exist {filename}")
        return None

    if not isinstance(data, list):
        print(f"Error: json is not a list in {filename}")
        return None

    pprintd(data)
    print(f"Loaded {len(data)} {name} from {filename}")

    return data


def input_validation() -> tuple[list[FunctionDefinition] | None,
                                list[PromptInput] | None,
                                pathlib.Path | None]:
    """Parse CLI arguments and validate all required input files."""

    parser = argparse.ArgumentParser(description="Call Me Maybe From Carlos")
    parser.add_argument('--functions_definition',
                        type=pathlib.Path,
                        metavar="FILE",
                        default=pathlib.Path(
                            "data/input/functions_definition.json"),
                        help="Functions definition json file")
    parser.add_argument('--input', type=pathlib.Path,
                        metavar="FILE",
                        default=pathlib.Path(
                            "data/input/function_calling_tests.json"),
                        help="Input json file")
    parser.add_argument('--output', type=pathlib.Path,
                        metavar="FILE",
                        default=pathlib.Path(
                            "data/output/function_calling_results.json"),
                        help="Output json file")

    args = parser.parse_args()

    printd("=" * 40)
    printd("Received Parameters:")
    printd("functions_definition:", args.functions_definition)
    printd("input:", args.input)
    printd("output:", args.output)
    printd("=" * 40)

    definitions = check_inputfile(getattr(args, "functions_definition"),
                                  "functions")

    prompts = check_inputfile(getattr(args, "input"),
                              "prompts")

    if definitions is None or prompts is None:
        return None, None, None

    output_file: pathlib.Path = getattr(args, "output")

    # confirm: str = ""

    if output_file.exists():
        if not output_file.is_file():
            print("Error: output is not a valid file name")
            return None, None, None

    validated_definitions = validate_function_definitions(definitions)
    validated_prompts = validate_prompts(prompts)

    if validated_definitions is None or validated_prompts is None:
        return None, None, None

    return (
            validated_definitions,
            validated_prompts,
            getattr(args, "output"))


def validate_prompts(prompts: list[Any]) -> list[PromptInput] | None:
    """Validate prompt input items with Pydantic."""

    result: list[PromptInput] = []

    for index, prompt in enumerate(prompts):
        try:
            result.append(PromptInput.model_validate(prompt))
        except ValidationError as e:
            print(f"Error: invalid prompt at index {index}: {e}")
            return None
    printd("Prompt validation result:")
    pprintd(result)
    return result


def validate_function_definitions(
        definitions: list[Any]) -> list[FunctionDefinition] | None:
    """Validate function definitions with Pydantic."""

    result: list[FunctionDefinition] = []

    for index, definition in enumerate(definitions):
        try:
            result.append(FunctionDefinition.model_validate(definition))
        except ValidationError as e:
            print("Error: invalid function definition"
                  f" at index {index}: {e}")
            return None

    return result


def createoutput(output_path: pathlib.Path,
                 data: list[dict[str, object]]) -> bool:
    """Write validated function call results to a JSON output file."""

    result: list[FunctionCallResult] = []
    for index, value in enumerate(data):
        try:
            result.append(FunctionCallResult.model_validate(value))
        except ValidationError as e:
            print("Error creating output file:"
                  f" invalid output in index {index}: {e}")
            return False

    try:

        #  Create only the immediate output directory.
        #  Do not create missing ancestor directories.

        output_path.parent.mkdir(exist_ok=True)

        finaljson: list[dict[str, object]] = []

        for model in result:
            finaljson.append(model.model_dump())

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(finaljson, f, indent=4)

    except (PermissionError, FileNotFoundError, OSError, FileExistsError) as e:
        print(f"Error: {e}")
        return False

    return True


def main() -> None:

    validated_definitions, validated_prompts, output_path = input_validation()

    if (validated_prompts is None or
            validated_definitions is None or
            output_path is None):
        print("Exiting.")
        return

    result = call_llm(validated_definitions, validated_prompts)

    if not createoutput(output_path, result):
        print("Exiting.")

    return


if __name__ == "__main__":
    main()
