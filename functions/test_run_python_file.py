import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).with_name("run_python_file.py")
SPEC = importlib.util.spec_from_file_location("run_python_file_module", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
run_python_file_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(run_python_file_module)
run_python_file = run_python_file_module.run_python_file


class TestRunPythonFile(unittest.TestCase):
    def test_rejects_non_python_file(self):
        with tempfile.TemporaryDirectory() as working_directory:
            file_path = Path(working_directory, "script.txt")
            file_path.write_text("not Python")

            result = run_python_file(working_directory, "script.txt")

        self.assertEqual(result, "Error: script.txt is not a Python file")

    def test_rejects_file_outside_working_directory(self):
        with tempfile.TemporaryDirectory() as working_directory, tempfile.TemporaryDirectory() as other_directory:
            file_path = Path(other_directory, "script.py")
            file_path.write_text("print('outside')")

            result = run_python_file(working_directory, str(file_path))

        self.assertEqual(
            result,
            f"Error: Cannot access file {file_path} outside of the working directory",
        )

    def test_rejects_missing_file(self):
        with tempfile.TemporaryDirectory() as working_directory:
            result = run_python_file(working_directory, "missing.py")

        self.assertEqual(result, "Error: missing.py does not exist or is not a file")

    @patch.object(run_python_file_module.subprocess, "run")
    def test_returns_process_output(self, mock_run):
        mock_run.return_value = run_python_file_module.subprocess.CompletedProcess(
            args=[], returncode=0, stdout="hello\n", stderr="warning\n"
        )
        with tempfile.TemporaryDirectory() as working_directory:
            Path(working_directory, "script.py").write_text("print('hello')")

            result = run_python_file(working_directory, "script.py", ["--name", "Ada"])

        self.assertEqual(result, "STDOUT: hello\n\nSTDERR: warning\n")
        mock_run.assert_called_once_with(
            ["uv", "run", str(Path(working_directory, "script.py")), "--name", "Ada"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    @patch.object(run_python_file_module.subprocess, "run")
    def test_returns_nonzero_process_error(self, mock_run):
        mock_run.return_value = run_python_file_module.subprocess.CompletedProcess(
            args=[], returncode=1, stdout="", stderr="failure\n"
        )
        with tempfile.TemporaryDirectory() as working_directory:
            Path(working_directory, "script.py").touch()

            result = run_python_file(working_directory, "script.py")

        self.assertEqual(result, "Process exited with code 1\nError: failure\n")

    @patch.object(run_python_file_module.subprocess, "run")
    def test_returns_no_output_for_silent_process(self, mock_run):
        mock_run.return_value = run_python_file_module.subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )
        with tempfile.TemporaryDirectory() as working_directory:
            Path(working_directory, "script.py").touch()

            result = run_python_file(working_directory, "script.py")

        self.assertEqual(result, "No output")

    @patch.object(run_python_file_module.subprocess, "run")
    def test_handles_process_timeout(self, mock_run):
        mock_run.side_effect = run_python_file_module.subprocess.TimeoutExpired("uv", 30)
        with tempfile.TemporaryDirectory() as working_directory:
            Path(working_directory, "script.py").touch()

            result = run_python_file(working_directory, "script.py")

        self.assertEqual(result, "Error: Process timed out after 30 seconds")

    @patch.object(run_python_file_module.subprocess, "run")
    def test_handles_missing_uv_executable(self, mock_run):
        mock_run.side_effect = FileNotFoundError
        with tempfile.TemporaryDirectory() as working_directory:
            Path(working_directory, "script.py").touch()

            result = run_python_file(working_directory, "script.py")

        self.assertEqual(result, "Error: Unable to run Python file because uv was not found")

    @patch.object(run_python_file_module.subprocess, "run")
    def test_handles_permission_error(self, mock_run):
        mock_run.side_effect = PermissionError
        with tempfile.TemporaryDirectory() as working_directory:
            Path(working_directory, "script.py").touch()

            result = run_python_file(working_directory, "script.py")

        self.assertEqual(result, "Error: Permission denied while running Python file")


if __name__ == "__main__":
    unittest.main()
