# tests/test_release_script.py
import pytest
import subprocess
from unittest.mock import patch, MagicMock

# We need to tell Python where to find the 'release' script.
# This assumes your 'tests' directory is at the same level as 'release.py'.
import sys

sys.path.insert(0, ".")

# Now we can import the functions we want to test
from release import is_git_clean, handle_deploy_docs

# --- Existing Tests (converted to pytest style) ---


@patch("release.subprocess.run")
def test_is_git_clean_returns_true_when_output_is_empty(mock_run):
    """
    Verifies that is_git_clean() returns True when the git status command
    produces no output (indicating a clean directory).
    """
    # Arrange
    mock_result = MagicMock()
    mock_result.stdout = ""
    mock_run.return_value = mock_result

    # Act
    result = is_git_clean()

    # Assert
    assert result is True
    mock_run.assert_called_once_with(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )


@patch("release.subprocess.run")
def test_is_git_clean_returns_false_when_output_is_not_empty(mock_run):
    """
    Verifies that is_git_clean() returns False when the git status command
    produces output (indicating a dirty directory).
    """
    # Arrange
    mock_result = MagicMock()
    mock_result.stdout = " M release.py"
    mock_run.return_value = mock_result

    # Act
    result = is_git_clean()

    # Assert
    assert result is False


# --- New Tests for Documentation Deployment ---


@patch("release.shutil.copytree")
@patch("release.subprocess.run")
@patch("release.os.path.isdir")
@patch("release.os.getenv")
@patch("release.load_dotenv")
def test_handle_deploy_docs_happy_path(
    mock_load_dotenv, mock_getenv, mock_isdir, mock_subprocess_run, mock_copytree
):
    """Tests the successful execution of the deploy_docs command."""
    # Arrange: Mock all external dependencies to simulate a perfect run.
    mock_getenv.return_value = "/fake/deploy/path"
    mock_isdir.return_value = True

    # Act: Run the function.
    handle_deploy_docs()

    # Assert: Verify that all the steps were called as expected.
    mock_load_dotenv.assert_called_once()
    mock_getenv.assert_called_once_with("DOCS_DEPLOY_PATH")
    mock_isdir.assert_called_once_with("/fake/deploy/path")

    mock_subprocess_run.assert_called_once_with(
        ["python", "-m", "mkdocs", "build", "--clean"], check=True, capture_output=True
    )
    mock_copytree.assert_called_once_with(
        "site/", "/fake/deploy/path", dirs_exist_ok=True
    )


@patch("release.load_dotenv")
@patch("release.os.getenv")
def test_handle_deploy_docs_no_env_variable(mock_getenv, mock_load_dotenv):
    """Tests that the script exits if the DOCS_DEPLOY_PATH variable is not set."""
    # Arrange: Mock getenv to return None, simulating a missing variable.
    mock_getenv.return_value = None

    # Act & Assert: Expect the function to call sys.exit(1).
    with pytest.raises(SystemExit) as e:
        handle_deploy_docs()
    assert e.type == SystemExit
    assert e.value.code == 1
    mock_load_dotenv.assert_called_once()


@patch("release.load_dotenv")
@patch("release.os.getenv")
@patch("release.os.path.isdir")
def test_handle_deploy_docs_invalid_deploy_path(
    mock_isdir, mock_getenv, mock_load_dotenv
):
    """Tests that the script exits if the DOCS_DEPLOY_PATH is not a valid directory."""
    # Arrange: Mock isdir to return False.
    mock_getenv.return_value = "/not/a/real/path"
    mock_isdir.return_value = False

    # Act & Assert: Expect the function to exit.
    with pytest.raises(SystemExit) as e:
        handle_deploy_docs()
    assert e.value.code == 1
    mock_isdir.assert_called_once_with("/not/a/real/path")


@patch("release.shutil.copytree")
@patch("release.subprocess.run")
@patch("release.os.path.isdir")
@patch("release.os.getenv")
@patch("release.load_dotenv")
def test_handle_deploy_docs_mkdocs_build_fails(
    mock_load_dotenv, mock_getenv, mock_isdir, mock_subprocess_run, mock_copytree
):
    """Tests that the script exits if the 'mkdocs build' command fails."""
    # Arrange: Configure the subprocess mock to raise an error.
    mock_getenv.return_value = "/fake/deploy/path"
    mock_isdir.return_value = True
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "cmd")

    # Act & Assert: Expect the function to exit.
    with pytest.raises(SystemExit) as e:
        handle_deploy_docs()
    assert e.value.code == 1
    # Ensure we didn't try to copy files after the build failed.
    mock_copytree.assert_not_called()
