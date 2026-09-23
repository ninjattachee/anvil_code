import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).with_name("get_file_content.py")
SPEC = importlib.util.spec_from_file_location("get_file_content_module", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
get_file_content_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(get_file_content_module)
get_file_content = get_file_content_module.get_file_content


class TestGetFileContent(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.working_directory = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_reads_file_content(self):
        file_path = Path(self.working_directory, "notes.txt")
        file_path.write_text("Hello, world!")

        result = get_file_content(self.working_directory, "notes.txt")

        self.assertEqual(result, "Hello, world!")

    def test_rejects_path_outside_working_directory(self):
        outside_file = Path(self.working_directory).parent / "outside.txt"
        outside_file.write_text("private")
        self.addCleanup(outside_file.unlink)

        result = get_file_content(self.working_directory, "../outside.txt")

        expected_path = os.path.realpath(outside_file)
        expected_directory = os.path.realpath(self.working_directory)
        self.assertEqual(
            result,
            f'Error: Cannot read "{expected_path}" as it is outside the working directory {expected_directory}',
        )

    def test_reports_missing_file(self):
        missing_file = Path(self.working_directory, "missing.txt")

        result = get_file_content(self.working_directory, "missing.txt")

        self.assertEqual(result, f'Error: Cannot read "{missing_file}" as it does not exist')

    def test_rejects_directory(self):
        directory = Path(self.working_directory, "nested")
        directory.mkdir()

        result = get_file_content(self.working_directory, "nested")

        self.assertEqual(result, f'Error: Cannot read "{directory}" as it is not a file')

    def test_truncates_content_larger_than_maximum(self):
        file_path = Path(self.working_directory, "large.txt")
        file_path.write_text("abcdef")

        with patch.object(get_file_content_module, "MAX_CHARS", 5):
            result = get_file_content(self.working_directory, "large.txt")

        self.assertEqual(
            result,
            f'abcde[...File "{file_path}" truncated at 5 characters]',
        )

    def test_returns_permission_error(self):
        file_path = Path(self.working_directory, "private.txt")
        file_path.write_text("private")

        with patch("builtins.open", side_effect=PermissionError("access denied")):
            result = get_file_content(self.working_directory, "private.txt")

        self.assertEqual(result, "Error: Permission denied - access denied")

    def test_returns_os_error(self):
        with patch.object(get_file_content_module.os.path, "exists", side_effect=OSError("I/O failure")):
            result = get_file_content(self.working_directory, "file.txt")

        self.assertEqual(result, "Error: OS error - I/O failure")

    def test_returns_value_error(self):
        with patch.object(get_file_content_module.os.path, "commonpath", side_effect=ValueError("invalid path")):
            result = get_file_content(self.working_directory, "file.txt")

        self.assertEqual(result, "Error: Invalid value - invalid path")


if __name__ == "__main__":
    unittest.main()
