from openai.types.responses import FunctionToolParam

schema_get_files_info: FunctionToolParam = {
    "type": "function",
    "name": "get_files_info",
    "description": "Get information about files in the repository",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "The directory to search for files (default is '.')"
            }
        },
        "additionalProperties": False,
        "required": ["directory"],
    },
}

schema_get_file_content: FunctionToolParam = {
    "type": "function",
    "name": "get_file_content",
    "description": "Get the content of a file",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file"
            }
        },
        "additionalProperties": False,
        "required": ["file_path"],
    },
}

schema_write_file: FunctionToolParam = {
    "type": "function",
    "name": "write_file",
    "description": "Write content to a file",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file"
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file"
            }
        },
        "additionalProperties": False,
        "required": ["file_path", "content"],
    },
}

schema_run_python_file: FunctionToolParam = {
    "type": "function",
    "name": "run_python_file",
    "description": "Run a Python file",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the Python file"
            },
            "args": {
                "type": "array",
                "description": "The arguments to pass to the Python file",
                "items": {
                    "type": "string"
                }
            }

        },
        "additionalProperties": False,
        "required": ["file_path"],
    },
}
