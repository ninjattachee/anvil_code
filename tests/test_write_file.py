import importlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

write_file_module = importlib.import_module("anvil_code.functions.write_file")
write_file = write_file_module.write_file


class TestWriteFile(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.working_directory = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_writes_file_content(self):
        result = write_file(self.working_directory, "notes.txt", "Hello, world!")

        self.assertEqual(result, 'Successfully wrote to "notes.txt" (13 characters)')
        self.assertEqual(Path(self.working_directory, "notes.txt").read_text(), "Hello, world!")

    def test_creates_parent_directories(self):
        result = write_file(self.working_directory, "nested/notes.txt", "content")

        self.assertEqual(result, 'Successfully wrote to "nested/notes.txt" (7 characters)')
        self.assertEqual(Path(self.working_directory, "nested/notes.txt").read_text(), "content")

    def test_rejects_path_outside_working_directory(self):
        result = write_file(self.working_directory, "../outside.txt", "private")

        self.assertEqual(
            result,
            'Error: Cannot write to "../outside.txt" as it is outside the working directory',
        )

    def test_rejects_directory_target(self):
        Path(self.working_directory, "nested").mkdir()

        result = write_file(self.working_directory, "nested", "content")

        self.assertEqual(result, 'Error: Cannot write to "nested" as it is a directory')

    def test_returns_os_error(self):
        with patch("builtins.open", side_effect=OSError("disk full")):
            result = write_file(self.working_directory, "notes.txt", "content")

        self.assertEqual(result, 'Error: Unable to write "notes.txt": disk full')

    def test_returns_value_error(self):
        with patch.object(write_file_module.os.path, "commonpath", side_effect=ValueError("invalid path")):
            result = write_file(self.working_directory, "notes.txt", "content")

        self.assertEqual(result, 'Error: Unable to write "notes.txt": invalid path')

    def test_returns_type_error(self):
        with patch.object(write_file_module.os.path, "abspath", side_effect=TypeError("invalid path type")):
            result = write_file(self.working_directory, "notes.txt", "content")

        self.assertEqual(result, 'Error: Unable to write "notes.txt": invalid path type')


if __name__ == "__main__":
    unittest.main()
