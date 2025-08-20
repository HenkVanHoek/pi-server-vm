# tests/test_release_script.py
import unittest
from unittest.mock import patch, MagicMock

# We need to tell Python where to find the 'release' script.
# This assumes your 'tests' directory is at the same level as 'release.py'.
import sys

sys.path.insert(0, "..")

# Now we can import the function we want to test
from release import is_git_clean


class TestGitChecks(unittest.TestCase):

    @patch("release.subprocess.run")
    def test_is_git_clean_returns_true_when_output_is_empty(self, mock_run):
        """
        Verifies that is_git_clean() returns True when the git status command
        produces no output (indicating a clean directory).
        """
        # Arrange: Configure our "fake" subprocess.run to return a result
        # with empty stdout, simulating a clean git status.
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_run.return_value = mock_result

        # Act: Call the function we are testing.
        result = is_git_clean()

        # Assert: Check that the function behaved as expected.
        self.assertTrue(result)
        mock_run.assert_called_once_with(
            ["git", "status", "--porcelain"], capture_output=True, text=True
        )

    @patch("release.subprocess.run")
    def test_is_git_clean_returns_false_when_output_is_not_empty(self, mock_run):
        """
        Verifies that is_git_clean() returns False when the git status command
        produces output (indicating a dirty directory).
        """
        # Arrange: Configure our "fake" subprocess to return a result
        # with some text in stdout, simulating a dirty git status.
        mock_result = MagicMock()
        mock_result.stdout = " M release.py"
        mock_run.return_value = mock_result

        # Act: Call the function.
        result = is_git_clean()

        # Assert: Check that the function returned the correct boolean.
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
