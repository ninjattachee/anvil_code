import argparse
import os
from collections.abc import Iterable
from dataclasses import dataclass

from dotenv import load_dotenv
from openai.types.responses import ResponseInputParam, ToolParam

from call_function import call_function
from config import MAX_ITERATIONS
from prompts import system_prompt
from tools import (
    schema_get_file_content,
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file,
)

load_dotenv()

def create_client():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key is None:
        raise ValueError("OPENROUTER_API_KEY not set")

    from openai import OpenAI

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


client = create_client()


@dataclass
class ParsedArgs:
    user_prompt: str
    verbose: bool


def parse_args() -> ParsedArgs:
    parser = argparse.ArgumentParser(
        prog="iagent",
        description="A CLI tool for interacting with OpenRouter AI models",
        allow_abbrev=False,
    )
    parser.add_argument("user_prompt", type=str, help="The user prompt to send to the AI model")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")
    parsed_args = parser.parse_args()
    return ParsedArgs(
        user_prompt=parsed_args.user_prompt,
        verbose=parsed_args.verbose,
    )


args = parse_args()

context: ResponseInputParam = [{"role": "user", "content": args.user_prompt}]

tools: Iterable[ToolParam] = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]


def create_response(input_context: ResponseInputParam):
    return client.responses.create(
        model="openrouter/free",
        instructions=system_prompt,
        input=input_context,
        tools=tools,
    )

def print_response(response, user_prompt: str, verbose: bool) -> None:
    print("\n--------Final Result--------\n")
    if verbose:
        print(f"User prompt: {user_prompt}\n")
        print(response.output_text)
        print(f"\nUsage:\nInput: {response.usage.input_tokens if response.usage else 0} tokens, Output: {response.usage.output_tokens if response.usage else 0} tokens")
    else:
        print(response.output_text)

def process_response_output(response) -> bool:
    types = [item.type for item in response.output]
    if not "function_call" in types:
        print_response(response, user_prompt=args.user_prompt, verbose=args.verbose)
        return True

    for item in response.output:
        if item.type == "function_call":
            function_call_result = call_function(item)
            print(f"-> {function_call_result.output}")
        elif item.type == "message":
            print(f"message: content={item.content}")
    return False

def update_context(response) -> None:
    for item in response.output:
        if item.type == "function_call":
            function_call_output = call_function(item)
            context.append({"role": "assistant", "content": function_call_output.output})
        elif item.type == "message":
            context.append({"role": "assistant", "content": item.content})


def agent_loop() -> None:
    done = False
    for _ in range(MAX_ITERATIONS):
        response = create_response(context)
        done = process_response_output(response)
        if done:
            return
        update_context(response)

    print("Failed to get a valid response after maximum iterations.")
    raise SystemExit(1)


if __name__ == "__main__":
    agent_loop()
