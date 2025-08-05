# scripts/clone_vm.py
"""
A cross-platform script to clone the master Debian VM template.

This script creates a new, configurable VM by cloning 'pi-master-template'.
It supports command-line arguments to customize RAM, CPUs, user, password,
a secondary disk, and whether to start the VM after creation.
"""

import argparse
import shlex
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
    parser.add_argument("name", help="The name for the new cloned virtual machine.")
    parser.add_argument(
        "--ram",
        type=int,
        help="Amount of RAM in megabytes for the new VM (e.g., 2048 for 2GB).\nDefaults to the master template setting.",
    )
    parser.add_argument(
        "--cpus",
        type=int,
        help="Number of CPU cores for the new VM (e.g., 2 or 4).\nDefaults to the master template setting.",
    )
    parser.add_argument(
        "--disk-size",
        type=int,
        help="Size in gigabytes for a new, secondary virtual disk (e.g., 32 for 32GB).\nIf omitted, no secondary disk is created.",
    )
    parser.add_argument(
        "--user",
        type=str,
        help="The username for the default user. Defaults to 'pivm'.",
    )
    parser.add_argument(
        "--password",
        type=str,
        help="The password for the user.\nIf not set, you will be forced to change the default password on first login.",
    )
    parser.add_argument(
        "--start",
        action="store_true",
        help="Automatically start the VM after it is cloned.",
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
        print(f"New VM '{args.name}' has been created.")
        if args.ram:
            print(f"- RAM set to: {args.ram} MB")
        if args.cpus:
            print(f"- CPUs set to: {args.cpus}")
        if args.disk_size:
            print(f"- A new {args.disk_size}GB secondary disk has been attached.")
        if args.user or args.password:
            user_disp = args.user or "pivm"
            print(f"- User '{user_disp}' has been configured.")

        if args.start:
            print(f"\nVM '{args.name}' is starting up...")
        else:
            print(
                f'\nYou can now start it by running: VBoxManage startvm "{args.name}"'
            )
        return 0

    except subprocess.CalledProcessError as e:
        print("\n--- ERROR ---", file=sys.stderr)
        # The 'e.cmd' attribute is only available on CalledProcessError
        cmd_string = shlex.join(e.cmd) if hasattr(e, "cmd") else "N/A"
        print(
            f"An error occurred while running a VBoxManage command: {cmd_string}",
            file=sys.stderr,
        )
        print(f"Error output:\n{e.stderr}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
