# create_master_vm.py
import os
from vm_manager import VMManager
vbox_path = r"C:\Program Files\Oracle\VirtualBox"
os.environ["PATH"] += os.pathsep + vbox_path
ISO_PATH = "/home/hvhoek/isos/debian-12.5.0-amd64-netinst.iso"  # Adjust if needed
VM_NAME = "pi-master-template"
VM_DISK = f"{VM_NAME}.vdi"
VM_RAM_MB = 1024
VM_CPUS = 1

def main():
    manager = VMManager()

    if manager.vm_exists(VM_NAME):
        print(f"VM '{VM_NAME}' already exists.")
        return

    print(f"Creating master VM: {VM_NAME}")
    manager.create_vm(
        name=VM_NAME,
        ram=VM_RAM_MB,
        cpus=VM_CPUS,
        disk=VM_DISK,
        iso=ISO_PATH,
        bridge=True
    )

    print("VM created. Please complete Debian installation manually.")
    print("After setup, shut it down and run 'VBoxManage snapshot' to create a clean snapshot.")

if __name__ == "__main__":
    main()
