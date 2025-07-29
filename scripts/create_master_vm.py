# create_master_vm.py
"""
A script to create a master Debian VM template in VirtualBox.

This script automates the creation of a 'master' virtual machine. It will
dynamically find and download the latest stable Debian net-installer ISO,
create a new VM, and attach the necessary storage.
"""

# Standard library imports
import hashlib
import os
import re
import sys

# Third-party imports
import requests

# Local application imports
from vm_manager import VMManager


# --- Configuration ---
# Set path to your VirtualBox installation directory
VBOX_PATH = r"C:\Program Files\Oracle\VirtualBox"

# Dynamic ISO Configuration using Debian's permanent URL for the stable release
STABLE_RELEASE_URL = "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/"
ISO_DIR = "isos"

# VM Configuration
VM_NAME = "pi-master-template"
VM_DISK = f"{VM_NAME}.vdi"
VM_RAM_MB = 1024
VM_CPUS = 1


def get_latest_iso_info():
    """
    Find the filename and checksum for the latest stable Debian netinst ISO.

    This function scrapes the official Debian stable release page to find the
    direct download link for the net-installer ISO and its corresponding
    SHA256 checksum.

    Raises:
        RuntimeError: If the ISO filename or checksum cannot be found.
        requests.exceptions.RequestException: If network requests fail.

    Returns:
        tuple[str, str, str]: A tuple containing the ISO filename, the full
        download URL, and the expected SHA256 checksum.
    """
    print(f"Checking for latest Debian release at: {STABLE_RELEASE_URL}")

    # Get the directory listing page for the latest release
    response = requests.get(STABLE_RELEASE_URL, timeout=30)
    response.raise_for_status()

    # Regex to find the netinst ISO filename, e.g., "debian-12.5.0-amd64-netinst.iso"
    iso_match = re.search(r'href="(debian-[\d.]+-amd64-netinst\.iso)"', response.text)
    if not iso_match:
        raise RuntimeError("Could not find the netinst ISO filename on Debian page.")

    iso_filename = iso_match.group(1)
    iso_url = f"{STABLE_RELEASE_URL}{iso_filename}"

    # Now find and download the checksums file
    checksum_url = f"{STABLE_RELEASE_URL}SHA256SUMS"
    checksum_response = requests.get(checksum_url, timeout=30)
    checksum_response.raise_for_status()

    # Find the checksum for our specific ISO file from the SHA256SUMS content.
    # The `re.escape` is crucial to safely handle dots in the filename.
    checksum_pattern = f"^([a-f0-9]{{64}})\\s+{re.escape(iso_filename)}"
    checksum_match = re.search(checksum_pattern, checksum_response.text, re.MULTILINE)
    if not checksum_match:
        raise RuntimeError(f"Could not find checksum for {iso_filename}.")

    iso_sha256 = checksum_match.group(1)

    print(f"Found latest version: {iso_filename}")
    print(f"Expected SHA256: {iso_sha256[:10]}...")  # Print a snippet

    return iso_filename, iso_url, iso_sha256


def verify_and_download_iso(iso_filename, iso_url, iso_sha256):
    """
    Verify a local ISO's integrity or download it if missing/corrupt.

    Args:
        iso_filename (str): The name of the ISO file.
        iso_url (str): The URL to download the ISO from.
        iso_sha256 (str): The expected SHA256 checksum.

    Returns:
        str or None: The full path to the valid ISO file, or None on failure.
    """
    iso_path = os.path.join(ISO_DIR, iso_filename)
    os.makedirs(ISO_DIR, exist_ok=True)

    if os.path.exists(iso_path):
        print("Verifying checksum of existing ISO...")
        sha256_hash = hashlib.sha256()
        with open(iso_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        if sha256_hash.hexdigest() == iso_sha256:
            print("Checksum OK. ISO is ready.")
            return iso_path

        print("Checksum mismatch. Deleting corrupted file and re-downloading.")
        os.remove(iso_path)

    print(f"Downloading {iso_filename}...")
    try:
        with requests.get(iso_url, stream=True, timeout=30) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0)) # Now used
            block_size = 8192
            downloaded_size = 0

            with open(iso_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=block_size):
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    # --- Progress bar logic restored ---
                    if total_size > 0:
                        done = int(50 * downloaded_size / total_size)
                        progress = (
                            f"\r[{'=' * done}{' ' * (50 - done)}] "
                            f"{downloaded_size / (1024*1024):.2f}MB / "
                            f"{total_size / (1024*1024):.2f}MB"
                        )
                        print(progress, end='')

            print("\nDownload complete.")
        # After download, verify the new file.
        return verify_and_download_iso(iso_filename, iso_url, iso_sha256)

    except requests.exceptions.RequestException as e:
        print(f"\nError downloading file: {e}", file=sys.stderr)
        return None


def main():
    """Main execution function."""
    # Add VirtualBox to the system's PATH environment variable
    os.environ["PATH"] = f'{os.environ["PATH"]}{os.pathsep}{VBOX_PATH}'
    manager = VMManager()

    if manager.vm_exists(VM_NAME):
        print(
            f"Error: VM '{VM_NAME}' already exists. "
            "Please remove it from VirtualBox first.",
            file=sys.stderr
        )
        return 1

    try:
        iso_info = get_latest_iso_info()
        if not all(iso_info):
            return 1

        iso_path = verify_and_download_iso(*iso_info)
        if not iso_path:
            return 1

    except (requests.exceptions.RequestException, RuntimeError) as e:
        print(f"\nAn error occurred: {e}", file=sys.stderr)
        return 1

    print(f"\nCreating and starting master VM: {VM_NAME}") # Modified text
    manager.create_vm(
        name=VM_NAME,
        ram=VM_RAM_MB,
        cpus=VM_CPUS,
        disk=VM_DISK,
        iso=iso_path,
        bridge=True
    )

    # --- UPDATED FINAL INSTRUCTIONS ---
    print("\nVM has been started in a new window.")
    print("Please complete the Debian installation manually now.")
    print("\nRemember to select the 'SSH server' and deselect any desktop environments.")
    print("After setup, the installer will shut down the VM.")
    print("You can then create a clean snapshot for cloning.")
    return 0


if __name__ == "__main__":
    sys.exit(main())