"""Pydantic models used to validate project input and output data."""

from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field


class PromptInput(BaseModel):
    """Validate one prompt item from function_calling_tests.json."""

    # I'm going to configure a dict
    # The dict does not allow more keys than the specified later ...
    model_config = ConfigDict(extra="forbid")

    # ... these are the accepted keys:

    # Key "prompt", value "str" with min length of 1
    prompt: str = Field(min_length=1)


class TypeDefinition(BaseModel):
    """Validate a JSON type definition."""

    model_config = ConfigDict(extra="forbid")
    type: Literal["string", "number", "boolean", "integer"]


class FunctionDefinition(BaseModel):
    """Validate one function definition from functions_definition.json."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    parameters: dict[str, TypeDefinition]
    returns: TypeDefinition


class FunctionCallResult(BaseModel):
    """Validate one generated function call result."""

    model_config = ConfigDict(extra="forbid")

    prompt: str = Field(min_length=1)
    name: str = Field(min_length=1)
    parameters: dict[str, Any]
