# scripts/clone_vm.py
"""
A cross-platform script to clone the master Debian VM template.

This script creates a new VM by cloning 'pi-master-template'.
It requires one command-line argument: the name for the new VM.

The new VM will be assigned a unique MAC address and serial number.
"""

import os
import platform
import shutil
import sys
from vm_manager import VMManager

# --- Configuration ---
SOURCE_VM_NAME = "pi-master-template"


def setup_environment():
    """
    Finds VBoxManage and adds it to the PATH if necessary.

    Returns:
        bool: True if VBoxManage is found, False otherwise.
    """
    # 1. Best case: Is VBoxManage already in the system's PATH?
    if shutil.which("VBoxManage"):
        print("VBoxManage found in system PATH.")
        return True

    # 2. Fallback: Check known default installation locations.
    system = platform.system()
    if system == "Windows":
        # The .exe is required on Windows for os.path.exists
        vbox_exe = "VBoxManage.exe"
        # 64-bit program files is the most common
        vbox_path = r"C:\Program Files\Oracle\VirtualBox"
    elif system in ("Linux", "Darwin"):  # Darwin is the system name for macOS
        vbox_exe = "VBoxManage"
        # On macOS and Linux, it's usually in a PATH directory like /usr/local/bin
        # This check is for non-standard installations.
        vbox_path = "/usr/local/bin"  # A common fallback for macOS
    else:
        vbox_path = None

    if vbox_path and os.path.exists(os.path.join(vbox_path, vbox_exe)):
        print(f"Found VirtualBox at: {vbox_path}")
        os.environ["PATH"] = f'{os.environ["PATH"]}{os.pathsep}{vbox_path}'
        return True

    # 3. Worst case: We could not find it.
    print("Error: Could not find VBoxManage executable.", file=sys.stderr)
    print("Please ensure VirtualBox is installed and its directory is in your system's PATH.", file=sys.stderr)
    return False


def main():
    """Main execution function."""
    # This setup function makes the script cross-platform.
    if not setup_environment():
        return 1

    manager = VMManager()

    # --- Pre-flight Checks ---
    if len(sys.argv) < 2:
        print("Error: You must provide a name for the new cloned VM.", file=sys.stderr)
        print(f"Usage: python {sys.argv[0]} <new-vm-name>", file=sys.stderr)
        return 1

    target_vm_name = sys.argv[1]

    if not manager.vm_exists(SOURCE_VM_NAME):
        print(f"Error: The source VM '{SOURCE_VM_NAME}' does not exist.", file=sys.stderr)
        return 1

    if manager.vm_exists(target_vm_name):
        print(f"Error: A VM with the name '{target_vm_name}' already exists.", file=sys.stderr)
        return 1

    # --- Cloning Process ---
    print(f"\nCloning '{SOURCE_VM_NAME}' to new VM '{target_vm_name}'...")
    manager.clone_vm(source=SOURCE_VM_NAME, target=target_vm_name)

    print("\nCloning complete!")
    print(f"New VM '{target_vm_name}' has been created with a unique MAC address and serial number.")
    print(f"You can now start it by running: VBoxManage startvm \"{target_vm_name}\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())