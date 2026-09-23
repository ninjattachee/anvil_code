import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

        valid_path = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
        if not valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the working directory'
        if os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)
        with open(file_path_abs, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters)'
    except (OSError, TypeError, ValueError) as error:
        return f'Error: Unable to write "{file_path}": {error}'

if __name__ == '__main__':
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)
