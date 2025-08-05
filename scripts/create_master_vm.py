# scripts/create_master_vm.py
"""
A script to create the master Debian VM template.

This script automates the creation of 'pi-master-template' using the correct
network configuration and hardware settings.
"""

import argparse
import shlex
import subprocess
import sys
from scripts import vm_manager

# --- Configuration ---
MASTER_VM_NAME = "pi-master-template"
DEFAULT_RAM = "2048"
DEFAULT_CPUS = "2"
DEFAULT_DISK = "8000"


def parse_arguments():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Create the master 'pi-master-template' VM for cloning."
    )
    parser.add_argument(
        "iso_path", help="The absolute path to the Debian netinstall ISO file."
    )
    return parser.parse_args()


def main():
    """Main execution function."""
    if not vm_manager.setup_environment():
        return 1

    args = parse_arguments()

    if vm_manager.vm_exists(MASTER_VM_NAME):
        print(
            f"Error: The master VM '{MASTER_VM_NAME}' already exists.", file=sys.stderr
        )
        return 1

    print(f"Creating master VM '{MASTER_VM_NAME}'...")
    try:
        disk_path = f"{MASTER_VM_NAME}.vdi"
        vm_manager.create_vm(
            name=MASTER_VM_NAME,
            ram=DEFAULT_RAM,
            cpus=DEFAULT_CPUS,
            disk=disk_path,
            iso=args.iso_path,
        )
        print("\nMaster VM creation started.")
        print("The Debian installer will now run in the new VM window.")
        print("Please complete the installation manually.")
        return 0

    except (subprocess.CalledProcessError, RuntimeError) as e:
        print("\n--- ERROR ---", file=sys.stderr)
        if isinstance(e, subprocess.CalledProcessError):
            # The 'e.cmd' attribute is only available on CalledProcessError
            cmd_string = shlex.join(e.cmd) if hasattr(e, "cmd") else "N/A"
            print(
                f"An error occurred while running a VBoxManage command: {cmd_string}",
                file=sys.stderr,
            )
            print(f"Error output:\n{e.stderr}", file=sys.stderr)
        else:
            print(f"A runtime error occurred: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
