# vm_manager.py
"""
A module to provide a high-level interface for managing VirtualBox VMs.

This manager class handles the creation, cloning, and modification of
VirtualBox virtual machines using the VBoxManage command-line tool.
"""

import os
import random
import re
import subprocess


class VMManager:
    """A collection of static methods to manage VirtualBox VMs."""

    @staticmethod
    def run(cmd):
        """
        Execute a shell command and raise an exception if it fails.

        Args:
            cmd (str): The command to execute.
        """
        print(f"Running: {cmd}")
        subprocess.run(cmd, shell=True, check=True)

    @staticmethod
    def vm_exists(name):
        """
        Check if a virtual machine with the given name already exists.

        Args:
            name (str): The name of the VM to check.

        Returns:
            bool: True if the VM exists, False otherwise.
        """
        result = subprocess.run(
            ["VBoxManage", "list", "vms"],
            capture_output=True,
            text=True,
            check=False  # Do not fail if no VMs exist
        )
        return name in result.stdout

    @staticmethod
    def generate_pi_mac():
        """
        Generate a random MAC address using a Raspberry Pi Foundation OUI.

        Returns:
            str: A 12-character hex string MAC address (without separators).
        """
        # Official Raspberry Pi Foundation OUIs (Organizationally Unique Identifiers)
        prefixes = ["b827eb", "dca632"]
        prefix = random.choice(prefixes)
        suffix = ''.join(f"{random.randint(0x00, 0xFF):02x}" for _ in range(3))
        return f"{prefix}{suffix}"

    @staticmethod
    def generate_serial_number():
        """
        Generate a random 16-character hexadecimal string for the VM serial.

        Returns:
            str: A 16-character hex string.
        """
        return ''.join(random.choices('0123456789abcdef', k=16))

    @staticmethod
    def get_first_bridged_adapter():
        """
        Find the name of the first available bridged network adapter.

        Raises:
            RuntimeError: If no bridged network adapters are found.

        Returns:
            str: The name of the first bridged adapter.
        """
        result = subprocess.run(
            ["VBoxManage", "list", "bridgedifs"],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            if line.strip().startswith("Name:"):
                return line.split(":", 1)[1].strip()
        raise RuntimeError("No bridged network adapter found.")

    @staticmethod
    def get_serial(vm_name):
        """
        Retrieve the custom serial number from a VM's description.

        Args:
            vm_name (str): The name of the virtual machine.

        Returns:
            str or None: The serial number if found, otherwise None.
        """
        result = subprocess.run(
            ["VBoxManage", "showvminfo", vm_name, "--machinereadable"],
            capture_output=True,
            text=True,
            check=True
        )
        match = re.search(r'description="serial:([0-9a-f]+)"', result.stdout)
        return match.group(1) if match else None

    def create_vm(self, name, ram, cpus, disk, iso, bridge=True):
        """
        Create, configure, and start a new virtual machine.

        Args:
            name (str): The name for the new VM.
            ram (int): The amount of RAM in megabytes.
            cpus (int): The number of CPU cores.
            disk (str): The path for the virtual hard disk file.
            iso (str): The path to the installation ISO.
            bridge (bool): Whether to use a bridged network adapter.
        """
        self.run(f'VBoxManage createvm --name "{name}" --register')
        bridge_adapter = self.get_first_bridged_adapter() if bridge else "null"
        self.run(
            f'VBoxManage modifyvm "{name}" --memory {ram} --cpus {cpus} '
            f'--boot1 dvd --nic1 bridged --bridgeadapter1="{bridge_adapter}"'
        )

        disk_path = os.path.abspath(disk)
        iso_path = os.path.abspath(iso)

        self.run(f'VBoxManage createhd --filename "{disk_path}" --size 8000')
        self.run(
            f'VBoxManage storagectl "{name}" --name="SATA Controller" '
            '--add sata --controller IntelAhci'
        )
        self.run(
            f'VBoxManage storageattach "{name}" --storagectl="SATA Controller" '
            f'--port 0 --device 0 --type hdd --medium "{disk_path}"'
        )
        self.run(
            f'VBoxManage storageattach "{name}" --storagectl="SATA Controller" '
            f'--port 1 --device 0 --type dvddrive --medium "{iso_path}"'
        )

        mac = self.generate_pi_mac()
        self.run(f'VBoxManage modifyvm "{name}" --macaddress1 {mac}')

        serial = self.generate_serial_number()
        self.run(f'VBoxManage modifyvm "{name}" --description "serial:{serial}"')

        # --- ADDED LINE: Start the VM after creation ---
        self.run(f'VBoxManage startvm "{name}"')

    def clone_vm(self, source, target):
        """
        Clone an existing VM and assign it a new MAC and serial number.

        Args:
            source (str): The name of the source VM to clone.
            target (str): The name for the new cloned VM.
        """
        self.run(f'VBoxManage clonevm "{source}" --name "{target}" --register')
        new_mac = self.generate_pi_mac()
        serial = self.generate_serial_number()
        self.run(f'VBoxManage modifyvm "{target}" --macaddress1 {new_mac}')
        self.run(f'VBoxManage modifyvm "{target}" --description "serial:{serial}"')
        self.run(f'VBoxManage guestproperty set "{target}" /VirtualBox/GuestAdd/hostname "{target}"')