# Installation and Usage on Linux (Ubuntu Desktop)

**Minimum Requirement:** macOS 10.15 (Catalina)

The provided executable is built to be compatible with macOS 10.15 and all newer versions.
This guide provides the complete instructions for setting up and using the **pi-server-vm** project on a Linux system, such as Ubuntu Desktop.

---

## Phase 1: Host System Preparation

### 1. Install VirtualBox and System Tools

Install VirtualBox from the official Ubuntu repositories and update your system.

    sudo apt update
    sudo apt install -y virtualbox virtualbox-guest-additions-iso
    sudo apt upgrade -y

### 2. Add Your User to the vboxusers Group

This is required to run VirtualBox without needing **sudo**.

    # This command uses the $USER variable for your current username
    sudo adduser $USER vboxusers

**IMPORTANT:** You must **log out and log back in** for this group change to take effect.

### 3. Prevent KVM Conflict (Recommended)

This permanently prevents the native Linux KVM hypervisor from conflicting with VirtualBox, which can cause startup errors.

1.  **Create the blacklist file:**
        sudo nano /etc/modprobe.d/blacklist-kvm.conf

2.  **Add the following content:**
        blacklist kvm
        blacklist kvm_intel

3.  **Update the initial RAM filesystem and reboot:**
        sudo update-initramfs -u
        reboot

---

## Phase 2: Project Setup

### 1. Download the Release Files

Go to the [GitHub Releases page](https://github.com/HenkVanHoek/pi-server-vm/releases/latest) for this project.

You will need to download **two** types of files for the latest release:
-   The virtual machine template, which is a file ending in **.ova**.
-   The command-line tools for Linux, which is a file ending in **.tar.gz**.

### 2. Extract the Executables

1.  Open your terminal and navigate to your **Downloads** folder.
2.  Run the **tar** command to extract the archive. The files will already be executable.

        tar -xvzf executables-Linux.tar.gz

    This will create a new folder containing the **create-master-vm** and **clone-vm** tools.

### 3. Import the Master Template Appliance

You must first import the pre-built **.ova** file into VirtualBox.

1.  Open the **VirtualBox** application.
2.  Go to the menu **File -> Import Appliance...**
3.  Select the **.ova** file you downloaded.
4.  On the settings review screen, you can leave all settings as they are and click **Import**. The network adapter will be automatically configured for bridged networking.

---

## Phase 3: Creating Your First Virtual Pi

You are now ready to create your first clone.

1.  In your terminal, navigate into the folder where you extracted the executables.
2.  Run the **clone-vm** tool, providing a name for your new VM and any optional parameters.

        # Example: Create a new VM named 'pi-test-linux'
        ./clone-vm pi-test-linux

        # Example: Create a more powerful VM and start it immediately
        ./clone-vm my-powerful-pi --ram 4096 --cpus 4 --start

Your new virtual Pi will be created and will appear in the VirtualBox Manager. After it starts, it will be visible on your local network, ready for use.
