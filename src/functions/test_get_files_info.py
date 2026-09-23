import unittest

from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def test_get_files_info(self):
        # Test 1: Basic case - relative path
        result = get_files_info("calculator", ".")
        self.assertIn("Files for '.':", result)
        self.assertRegex(result, r"- main\.py: \d+ bytes \(file\)")
        self.assertRegex(result, r"- tests\.py: \d+ bytes \(file\)")
        self.assertRegex(result, r"- pkg: \d+ bytes \(directory\)")

        # Test 2: Absolute path - leading slash is treated as absolute path, fails subdirectory check
        result = get_files_info("calculator", "/bin")
        self.assertIn('Error', result)
        self.assertIn("not a valid subdirectory", result)

        # Test 3: Parent directory - ../ resolves to parent, which fails the subdirectory check
        result = get_files_info("calculator", "../")
        self.assertIn('Error', result)
        self.assertIn("not a valid subdirectory", result)

        # Test 4: Deep nested path - fails because src/main.py is a file, not a directory
        result = get_files_info("calculator", "src/main.py")
        self.assertIn('Error', result)
        self.assertIn("is not a valid directory", result)
