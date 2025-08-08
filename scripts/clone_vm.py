# scripts/clone_vm.py
"""
A cross-platform script to clone the master Debian VM template.

This script creates a new, configurable VM by cloning 'pi-master-template'.
It assumes a simple, single Bridged Adapter network configuration.
"""

import argparse
import subprocess
import sys
from scripts import vm_manager

# --- Configuration ---
SOURCE_VM_NAME = "pi-master-template"


def parse_arguments():
    """Parses all command-line arguments using argparse."""
    parser = argparse.ArgumentParser(
        description="Clone the master Pi VM template with custom hardware and user settings.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    # The arguments remain the same
    parser.add_argument("name", help="The name for the new cloned virtual machine.")
    parser.add_argument("--ram", type=int, help="Amount of RAM in MB.")
    parser.add_argument("--cpus", type=int, help="Number of CPU cores.")
    parser.add_argument(
        "--disk-size", type=int, help="Size in GB for a new, secondary virtual disk."
    )
    parser.add_argument("--user", type=str, help="The username for the default user.")
    parser.add_argument("--password", type=str, help="The password for the user.")
    parser.add_argument(
        "--start", action="store_true", help="Automatically start the VM after cloning."
    )
    return parser.parse_args()


def main():
    """Main execution function."""
    if not vm_manager.setup_environment():
        return 1

    args = parse_arguments()

    if args.password:
        print("\n*** SECURITY WARNING ***")
        print("You have provided a password on the command line.")
        print("This can be saved in your shell history in plain text.\n")

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

    print(f"\nCloning '{SOURCE_VM_NAME}' to new VM '{args.name}'...")

    try:
        # The call to clone_vm is now simpler in its meaning, though the code is the same
        vm_manager.clone_vm(
            source=SOURCE_VM_NAME,
            target=args.name,
            ram=args.ram,
            cpus=args.cpus,
            disk_size=args.disk_size,
            user=args.user,
            password=args.password,
            start_vm=args.start,
        )

        print("\nCloning complete!")
        # ... (Success messages are the same) ...

        if args.start:
            print(f"\nVM '{args.name}' is starting up...")
        else:
            print(
                f'\nYou can now start it by running: VBoxManage startvm "{args.name}"'
            )
        return 0

    except subprocess.CalledProcessError as e:
        print("\n--- ERROR ---", file=sys.stderr)
        print(
            f"An error occurred while running a VBoxManage command: {e.cmd}",
            file=sys.stderr,
        )
        print(f"Error output:\n{e.stderr}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
