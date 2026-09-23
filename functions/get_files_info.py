import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    """
    Returns a list of files in the specified directory relative to the working directory.

    parameters:
        - working_directory: The working directory that scope the search to the repository root
        - directory: The directory to search for files (default is '.')
    """

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath([target_dir, working_dir_abs]) == working_dir_abs
        if not valid_target_dir:
            return f"Error: '{directory}' is not a valid subdirectory of {working_directory}"

        # Check if directory argument is actually a directory
        if not os.path.isdir(target_dir):
            return f"Error: '{directory}' is not a valid directory"

        result = []

        files = os.listdir(target_dir)
        for file in files:
            file_path = os.path.join(target_dir, file)
            size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            result.append(f"{file}: {size} bytes ({'directory' if is_dir else 'file'})")
        return f"Files for '{directory}':\n- {'\n- '.join(result)}"
    except PermissionError as e:
        return f'Error: Permission denied - {e!s}'
    except OSError as e:
        return f'Error: OS error - {e!s}'
    except ValueError as e:
        return f'Error: Invalid value - {e!s}'

if __name__ == "__main__":
    result = get_files_info("calculator", ".")
    print(result)
    result = get_files_info("calculator", "pkg")
    print(result)
    result = get_files_info("calculator", "..")
    print(result)
