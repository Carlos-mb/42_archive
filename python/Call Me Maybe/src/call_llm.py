from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]
from .models import FunctionDefinition, PromptInput
import json
import re
from .functions import printd, printrepd


def call_llm(definitions: list[FunctionDefinition],
             prompts: list[PromptInput]) -> list[dict[str, object]]:

    my_ai = Small_LLM_Model()
    output: list[dict[str, object]] = []

    context = """You are a function call generator.

Your task is to generate a JSON function call using "name" and "parameters".
JSON has to be minifie, compact, not indented.
If a regex needs a backslash, the backslash must be escaped for JSON.
The regex \\d+ must be written as "\\\\d+" in JSON.
Arguments declared with type "number" must be emitted as JSON numbers with a decimal part, for example 3.0 instead of 3.
Never remove, rewrite, summarize, normalize, or reinterpret the content of string arguments.

"""

    context += "Available functions:\n"

    for function in definitions:
        context += f"- {function.name}("
        comma = ""
        for name, type in function.parameters.items():
            context += f"{comma}{name}: {type.type}"
            comma = ", "
        context += f"): {function.description}\n"

    for prompt in prompts:
    # prompt = prompts[10]
    # if True:

        # VERY IMPORTANT: this has to be the last line and
        # include the Answer: text
        # If I remove the "Answer:" the IA puts it, I reject the token and
        # it modifies the path. In this case, it does not generated a valid
        # regex as 1st token in prompt 9

        request = f'User request: {prompt.prompt}\nAnswer:\n'
        evolution = '{"name":"'
        final = False

        printd(f"PROMPT: {prompt.prompt}")
        printd("Full prompt: \n" + context + "\n" + request + "\n" + evolution)
        printd(f"\n Scaped PROMPT: {prompt.prompt}")
        printrepd("\n" + context + "\n" + request + "\n" + evolution)

        while not final:

            current = context + "\n" + request + "\n" + evolution

            # Ask to IA
            tensor2d = my_ai.encode(current)

            my_ids_int: list[int] = []

            for tensor in tensor2d:
                for token_id_tensor in tensor:
                    my_ids_int.append(int(token_id_tensor))

            my_logits = my_ai.get_logits_from_input_ids(my_ids_int)

            best_rank = float("-inf")
            best_token = 0

            ordered = sorted(enumerate(my_logits),
                             key=lambda item: item[1], reverse=True)

            for token_id, logit in ordered:
                token_text = my_ai.decode([token_id])

                if best_rank < my_logits[token_id]:

                    goodway, final = isvalidcombination(evolution,
                                                        token_text,
                                                        definitions)

                    if goodway:
                        best_rank = my_logits[token_id]
                        best_token = token_id
                        # Print current prompt for debuging:
                        printd("ACEPTADO:")
                        printrepd(evolution+token_text)
                        printd("-" * 40)
                        break
                    else:
                        printd("RECHAZADO:")
                        printrepd(evolution+token_text)
                        printd("-" * 40)
                        my_logits[token_id] = float("-inf")
                    # goodway = True
                    # final = False

                    # best_rank = my_logits[token_id]
                    # best_token = token_id
                    # break
            if best_rank == float("-inf"):
                print(f"ERROR: Can't resolve request {prompt.prompt}")
                return []

            evolution += my_ai.decode([best_token])

        try:
            tmp = json.loads(evolution)
            tmp["prompt"] = prompt.prompt
            output.append(tmp)
        except json.JSONDecodeError:
            print("ERROR: Invalid JSON for prompt"
                  f" {evolution} for prompt:{prompt.prompt}")
            return []

    return output


def optional(mixed: str, expected: str, string: str) -> str:

    if len(mixed) > len(expected):
        pos_expected = expected + string
        if mixed[:min(len(mixed), len(pos_expected))] ==\
           pos_expected[:min(len(mixed), len(pos_expected))]:
            expected += string

    return expected


