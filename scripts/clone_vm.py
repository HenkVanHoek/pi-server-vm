# scripts/clone_vm.py
"""
A cross-platform script to clone the master Debian VM template.

This script creates a new, configurable VM by cloning 'pi-master-template'.
It supports command-line arguments to customize RAM, CPUs, and add a
secondary disk, making it a flexible provisioning tool.
"""

import argparse
import subprocess
import sys
from scripts import vm_manager

# --- Configuration ---
SOURCE_VM_NAME = "pi-master-template"


def parse_arguments():
    """
    Parses command-line arguments using argparse. This function is isolated
    so it can be easily unit-tested.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Clone the master Pi VM template with custom hardware settings.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("name", help="The name for the new cloned virtual machine.")
    parser.add_argument(
        "--ram",
        type=int,
        help="Amount of RAM in megabytes for the new VM (e.g., 2048 for 2GB).\nDefaults to the setting from the master template (1024MB).",
    )
    parser.add_argument(
        "--cpus",
        type=int,
        help="Number of CPU cores for the new VM (e.g., 2 or 4).\nDefaults to the setting from the master template (1 CPU).",
    )
    parser.add_argument(
        "--disk-size",
        type=int,
        help="Size in gigabytes for a new, secondary virtual disk (e.g., 32 for 32GB).\nIf omitted, no secondary disk is created.",
    )
    return parser.parse_args()


def main():
    """Main execution function."""
    if not vm_manager.setup_environment():
        return 1

    # We now call our dedicated, testable parsing function.
    args = parse_arguments()

    # --- Pre-flight Checks ---
    if not vm_manager.vm_exists(SOURCE_VM_NAME):
        print(
            f"Error: The source VM '{SOURCE_VM_NAME}' does not exist.", file=sys.stderr
        )
        return 1

    if vm_manager.vm_exists(args.name):
        print(
            f"Error: A VM with the name '{args.name}' already exists.", file=sys.stderr
        )
        return 1

    # --- Cloning Process ---
    print(f"\nCloning '{SOURCE_VM_NAME}' to new VM '{args.name}'...")

    try:
        vm_manager.clone_vm(
            source=SOURCE_VM_NAME,
            target=args.name,
            ram=args.ram,
            cpus=args.cpus,
            disk_size=args.disk_size,
        )

        print("\nCloning complete!")
        print(
            f"New VM '{args.name}' has been created with a unique MAC address and serial number."
        )
        if args.ram:
            print(f"- RAM set to: {args.ram} MB")
        if args.cpus:
            print(f"- CPUs set to: {args.cpus}")
        if args.disk_size:
            print(f"- A new {args.disk_size}GB secondary disk has been attached.")
        print(f'\nYou can now start it by running: VBoxManage startvm "{args.name}"')
        return 0

    except subprocess.CalledProcessError as e:
        print("\n--- ERROR ---", file=sys.stderr)
        print("An error occurred while running a VBoxManage command.", file=sys.stderr)
        print(f"Command failed: {e.cmd}", file=sys.stderr)
        print(f"Error output:\n{e.stderr}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
