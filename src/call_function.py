import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from openai.types.responses import ResponseFunctionToolCall

from config import WORKING_DIRECTORY
from functions import get_file_content, get_files_info, run_python_file, write_file


@dataclass(frozen=True, slots=True)
class ToolCallResult:
    """The result of executing a model-requested tool call."""

    type: Literal["function_call_output"]
    tool_call_id: str | None
    output: str


function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(
    tool_call: ResponseFunctionToolCall, verbose: bool = False
) -> ToolCallResult:
    func_name = tool_call.name
    func_args = json.loads(tool_call.arguments or "{}")

    if verbose:
        print(f"Calling function {func_name} with args {func_args}")
    else:
        print(f"Calling function {func_name}")

    func = function_map.get(func_name)
    if func is None:
        return ToolCallResult(
            type="function_call_output",
            tool_call_id=tool_call.id,
            output=f"Error: Unknown function {func_name}",
        )

    result = func(WORKING_DIRECTORY, **func_args)
    return ToolCallResult(
        type="function_call_output",
        tool_call_id=tool_call.id,
        output=result,
    )
