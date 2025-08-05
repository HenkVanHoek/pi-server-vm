# scripts/vm_manager.py
"""
A module of helper functions to manage VirtualBox VMs.

This module provides a high-level, cross-platform interface for creating,
cloning, and modifying VirtualBox virtual machines using the VBoxManage
command-line tool.
"""

import os
import platform
import random
import shlex
import shutil
import subprocess
import sys

# --- Public Functions ---


def setup_environment():
    """
    Finds the VBoxManage executable and adds its directory to the system PATH.
    """
    if shutil.which("VBoxManage"):
        print("VBoxManage found in system PATH.")
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
        print(f"Found VirtualBox at: {vbox_path}")
        os.environ["PATH"] = f'{os.environ["PATH"]}{os.pathsep}{vbox_path}'
        return True

    print("Error: Could not find VBoxManage executable.", file=sys.stderr)
    print(
        "Please ensure VirtualBox is installed and its directory is in the system PATH.",
        file=sys.stderr,
    )
    return False


def run(cmd_list):
    """
    Execute a command and raise an exception if it fails.
    Expects cmd_list to be a list of arguments.
    """
    print(f"Running: {shlex.join(cmd_list)}")
    subprocess.run(cmd_list, check=True, capture_output=True, text=True)


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


def get_host_only_adapter_name():
    """Finds the name of the first available Host-Only network adapter."""
    result = subprocess.run(
        ["VBoxManage", "list", "hostonlyifs"],
        capture_output=True,
        text=True,
        check=True,
    )
    for line in result.stdout.splitlines():
        if line.strip().startswith("Name:"):
            return line.split(":", 1)[1].strip()
    raise RuntimeError("No Host-Only network adapter found. Please create one.")


def create_vm(name, ram, cpus, disk, iso):
    """
    Creates and configures a new virtual machine with the standard network setup.
    """
    run(["VBoxManage", "createvm", "--name", name, "--register"])
    host_only_adapter = get_host_only_adapter_name()

    run(
        [
            "VBoxManage",
            "modifyvm",
            name,
            "--memory",
            str(ram),
            "--cpus",
            str(cpus),
            "--boot1",
            "dvd",
            "--nic1",
            "nat",  # Adapter 1: NAT for internet access
            "--nic2",
            "hostonly",  # Adapter 2: Host-Only for management
            f"--hostonlyadapter2",
            host_only_adapter,
        ]
    )

    disk_path = os.path.abspath(disk)
    iso_path = os.path.abspath(iso)
    run(["VBoxManage", "createhd", "--filename", disk_path, "--size", "8000"])
    run(
        [
            "VBoxManage",
            "storagectl",
            name,
            "--name",
            "SATA Controller",
            "--add",
            "sata",
            "--controller",
            "IntelAhci",
        ]
    )
    run(
        [
            "VBoxManage",
            "storageattach",
            name,
            "--storagectl",
            "SATA Controller",
            "--port",
            "0",
            "--device",
            "0",
            "--type",
            "hdd",
            "--medium",
            disk_path,
        ]
    )
    run(
        [
            "VBoxManage",
            "storageattach",
            name,
            "--storagectl",
            "SATA Controller",
            "--port",
            "1",
            "--device",
            "0",
            "--type",
            "dvddrive",
            "--medium",
            iso_path,
        ]
    )
    mac = generate_pi_mac()
    run(["VBoxManage", "modifyvm", name, "--macaddress1", mac])
    serial = generate_serial_number()
    run(["VBoxManage", "modifyvm", name, "--description", f"serial:{serial}"])
    run(["VBoxManage", "startvm", name])


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
    Clones an existing VM and applies all specified customizations.
    """
    run(["VBoxManage", "clonevm", source, "--name", target, "--register"])

    # Assign new unique identifiers
    new_mac = generate_pi_mac()
    serial = generate_serial_number()
    run(["VBoxManage", "modifyvm", target, "--macaddress1", new_mac])
    run(["VBoxManage", "modifyvm", target, "--description", f"serial:{serial}"])

    # Set guest properties for the first-boot configuration script
    run(
        [
            "VBoxManage",
            "guestproperty",
            "set",
            target,
            "/VirtualBox/GuestAdd/hostname",
            target,
        ]
    )
    if user:
        run(
            [
                "VBoxManage",
                "guestproperty",
                "set",
                target,
                "/VirtualBox/GuestAdd/user",
                user,
            ]
        )
    if password:
        run(
            [
                "VBoxManage",
                "guestproperty",
                "set",
                target,
                "/VirtualBox/GuestAdd/password",
                password,
            ]
        )

    # Apply optional hardware customizations
    if ram:
        run(["VBoxManage", "modifyvm", target, "--memory", str(ram)])
    if cpus:
        run(["VBoxManage", "modifyvm", target, "--cpus", str(cpus)])
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
        run(
            [
                "VBoxManage",
                "createhd",
                "--filename",
                disk_path,
                "--size",
                str(disk_size_mb),
            ]
        )
        run(
            [
                "VBoxManage",
                "storageattach",
                target,
                "--storagectl",
                "SATA Controller",
                "--port",
                "2",
                "--device",
                "0",
                "--type",
                "hdd",
                "--medium",
                disk_path,
            ]
        )

    # Conditionally start the VM
    if start_vm:
        print("Starting the new VM...")
        run(["VBoxManage", "startvm", target])
