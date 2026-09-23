import argparse
import json
import os
from collections.abc import Iterable

from dotenv import load_dotenv
from openai.types.responses import ResponseInputParam, ToolParam

from prompts import system_prompt
from tools import (
    schema_get_file_content,
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file,
)

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if api_key is None:
    raise ValueError("OPENROUTER_API_KEY not set")

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(
    prog="iagent",
    description="A CLI tool for interacting with OpenRouter AI models",
    allow_abbrev=False,
)
parser.add_argument("user_prompt", type=str, help="The user prompt to send to the AI model")
parser.add_argument("--verbose", action="store_true", help="Print verbose output")
args = parser.parse_args()

context: ResponseInputParam = [{"role": "user", "content": args.user_prompt}]

tools: Iterable[ToolParam] = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]

response = client.responses.create(
    model="openrouter/free",
    instructions=system_prompt,
    input=context,
    tools=tools
)

for item in response.output:
    if item.type == "function_call":
        if item.name == "get_files_info":
            tool_args = json.loads(item.arguments)
            print(f"get_files_info: directory={tool_args.get('directory')}")
        elif item.name == "get_file_content":
            tool_args = json.loads(item.arguments)
            print(f"get_file_content: file_path={tool_args['file_path']}")
        elif item.name == "write_file":
            tool_args = json.loads(item.arguments)
            print(f"write_file: file_path={tool_args['file_path']}, content={tool_args['content']}")
        elif item.name == "run_python_file":
            tool_args = json.loads(item.arguments)
            if tool_args.get('args'):
                print(f"run_python_file: file_path={tool_args['file_path']}, args={tool_args['args']}")
            else:
                print(f"run_python_file: file_path={tool_args['file_path']}")
    elif item.type == "message":
        print(f"message: content={item.content}")

if args.verbose:
    print(f"User prompt: {args.user_prompt}\n")
    print(response.output_text)
    print(f"\nUsage:\nInput: {response.usage.input_tokens if response.usage else 0} tokens, Output: {response.usage.output_tokens if response.usage else 0} tokens")
else:
    print(response.output_text)
