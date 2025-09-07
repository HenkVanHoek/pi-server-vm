"""
This script downloads the latest release assets (OVA and installer) for a specified GitHub project.
By default, it downloads assets for HenkVanHoek/pi-server-vm.
"""

import os
import requests
import argparse

# --- Default Configuration ---
DEFAULT_OWNER = "HenkVanHoek"
DEFAULT_REPO = "pi-server-vm"
DOWNLOAD_DIR = "latest_release"
ASSET_EXTENSIONS = (".ova", ".exe")

# --- Script ---


def download_latest_release_assets(owner, repo):
    """
    Fetches the latest release from GitHub and downloads the specified assets.
    """
    print(f"Starting download process for {owner}/{repo}...")

    # 1. Create the download directory if it doesn't exist
    if not os.path.exists(DOWNLOAD_DIR):
        print(f"Creating download directory: {DOWNLOAD_DIR}")
        os.makedirs(DOWNLOAD_DIR)

    # 2. Get the latest release information from the GitHub API
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    print(f"Fetching latest release data from: {api_url}")

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching release data: {e}")
        return

    release_data = response.json()
    assets = release_data.get("assets", [])

    if not assets:
        print("No assets found in the latest release.")
        return

    print(f"Found {len(assets)} assets in release: {release_data.get('name')}")

    # 3. Filter and download the required assets
    for asset in assets:
        asset_name = asset.get("name", "")
        if asset_name.endswith(ASSET_EXTENSIONS):
            download_url = asset.get("browser_download_url")
            file_path = os.path.join(DOWNLOAD_DIR, asset_name)

            print(f"\nDownloading asset: {asset_name}")
            print(f"  -> From: {download_url}")
            print(f"  -> To:   {file_path}")

            try:
                with requests.get(download_url, stream=True) as r:
                    r.raise_for_status()
                    total_size = int(r.headers.get("content-length", 0))
                    downloaded_size = 0

                    with open(file_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            progress = (
                                (downloaded_size / total_size) * 100
                                if total_size > 0
                                else 0
                            )
                            print(
                                f"\r  -> Progress: {downloaded_size / (1024*1024):.2f} MB / {total_size / (1024*1024):.2f} MB ({progress:.1f}%)",
                                end="",
                            )
                print("\n  -> Download complete.")
            except requests.exceptions.RequestException as e:
                print(f"\nError downloading {asset_name}: {e}")
            except IOError as e:
                print(f"\nError writing file {file_path}: {e}")

    print("\n\nAll desired assets have been processed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download latest release assets from a GitHub repository."
    )
    parser.add_argument(
        "--owner",
        type=str,
        default=DEFAULT_OWNER,
        help=f"The owner of the repository (default: {DEFAULT_OWNER})",
    )
    parser.add_argument(
        "--repo",
        type=str,
        default=DEFAULT_REPO,
        help=f"The name of the repository (default: {DEFAULT_REPO})",
    )
    args = parser.parse_args()

    download_latest_release_assets(args.owner, args.repo)
