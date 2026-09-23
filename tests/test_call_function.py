import unittest
from types import SimpleNamespace
from typing import cast
from unittest.mock import patch

from openai.types.responses import ResponseFunctionToolCall

from anvil_code.call_function import ToolCallResult, call_function


class TestCallFunction(unittest.TestCase):
    def test_returns_structured_result_for_known_function(self):
        tool_call = SimpleNamespace(
            name="get_files_info", arguments='{"directory": "."}', id="call_123"
        )

        with patch("anvil_code.call_function.function_map", {"get_files_info": lambda *_args, **_kwargs: "files"}):
            result = call_function(cast(ResponseFunctionToolCall, tool_call))

        self.assertEqual(
            result,
            ToolCallResult(type="function_call_output", tool_call_id="call_123", output="files"),
        )

    def test_returns_structured_result_for_unknown_function(self):
        tool_call = SimpleNamespace(name="missing", arguments="{}", id="call_456")

        result = call_function(cast(ResponseFunctionToolCall, tool_call))

        self.assertEqual(
            result,
            ToolCallResult(
                type="function_call_output",
                tool_call_id="call_456",
                output="Error: Unknown function missing",
            ),
        )


if __name__ == "__main__":
    unittest.main()
