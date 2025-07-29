# scripts/clone_vm.py
"""
A script to clone the master Debian VM template.

This script creates a new VM by cloning 'pi-master-template'.
It requires one command-line argument: the name for the new VM.

The new VM will be assigned a unique MAC address and serial number.
"""

import os
import sys
from vm_manager import VMManager

# --- Configuration ---
# Set path to your VirtualBox installation directory
VBOX_PATH = r"C:\Program Files\Oracle\VirtualBox"
SOURCE_VM_NAME = "pi-master-template"


def main():
    """Main execution function."""
    # Add VirtualBox to the system's PATH environment variable
    os.environ["PATH"] = f'{os.environ["PATH"]}{os.pathsep}{VBOX_PATH}'
    manager = VMManager()

    # --- Pre-flight Checks ---

    # Check if a name for the new VM was provided
    if len(sys.argv) < 2:
        print("Error: You must provide a name for the new cloned VM.", file=sys.stderr)
        print(f"Usage: python {sys.argv[0]} <new-vm-name>", file=sys.stderr)
        return 1

    target_vm_name = sys.argv[1]

    # Check if the source VM template exists
    if not manager.vm_exists(SOURCE_VM_NAME):
        print(
            f"Error: The source VM '{SOURCE_VM_NAME}' does not exist.",
            file=sys.stderr
        )
        print("Please create it first by running 'create_master_vm.py'.", file=sys.stderr)
        return 1

    # Check if the target VM name is already in use
    if manager.vm_exists(target_vm_name):
        print(
            f"Error: A VM with the name '{target_vm_name}' already exists.",
            file=sys.stderr
        )
        return 1

    # --- Cloning Process ---

    print(f"Cloning '{SOURCE_VM_NAME}' to new VM '{target_vm_name}'...")
    manager.clone_vm(source=SOURCE_VM_NAME, target=target_vm_name)

    print("\nCloning complete!")
    print(f"New VM '{target_vm_name}' has been created with a unique MAC address and serial number.")
    print(f"You can now start it by running: VBoxManage startvm {target_vm_name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())