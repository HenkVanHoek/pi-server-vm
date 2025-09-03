# scripts/vm_manager.py
"""
A module of helper functions to manage VirtualBox VMs using a simple,
single Bridged Adapter network configuration.
"""

import os
import platform
import random
import shutil
import subprocess
import sys


# --- Public Functions ---


def setup_environment():
    """Finds the VBoxManage executable and adds its directory to the system PATH."""
    if shutil.which("VBoxManage"):
        return True

    system = platform.system()
    vbox_path = None
    if system == "Windows":
        vbox_exe_name = "VBoxManage.exe"
        vbox_path = r"C:\Program Files\Oracle\VirtualBox"
    elif system in ("Linux", "Darwin"):
        vbox_exe_name = "VBoxManage"
        vbox_path = "/usr/local/bin"
    else:
        vbox_exe_name = None

    if (
        vbox_path
        and vbox_exe_name
        and os.path.exists(os.path.join(vbox_path, vbox_exe_name))
    ):
        os.environ["PATH"] = f'{os.environ["PATH"]}{os.pathsep}{vbox_path}'
        return True

    print("Error: Could not find VBoxManage executable.", file=sys.stderr)
    return False


def run(cmd):
    """Execute a shell command and raise an exception if it fails."""
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)


def vm_exists(name):
    """Check if a virtual machine with the given name already exists."""
    result = subprocess.run(
        ["VBoxManage", "list", "vms"], capture_output=True, text=True, check=False
    )
    return f'"{name}"' in result.stdout


def generate_pi_mac():
    """Generate a random MAC address using a Raspberry Pi Foundation OUI."""
    prefixes = ["b827eb", "dca632"]
    prefix = random.choice(prefixes)
    suffix = "".join(f"{random.randint(0x00, 0xFF):02x}" for _ in range(3))
    return f"{prefix}{suffix}"


def generate_serial_number():
    """Generate a random 16-character hexadecimal string for the VM serial."""
    return "".join(random.choices("0123456789abcdef", k=16))


def get_first_bridged_adapter():
    """Find the name of the first available bridged network adapter."""
    result = subprocess.run(
        ["VBoxManage", "list", "bridgedifs"], capture_output=True, text=True, check=True
    )
    for line in result.stdout.splitlines():
        if line.strip().startswith("Name:"):
            return line.split(":", 1)[1].strip()
    raise RuntimeError("No bridged network adapter found.")


def create_vm(name, ram, cpus, disk, iso):
    """Creates, configures, and starts a new VM with a single bridged adapter."""
    run(f'VBoxManage createvm --name "{name}" --register')

    bridge_adapter_name = get_first_bridged_adapter()
    # Programmatically set Promiscuous Mode to 'Allow All' for better network discovery.
    run(
        f'VBoxManage modifyvm "{name}" --memory {ram} --cpus {cpus} '
        f'--boot1 dvd --nic1 bridged --bridgeadapter1="{bridge_adapter_name}" '
        f"--nicpromisc1 allow-all"
    )

    disk_path = os.path.abspath(disk)
    iso_path = os.path.abspath(iso)
    run(f'VBoxManage createhd --filename "{disk_path}" --size 8000')
    run(
        f'VBoxManage storagectl "{name}" --name="SATA Controller" '
        "--add sata --controller IntelAhci"
    )
    run(
        f'VBoxManage storageattach "{name}" --storagectl="SATA Controller" '
        f'--port 0 --device 0 --type hdd --medium "{disk_path}"'
    )
    run(
        f'VBoxManage storageattach "{name}" --storagectl="SATA Controller" '
        f'--port 1 --device 0 --type dvddrive --medium "{iso_path}"'
    )

    mac = generate_pi_mac()
    run(f'VBoxManage modifyvm "{name}" --macaddress1 {mac}')

    serial = generate_serial_number()
    run(f'VBoxManage modifyvm "{name}" --description "serial:{serial}"')

    run(f'VBoxManage startvm "{name}"')


def clone_vm(
    source,
    target,
    ram=None,
    cpus=None,
    disk_size=None,
    user=None,
    password=None,
    start_vm=False,
):
    """
    Clones an existing VM and applies customizations. Assumes a single Bridged Adapter.
    """
    run(f'VBoxManage clonevm "{source}" --name "{target}" --register')

    # Assign new unique identifiers
    new_mac = generate_pi_mac()
    serial = generate_serial_number()
    run(f'VBoxManage modifyvm "{target}" --macaddress1 {new_mac}')
    run(f'VBoxManage modifyvm "{target}" --description "serial:{serial}"')

    # Set guest properties for the first-boot configuration script
    run(
        f'VBoxManage guestproperty set "{target}" /VirtualBox/GuestAdd/hostname "{target}"'
    )
    if user:
        run(
            f'VBoxManage guestproperty set "{target}" /VirtualBox/GuestAdd/user "{user}"'
        )
    if password:
        run(
            f'VBoxManage guestproperty set "{target}" /VirtualBox/GuestAdd/password "{password}"'
        )
        # Create the content for the PiSelfhosting info file
        print("--- ACTION: Preparing PiSelfhosting identity file content ---")
        info_file_content = f"""MODEL_NAME=PiSelfhosting Virtual Pi
    SERIAL_NUMBER={serial}
    HOSTNAME={target}""".strip()

        # Set the content as a new Guest Property
        run(
            f'VBoxManage guestproperty set "{target}" /VirtualBox/GuestAdd/PiSelfhostingInfo "{info_file_content}"'
        )
        print("✅ PiSelfhosting identity file content has been set.")

    # Apply optional hardware customizations
    if ram:
        run(f'VBoxManage modifyvm "{target}" --memory {ram}')
    if cpus:
        run(f'VBoxManage modifyvm "{target}" --cpus {cpus}')
    if disk_size:
        print(f"Creating and attaching a new {disk_size}GB secondary disk...")
        vm_info_result = subprocess.run(
            ["VBoxManage", "showvminfo", target, "--machinereadable"],
            capture_output=True,
            text=True,
            check=True,
        )
        cfg_file_line = [
            line
            for line in vm_info_result.stdout.splitlines()
            if line.startswith("CfgFile=")
        ][0]
        vm_dir = os.path.dirname(cfg_file_line.split("=", 1)[1].strip().strip('"'))
        disk_path = os.path.join(vm_dir, f"{target}-disk2.vdi")
        disk_size_mb = disk_size * 1024
        run(f'VBoxManage createhd --filename "{disk_path}" --size {disk_size_mb}')
        run(
            f'VBoxManage storageattach "{target}" --storagectl="SATA Controller" '
            f'--port 2 --device 0 --type hdd --medium "{disk_path}"'
        )

    # Conditionally start the VM
    if start_vm:
        run(f'VBoxManage startvm "{target}"')
