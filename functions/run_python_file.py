import os
import subprocess


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        if not file_path.endswith(".py"):
            return f"Error: {file_path} is not a Python file"

        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

        valid_path = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
        if not valid_path:
            return f'Error: Cannot access file {file_path} outside of the working directory'

        is_file = os.path.isfile(file_path_abs)
        if not is_file:
            return f'Error: {file_path} does not exist or is not a file'

        command = ["uv", "run", file_path_abs]
        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
        if result.returncode != 0:
            return f'Process exited with code {result.returncode}\nError: {result.stderr}'
        if not result.stdout and not result.stderr:
            return 'No output'
        return f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}'
    except subprocess.TimeoutExpired:
        return 'Error: Process timed out after 30 seconds'
    except FileNotFoundError:
        return 'Error: Unable to run Python file because uv was not found'
    except PermissionError:
        return 'Error: Permission denied while running Python file'
