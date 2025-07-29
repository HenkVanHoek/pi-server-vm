# scripts/create_master_vm.py
"""
A cross-platform script to create a master Debian VM template in VirtualBox.

This script automates the creation of a 'master' virtual machine. It will
dynamically find and download the latest stable Debian net-installer ISO,
create a new VM, and attach the necessary storage.
"""

# Standard library imports
import hashlib
import os
import platform
import re
import shutil
import sys

# Third-party imports
import requests

# Local application imports
from vm_manager import VMManager


# --- Configuration ---
# Dynamic ISO Configuration using Debian's permanent URL for the stable release
STABLE_RELEASE_URL = "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/"
ISO_DIR = "isos"

# VM Configuration
VM_NAME = "pi-master-template"
VM_DISK = f"{VM_NAME}.vdi"
VM_RAM_MB = 1024
VM_CPUS = 1


def setup_environment():
    """
    Finds the VBoxManage executable and adds its directory to the system PATH.
    This makes the script cross-platform.

    Returns:
        bool: True if VBoxManage is found, False otherwise.
    """
    # 1. Best case: Is VBoxManage already in the system's PATH?
    if shutil.which("VBoxManage"):
        print("VBoxManage found in system PATH.")
        return True

    # 2. Fallback: Check known default installation locations.
    system = platform.system()
    vbox_path = None
    if system == "Windows":
        # On Windows, the .exe is required for os.path.exists
        vbox_exe_name = "VBoxManage.exe"
        # Program Files is the most common location
        vbox_path = r"C:\Program Files\Oracle\VirtualBox"
    elif system in ("Linux", "Darwin"):  # Darwin is the system name for macOS
        vbox_exe_name = "VBoxManage"
        # On macOS and Linux, it's usually in a standard PATH directory like /usr/local/bin,
        # which shutil.which() should have already found. This is a fallback.
        vbox_path = "/usr/local/bin"
    else:
        vbox_exe_name = None

    if vbox_path and vbox_exe_name and os.path.exists(os.path.join(vbox_path, vbox_exe_name)):
        print(f"Found VirtualBox at: {vbox_path}")
        os.environ["PATH"] = f'{os.environ["PATH"]}{os.pathsep}{vbox_path}'
        return True

    # 3. Worst case: We could not find it.
    print("Error: Could not find VBoxManage executable.", file=sys.stderr)
    print("Please ensure VirtualBox is installed and its directory is in your system's PATH.", file=sys.stderr)
    return False


def get_latest_iso_info():
    """
    Finds the filename, URL, and checksum for the latest stable Debian netinst ISO.

    Raises:
        RuntimeError: If the ISO filename or checksum cannot be found.
        requests.exceptions.RequestException: If network requests fail.

    Returns:
        tuple[str, str, str] or tuple[None, None, None]: A tuple containing
        the ISO filename, the full download URL, and the expected SHA256 checksum,
        or None values on failure.
    """
    print(f"Checking for latest Debian release at: {STABLE_RELEASE_URL}")
    try:
        response = requests.get(STABLE_RELEASE_URL, timeout=30)
        response.raise_for_status()

        iso_match = re.search(r'href="(debian-[\d.]+-amd64-netinst\.iso)"', response.text)
        if not iso_match:
            raise RuntimeError("Could not find the netinst ISO filename on Debian page.")

        iso_filename = iso_match.group(1)
        iso_url = f"{STABLE_RELEASE_URL}{iso_filename}"

        checksum_url = f"{STABLE_RELEASE_URL}SHA256SUMS"
        checksum_response = requests.get(checksum_url, timeout=30)
        checksum_response.raise_for_status()

        checksum_pattern = f"^([a-f0-9]{{64}})\\s+{re.escape(iso_filename)}"
        checksum_match = re.search(checksum_pattern, checksum_response.text, re.MULTILINE)
        if not checksum_match:
            raise RuntimeError(f"Could not find checksum for {iso_filename}.")

        iso_sha256 = checksum_match.group(1)
        print(f"Found latest version: {iso_filename}")
        return iso_filename, iso_url, iso_sha256

    except (requests.exceptions.RequestException, RuntimeError) as e:
        print(f"Error finding latest ISO info: {e}", file=sys.stderr)
        return None, None, None


def verify_and_download_iso(iso_filename, iso_url, iso_sha256):
    """
    Verifies a local ISO's integrity or downloads it if missing/corrupt.

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
        with requests.get(iso_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            block_size = 8192
            downloaded_size = 0

            with open(iso_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=block_size):
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size > 0:
                        done = int(50 * downloaded_size / total_size)
                        progress = (
                            f"\r[{'=' * done}{' ' * (50 - done)}] "
                            f"{downloaded_size / (1024*1024):.2f}MB / "
                            f"{total_size / (1024*1024):.2f}MB"
                        )
                        print(progress, end='')

            print("\nDownload complete.")
        return verify_and_download_iso(iso_filename, iso_url, iso_sha256)

    except requests.exceptions.RequestException as e:
        print(f"\nError downloading file: {e}", file=sys.stderr)
        return None


def main():
    """Main execution function."""
    if not setup_environment():
        return 1

    manager = VMManager()

    if manager.vm_exists(VM_NAME):
        print(f"Error: VM '{VM_NAME}' already exists.", file=sys.stderr)
        print("Please remove it from the VirtualBox Manager before proceeding.", file=sys.stderr)
        return 1

    try:
        iso_info = get_latest_iso_info()
        if not all(iso_info):
            return 1

        iso_path = verify_and_download_iso(*iso_info)
        if not iso_path:
            return 1

    except (requests.exceptions.RequestException, RuntimeError) as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        return 1

    print(f"\nCreating and starting master VM: {VM_NAME}")
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
    print("\nYour master template is now ready!")
    print("You can now create clones using the cloning script:")
    print(f"    python scripts/clone_vm.py <your-new-clone-name>")

    return 0

if __name__ == "__main__":
    sys.exit(main())