# Installation and Usage on macOS

This guide provides the complete instructions for setting up and using the **pi-server-vm** project on a macOS system.

---

## Phase 1: Host System Preparation

### 1. Install VirtualBox

The project requires the **Oracle VM VirtualBox** application and its command-line tools.

- **[Download VirtualBox](https://www.virtualbox.org/wiki/Downloads)**

Download and run the installer for macOS. During installation, you may be prompted to allow kernel extensions in your **System Settings -> Privacy & Security**. Please approve this for VirtualBox to function correctly.

---

## Phase 2: Project Setup

### 1. Download the Release Files

Go to the [GitHub Releases page](https://github.com/HenkVanHoek/pi-server-vm/releases/latest) for this project.

You will need to download **two** types of files for the latest release:
-   The virtual machine template, which is a file ending in **.ova**.
-   The command-line tools for macOS, which is a file ending in **.tar.gz**.

### 2. Extract the Executables

1.  Open the **Terminal** app.
2.  Navigate to your **Downloads** folder.
3.  Run the **tar** command to extract the archive. The files will already be executable.

        tar -xvzf executables-macOS.tar.gz

    This will create a new folder containing the **create-master-vm** and **clone-vm** tools.

### 3. Import the Master Template Appliance

You must first import the pre-built **.ova** file into VirtualBox.

1.  Open the **VirtualBox** application from your **/Applications** folder.
2.  Go to the menu **File -> Import Appliance...**
3.  Select the **.ova** file you downloaded.
4.  On the settings review screen, you can leave all settings as they are and click **Import**. The network adapter will be automatically configured for bridged networking.

---

## Phase 3: Creating Your First Virtual Pi

You are now ready to create your first clone.

1.  In your Terminal, navigate into the folder where you extracted the executables.
2.  Run the **clone-vm** tool, providing a name for your new VM and any optional parameters.

        # Example: Create a new VM named 'pi-test-macos'
        ./clone-vm pi-test-macos

        # Example: Create a more powerful VM and start it immediately
        ./clone-vm my-powerful-pi --ram 4096 --cpus 4 --start

Your new virtual Pi will be created and will appear in the VirtualBox Manager. After it starts, it will be visible on your local network, ready for use.
