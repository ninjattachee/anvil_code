from openai.types.responses import FunctionToolParam

schema_get_files_info: FunctionToolParam = {
    "type": "function",
    "name": "get_files_info",
    "description": "Get information about files in the repository",
    "parameters": {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "The directory to search for files (default is '.')"
            }
        },
    },
    "additionalProperties": False,
    "required": ["directory"]
}
