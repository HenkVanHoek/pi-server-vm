# Developer Guide: Setting Up a Linux Host Environment

This guide provides the complete, end-to-end instructions for setting up a fresh Ubuntu Desktop installation to be a stable development host for the **pi-server-vm** project.

This process covers all the necessary steps to configure the host, install the tools, and prepare the master VM template from which all releases are built.

---

## Phase 1: Host System Preparation

### 1. Initial System Update
    sudo apt update
    sudo apt upgrade -y

### 2. Install Core Development and Virtualization Software
This installs VirtualBox, Git, and the Python tools needed for the project.
    sudo apt install -y git python3-venv python3-pip virtualbox virtualbox-guest-additions-iso

### 3. Add Your User to the vboxusers Group
    sudo adduser $USER vboxusers

**IMPORTANT:** You must **log out and log back in** for this group change to take effect.

### 4. Prevent KVM Conflict (Recommended)
This permanently prevents the native Linux KVM hypervisor from conflicting with VirtualBox.
1.  **Create the blacklist file:**
        sudo nano /etc/modprobe.d/blacklist-kvm.conf
2.  **Add the following content:**
        blacklist kvm
        blacklist kvm_intel
3.  **Update the initial RAM filesystem and reboot:**
        sudo update-initramfs -u
        reboot

---

## Phase 2: `pi-server-vm` Project and Master Template Setup

### 1. Clone the Repository and Install Dependencies
1.  Clone the project repository from GitHub:
        git clone https://github.com/HenkVanHoek/pi-server-vm.git
        cd pi-server-vm

2.  Create and activate a Python virtual environment:
        python3 -m venv .venv
        source .venv/bin/activate

3.  Install the project in editable mode and all dependencies:
        pip install -e .
        pip install -r requirements.txt

### 2. Create the Master Template from Scratch
This step uses the project's own tool to create the initial VM.
1.  Run the creation script:
        python -m scripts.create_master_vm

2.  A VirtualBox window will open with the Debian installer. Complete the manual installation:
    - **User:** Create a user named **pivm**.
    - **Software Selection:** Deselect the desktop and ensure **SSH Server** is selected.

### 3. Finalize the Master Template Configuration
This is the most critical phase, where the "golden image" is perfected.
1.  Start the newly installed **pi-master-template** VM and log in.
2.  **Install all required guest software:**
        sudo apt update
        sudo apt install -y build-essential dkms linux-headers-$(uname -r) avahi-daemon dos2unix vim
        sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin # After adding Docker repo
        sudo usermod -aG docker pivm

3.  **Install VirtualBox Guest Additions:**
    - From the VirtualBox menu: **Devices -> Insert Guest Additions CD Image...**
    - Run the installer inside the VM:
            sudo mount /dev/cdrom /mnt
            sudo /mnt/VBoxLinuxAdditions.run
            sudo reboot

4.  **Install Automation Scripts:** After rebooting, log in and install the project's first-boot and IP display scripts. (This step would involve copying the scripts into `/usr/local/bin` and enabling the `systemd` services).

5.  **Configure Network (Hardware):**
    - Shut down the master VM.
    - In VirtualBox, go to **Settings -> Network**.
    - Configure **Adapter 1** as a **Bridged Adapter** with **Promiscuous Mode** set to **Allow All**.
    - Ensure **Adapter 2** is disabled.

6.  **Configure Network (Guest OS):**
    - Start the master VM again.
    - Ensure the `/etc/network/interfaces` file is correctly configured for a single `enp0s3` adapter using DHCP.

7.  **"Seal" the Template for Distribution:**
    - Perform the final cleanup and compaction:
            sudo apt-get clean
            sudo dd if=/dev/zero of=/tmp/zeroes bs=1M || true
            sudo rm /tmp/zeroes
    - Shut down the VM.

Your development environment is now complete, and the **pi-master-template** is ready to be cloned for testing or exported as an **.ova** file for a new release.
