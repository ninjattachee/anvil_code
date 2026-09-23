import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.realpath(working_directory)
        target_path = os.path.realpath(os.path.join(working_dir_abs, file_path))

        validate_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if not validate_target_path:
            return f'Error: Cannot read "{target_path}" as it is outside the working directory {working_dir_abs}'
        if not os.path.exists(target_path):
            return f'Error: Cannot read "{target_path}" as it does not exist'
        if not os.path.isfile(target_path):
            return f'Error: Cannot read "{target_path}" as it is not a file'

        with open(target_path, 'r') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{target_path}" truncated at {MAX_CHARS} characters]'
            return content
    except PermissionError as e:
        return f'Error: Permission denied - {e!s}'
    except OSError as e:
        return f'Error: OS error - {e!s}'
    except ValueError as e:
        return f'Error: Invalid value - {e!s}'


if __name__ == "__main__":
    result = get_file_content("calculator", "main.py")
    print(result)
    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)
    result = get_file_content("calculator", "/bin/cat")
    print(result)
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result)
