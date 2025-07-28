# vm_manager.py
import subprocess
import random
import re
import os

class VMManager:
    def run(self, cmd):
        print(f"Running: {cmd}")
        subprocess.run(cmd, shell=True, check=True)

    def vm_exists(self, name):
        result = subprocess.run(
            ["VBoxManage", "list", "vms"],
            capture_output=True,
            text=True
        )
        return name in result.stdout

    def generate_pi_mac(self):
        # Raspberry Pi Foundation OUI: B8:27:EB or DC:A6:32
        prefixes = ["b8:27:eb", "dc:a6:32"]
        prefix = random.choice(prefixes)
        suffix = ":".join(f"{random.randint(0x00, 0xFF):02x}" for _ in range(3))
        return f"{prefix}:{suffix}"

    def generate_serial_number(self):
        # 16-char hex string like real Pi serials
        return ''.join(random.choices('0123456789abcdef', k=16))

    def create_vm(self, name, ram, cpus, disk, iso, bridge=True):
        self.run(f"VBoxManage createvm --name {name} --register")
        self.run(f"VBoxManage modifyvm {name} --memory {ram} --cpus {cpus} --boot1 dvd --nic1 bridged --bridgeadapter1 enp0s3")

        self.run(f"VBoxManage createhd --filename {disk} --size 8000")
        self.run(f"VBoxManage storagectl {name} --name 'SATA Controller' --add sata --controller IntelAhci")
        self.run(f"VBoxManage storageattach {name} --storagectl 'SATA Controller' --port 0 --device 0 --type hdd --medium {disk}")
        self.run(f"VBoxManage storageattach {name} --storagectl 'SATA Controller' --port 1 --device 0 --type dvddrive --medium {iso}")

        mac = self.generate_pi_mac()
        self.run(f"VBoxManage modifyvm {name} --macaddress1 {mac.replace(':', '')}")

        # Save the serial number as a description tag
        serial = self.generate_serial_number()
        self.run(f"VBoxManage modifyvm {name} --description 'serial:{serial}'")

    def clone_vm(self, source, target):
        self.run(f"VBoxManage clonevm {source} --name {target} --register")
        new_mac = self.generate_pi_mac()
        serial = self.generate_serial_number()
        self.run(f"VBoxManage modifyvm {target} --macaddress1 {new_mac.replace(':', '')}")
        self.run(f"VBoxManage modifyvm {target} --description 'serial:{serial}'")

    def get_serial(self, vm_name):
        result = subprocess.run(["VBoxManage", "showvminfo", vm_name, "--machinereadable"],
                                capture_output=True, text=True)
        match = re.search(r'description="serial:([0-9a-f]+)"', result.stdout)
        return match.group(1) if match else None