def isvalidcombination(evolution: str,
                       token_text: str,
                       definitions: list[FunctionDefinition]) \
                        -> tuple[bool, bool]:

    # {"name": "fn_add_numbers","parameters": {"a":2,"b":3}}

    final = False
    function: FunctionDefinition | None = None

    mixed = evolution + token_text
    curlen = len(mixed)

    output = False
    expected = '{'

    # If I allow \n I'll have to manage indentations
    # I prefer not do it :)
    # expected = optional(mixed, expected, "\n")
    # output = mixed[:min(curlen, len(expected))] ==\
    #     expected[:min(curlen, len(expected))]

    if mixed[:min(curlen, len(expected))] ==\
       expected[:min(curlen, len(expected))]:
        output = True
        expected += '"name":'

    output = mixed[:min(curlen, len(expected))] ==\
        expected[:min(curlen, len(expected))]

    expected = optional(mixed, expected, " ")

    output = mixed[:min(curlen, len(expected))] ==\
        expected[:min(curlen, len(expected))]

    # {"name": "fn_add_numbers","parameters":{"a":2,"b":3}}
    if output and curlen > len(expected):
        output = False
        for function in definitions:
            new_expected = expected + '"' + function.name
            if mixed[:min(curlen, len(new_expected))] == \
               new_expected[:min(curlen, len(new_expected))]:
                output = True
                expected = new_expected
                break

    if output and curlen > len(expected):
        output = False
        expected = expected + '",'
        if mixed[:min(curlen, len(expected))] ==\
           expected[:min(curlen, len(expected))]:
            output = True
            expected = optional(mixed, expected, " ")
            output = mixed[:min(curlen, len(expected))] ==\
                expected[:min(curlen, len(expected))]

    if output and curlen > len(expected):
        output = False
        expected = expected + '"parameters":'
        if mixed[:min(curlen, len(expected))] ==\
           expected[:min(curlen, len(expected))]:
            output = True
            expected = optional(mixed, expected, " ")
            output = mixed[:min(curlen, len(expected))] ==\
                expected[:min(curlen, len(expected))]

    # {"name": "fn_add_numbers", "parameters": {"a":2,"b":3}}

    if output and curlen > len(expected):
        output = False
        expected = expected + '{'
        if mixed[:min(curlen, len(expected))] ==\
           expected[:min(curlen, len(expected))]:
            output = True

    if output and curlen > len(expected):
        output = False
        expected = expected + '"'
        if mixed[:min(curlen, len(expected))] ==\
           expected[:min(curlen, len(expected))]:
            output = True

    parameters: list[str] = []
    parameter = ""
    parameter_value = ""
    final = False

    # while there is a function, we are in the good way (output == True)
    # and still there are text to check...

    while function and (output and curlen > len(expected) and
                        len(parameters) < len(function.parameters)):

        if output and curlen > len(expected):
            output = False
            oldexpected = expected
            for parameter in function.parameters:
                if parameter not in parameters:  # Reject duplicated parameter
                    expected = oldexpected + parameter + '":'
                    if mixed[:min(curlen, len(expected))] == \
                       expected[:min(curlen, len(expected))]:
                        parameters.append(parameter)  # Parameter identified
                        output = True
                        expected = optional(mixed, expected, " ")
                        output = mixed[:min(curlen, len(expected))] ==\
                            expected[:min(curlen, len(expected))]
                        break

        # In the good way, still text to check and not the end
        if output and curlen > len(expected) and not final:
            output = False
            next_char = mixed[len(expected):len(expected)+1]
            parameter_value = ""
            if function.parameters[parameter].type == "number":
                output = True
                if next_char == '-':
                    parameter_value += next_char
                    expected += next_char
                    next_char = mixed[len(expected):len(expected)+1]
                while output and next_char and \
                        (next_char.isnumeric() or next_char == "."):
                    if next_char == "." and ("." in parameter_value or
                                             parameter_value == "" or
                                             parameter_value == "-"):
                        output = False
                    else:
                        expected += next_char
                        parameter_value += next_char
                        if (len(parameter_value) == 2
                                and parameter_value.startswith("0")
                                and parameter_value != "0."):
                            output = False
                        elif (len(parameter_value) == 3
                                and parameter_value.startswith("-0")
                                and parameter_value != "-0."):
                            output = False
                        next_char = mixed[len(expected):len(expected)+1]
            elif function.parameters[parameter].type == "integer":
                output = True
                if next_char == '-':
                    parameter_value += next_char
                    expected += next_char
                    next_char = mixed[len(expected):len(expected)+1]
                while output and next_char and \
                        (next_char.isnumeric()):
                    expected += next_char
                    parameter_value += next_char
                    if (len(parameter_value) == 2
                            and parameter_value.startswith("0")):
                        output = False
                    elif (len(parameter_value) == 3
                            and parameter_value.startswith("-0")):
                        output = False
                    next_char = mixed[len(expected):len(expected)+1]
            elif function.parameters[parameter].type == "string":
                if next_char == '"':
                    expected += next_char
                    output = True
                    parameter_value += next_char
                    next_char = mixed[len(expected):len(expected)+1]
                    scape_mode = 0
                    scaped_quote = False
                    while (output and
                            next_char and
                            (next_char.isalnum() or
                             next_char in "\\.,'/+- _:;?!@#*=[]{}()|" or
                             (scaped_quote and next_char == '"'))):
                        scaped_quote = False
                        if next_char == "\\":
                            scape_mode += 1
                        expected += next_char
                        parameter_value += next_char
                        next_char = mixed[len(expected):len(expected)+1]
                        if next_char:
                            if scape_mode == 1:
                                output = next_char in '\\"nr'
                                if next_char != '\\':
                                    scape_mode = 0
                                if next_char == '"':
                                    scaped_quote = True
                            elif scape_mode == 2:
                                # if next_char not in "\\dDwWsSbB.+*?()[]{}|":
                                #     output = False
                                if next_char != "\\":
                                    scape_mode = 0
                            elif scape_mode == 3:
                                if next_char != "\\":
                                    output = False
                                else:
                                    scape_mode = 0
                    if next_char == '"' and not scaped_quote:
                        expected += next_char
                        parameter_value += next_char
                        next_char = mixed[len(expected):len(expected)+1]
                else:
                    output = False
            elif function.parameters[parameter].type == "boolean":
                if next_char.upper() == "F":
                    i = 0
                    while i < 4 and output and next_char:
                        if next_char.upper() == "FALSE"[i]:
                            expected += next_char
                            output = True
                            parameter_value += next_char
                            next_char = mixed[len(expected):len(expected)+1]
                        else:
                            output = False
                        i += 1
                elif next_char.upper() == "T":
                    i = 0
                    while i < 4 and output and next_char:
                        if next_char.upper() == "TRUE"[i]:
                            expected += next_char
                            output = True
                            parameter_value += next_char
                            next_char = mixed[len(expected):len(expected)+1]
                        else:
                            output = False
                        i += 1
                else:
                    output = False

        if output and curlen > len(expected) and not final:
            next_char = mixed[len(expected):len(expected)+1]
            if function.parameters[parameter].type == "number":
                output = bool(
                        re.fullmatch(r"^-?(?:0|[1-9]\d*)\.\d+$",
                                     parameter_value))

            if output:
                if len(parameters) < len(function.parameters):
                    expected += ','
                    expected = optional(mixed, expected, " ")
                    output = mixed[:min(curlen, len(expected))] ==\
                        expected[:min(curlen, len(expected))]
                    if output:
                        expected += '"'
                else:
                    expected += "}}"
                    expected = optional(mixed, expected, "\n")
                    final = True

                output = mixed[:min(curlen, len(expected))] ==\
                    expected[:min(curlen, len(expected))]

    if final:
        final = output and expected == mixed

    if output and len(mixed) > len(expected):
        output = False

    # if final:
    #     print ("final", expected, mixed)

    return output, final
