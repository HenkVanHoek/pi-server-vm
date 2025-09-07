# tests/test_downloader_script.py
import pytest
import requests
import os
from unittest.mock import patch, MagicMock, mock_open

import sys

sys.path.insert(0, ".")

from download_latest_release import download_latest_release_assets


@patch("requests.get")
@patch("os.path.exists")
@patch("os.makedirs")
@patch("builtins.open", new_callable=mock_open)
def test_download_happy_path(
    mock_open_file, mock_makedirs, mock_exists, mock_requests_get
):
    """Tests the ideal workflow where everything succeeds."""
    # Arrange
    # 1. Mock the GitHub API response
    mock_api_response = MagicMock()
    mock_api_response.json.return_value = {
        "name": "v1.2.3",
        "assets": [
            {
                "name": "pi-server-vm.ova",
                "browser_download_url": "http://example.com/pi.ova",
            },
            {
                "name": "setup.exe",
                "browser_download_url": "http://example.com/setup.exe",
            },
            {
                "name": "source.zip",
                "browser_download_url": "http://example.com/source.zip",
            },  # Should be ignored
        ],
    }
    mock_api_response.raise_for_status = MagicMock()

    # 2. Mock the asset download response
    mock_download_response = MagicMock()
    mock_download_response.raise_for_status = MagicMock()
    mock_download_response.iter_content.return_value = [b"chunk1", b"chunk2"]
    mock_download_response.headers = {"content-length": "16"}

    mock_requests_get.side_effect = [
        mock_api_response,
        mock_download_response,
        mock_download_response,
    ]
    mock_exists.return_value = False

    # Act
    download_latest_release_assets("TestOwner", "TestRepo")

    # Assert
    mock_exists.assert_called_once_with("latest_release")
    mock_makedirs.assert_called_once_with("latest_release")
    assert mock_requests_get.call_count == 3
    mock_requests_get.assert_any_call(
        "https://api.github.com/repos/TestOwner/TestRepo/releases/latest"
    )
    mock_requests_get.assert_any_call("http://example.com/pi.ova", stream=True)
    mock_requests_get.assert_any_call("http://example.com/setup.exe", stream=True)
    expected_ova_path = os.path.join("latest_release", "pi-server-vm.ova")
    expected_exe_path = os.path.join("latest_release", "setup.exe")
    mock_open_file.assert_any_call(expected_ova_path, "wb")
    mock_open_file.assert_any_call(expected_exe_path, "wb")


@patch("requests.get")
def test_download_api_fails(mock_requests_get, capsys):
    """Tests that the script handles a failure to connect to the GitHub API."""
    # Arrange
    mock_requests_get.side_effect = requests.exceptions.RequestException("API is down")

    # Act
    download_latest_release_assets("TestOwner", "TestRepo")

    # Assert
    captured = capsys.readouterr()
    assert "Error fetching release data: API is down" in captured.out


@patch("requests.get")
def test_download_no_assets_in_release(mock_requests_get, capsys):
    """Tests that the script handles a release with no downloadable assets."""
    # Arrange
    mock_api_response = MagicMock()
    mock_api_response.json.return_value = {"name": "v1.2.4", "assets": []}
    mock_api_response.raise_for_status = MagicMock()
    mock_requests_get.return_value = mock_api_response

    # Act
    download_latest_release_assets("TestOwner", "TestRepo")

    # Assert
    captured = capsys.readouterr()
    assert "No assets found in the latest release." in captured.out
