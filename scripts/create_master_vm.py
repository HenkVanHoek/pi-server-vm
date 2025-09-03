# scripts/create_master_vm.py (Final, Audited Version)
"""
A cross-platform script to create a master Debian VM template in VirtualBox.
This script creates a VM with a single, discoverable Bridged Network Adapter.
"""
import hashlib
import os
import re
import sys
import requests
from scripts import vm_manager

# --- Configuration (remains the same) ---
ISO_DIR = "isos"
VM_NAME = "pi-master-template"
VM_DISK = f"{VM_NAME}.vdi"
VM_RAM_MB = 1024
VM_CPUS = 1
STABLE_RELEASE_URL = "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/"


def get_latest_iso_info():
    # ... (this function is complete and correct)
    print(f"Checking for latest Debian release at: {STABLE_RELEASE_URL}")
    try:
        response = requests.get(STABLE_RELEASE_URL, timeout=30)
        response.raise_for_status()
        iso_match = re.search(
            r'href="(debian-[\d.]+-amd64-netinst\.iso)"', response.text
        )
        if not iso_match:
            raise RuntimeError(
                "Could not find the netinst ISO filename on Debian page."
            )
        iso_filename = iso_match.group(1)
        iso_url = f"{STABLE_RELEASE_URL}{iso_filename}"
        checksum_url = f"{STABLE_RELEASE_URL}SHA256SUMS"
        checksum_response = requests.get(checksum_url, timeout=30)
        checksum_response.raise_for_status()
        checksum_pattern = f"^([a-f0-9]{{64}})\\s+{re.escape(iso_filename)}"
        checksum_match = re.search(
            checksum_pattern, checksum_response.text, re.MULTILINE
        )
        if not checksum_match:
            raise RuntimeError(f"Could not find checksum for {iso_filename}.")
        iso_sha256 = checksum_match.group(1)
        print(f"Found latest version: {iso_filename}")
        return iso_filename, iso_url, iso_sha256
    except (requests.exceptions.RequestException, RuntimeError) as e:
        print(f"Error finding latest ISO info: {e}", file=sys.stderr)
        return None, None, None


def verify_and_download_iso(iso_filename, iso_url, iso_sha256):
    # ... (this function is complete and correct)
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
            total_size = int(r.headers.get("content-length", 0))
            block_size = 8192
            downloaded_size = 0
            with open(iso_path, "wb") as f:
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
                        print(progress, end="")
            print("\nDownload complete.")
        return verify_and_download_iso(iso_filename, iso_url, iso_sha256)
    except requests.exceptions.RequestException as e:
        print(f"\nError downloading file: {e}", file=sys.stderr)
        return None


def main():
    """Main execution function."""
    if not vm_manager.setup_environment():
        return 1

    if vm_manager.vm_exists(VM_NAME):
        print(f"Error: VM '{VM_NAME}' already exists.", file=sys.stderr)
        print(
            "Please remove it from the VirtualBox Manager before proceeding.",
            file=sys.stderr,
        )
        return 1

    try:
        iso_info = get_latest_iso_info()
        if not all(iso_info):
            return 1
        iso_path = verify_and_download_iso(*iso_info)
        if not iso_path:
            return 1
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        return 1

    print(f"\nCreating and starting master VM: {VM_NAME}")
    vm_manager.create_vm(
        name=VM_NAME, ram=VM_RAM_MB, cpus=VM_CPUS, disk=VM_DISK, iso=iso_path
    )

    # --- START OF FINAL, AUDITED INSTRUCTIONS ---
    print("\n--- MANUAL SETUP REQUIRED ---")
    print("\nVM has been started. Please complete the manual Debian installation now.")
    print(
        "IMPORTANT: During setup, select the 'SSH server' and deselect any desktop environments."
    )
    print("After setup, the installer will shut down the VM.")

    print("\n--- FINAL STEP: Configure Master Template ---")
    print("After the installation is complete, you must start the VM again, log in,")
    print("and run the following complete block of commands to finalize the template.")
    print(
        "This will install all necessary services and the first-boot provisioning script."
    )

    print("\n--- Copy and paste the entire block below into the VM terminal ---")
    print("-----------------------------------------------------------------")
    print(
        """
# Update package list and install required tools
sudo apt-get update
sudo apt-get install -y virtualbox-guest-utils avahi-daemon

# Create script to show IP address on login
sudo tee /etc/profile.d/show-ip.sh > /dev/null << EOF
#!/bin/sh
echo "================================================================"
echo "Welcome to your Pi-Server-VM!"
echo "IP Address: \$(hostname -I)"
echo "Hostname:   \$(hostname).local"
echo "================================================================"
EOF

# Create the first-boot identity writer script
sudo tee /usr/local/bin/pivm-info-writer.sh > /dev/null << EOF
#!/bin/bash
PROPERTY_NAME="/VirtualBox/GuestAdd/PiSelfhostingInfo"
OUTPUT_FILE="/etc/piselfhosting-virtual-pi-server"
CONTENT=\\$(VBoxControl guestproperty get "\$PROPERTY_NAME" | sed 's/Value: //')
if [ -n "\$CONTENT" ]; then
    echo "Writing PiSelfhosting identity file to \$OUTPUT_FILE..."
    echo "\$CONTENT" > "\$OUTPUT_FILE"
    chmod 644 "\$OUTPUT_FILE"
fi
systemctl disable pivm-info.service
EOF

# Create the systemd service file for the identity writer
sudo tee /etc/systemd/system/pivm-info.service > /dev/null << EOF
[Unit]
Description=Pi-Server-VM First Boot Identity Writer
After=vboxadd-service.service
[Service]
Type=oneshot
ExecStart=/usr/local/bin/pivm-info-writer.sh
[Install]
WantedBy=multi-user.target
EOF

# Make the script executable and enable the service
sudo chmod +x /usr/local/bin/pivm-info-writer.sh
sudo systemctl enable pivm-info.service

# Final cleanup and shutdown
echo "Template configuration complete. Shutting down."
sudo shutdown now
"""
    )
    print("-----------------------------------------------------------------")
    print("\nYour master template is now complete and ready for cloning!")
    # --- END OF FINAL, AUDITED INSTRUCTIONS ---
    return 0


if __name__ == "__main__":
    sys.exit(main())
