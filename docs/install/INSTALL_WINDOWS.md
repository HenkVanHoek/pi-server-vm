# Installation and Usage on Windows

This guide provides the complete instructions for setting up and using the **pi-server-vm** project on a Windows 10 or Windows 11 system.

---

## Phase 1: Host System Preparation

### 1. Install VirtualBox

The project requires the **Oracle VM VirtualBox** application and its command-line tools.

-   **[Download VirtualBox](https://www.virtualbox.org/wiki/Downloads)**

Download and run the installer for Windows. During installation, use the default settings. This will correctly install the necessary bridged networking drivers.

---

## Phase 2: Project Setup

### 1. Download the Release Files

Go to the [GitHub Releases page](https://github.com/HenkVanHoek/pi-server-vm/releases/latest) for this project.

You will need to download **two** types of files for the latest release:
-   The virtual machine template, which is a file ending in **.ova**.
-   The command-line tools for Windows, which is a file ending in **.zip**.

### 2. Extract the Executables

1.  Navigate to your **Downloads** folder.
2.  Right-click on the downloaded **.zip** file (e.g., **executables-Windows.zip**) and select **"Extract All..."**.
3.  This will create a new folder containing the **create-master-vm.exe** and **clone-vm.exe** tools.

### 3. Import the Master Template Appliance

You must first import the pre-built **.ova** file into VirtualBox.

1.  Open the **Oracle VM VirtualBox** application.
2.  Go to the menu **File -> Import Appliance...**
3.  Select the **.ova** file you downloaded.
4.  On the settings review screen, you can leave all settings as they are and click **Import**. The network adapter will be automatically configured for bridged networking.

---

## Phase 3: Creating Your First Virtual Pi

You are now ready to create your first clone.

1.  Open a Command Prompt (cmd) or PowerShell.
2.  Navigate into the folder where you extracted the executables.
3.  Run the **clone-vm.exe** tool, providing a name for your new VM and any optional parameters.

        # Example: Create a new VM named 'pi-test-windows'
        .\clone-vm.exe pi-test-windows

        # Example: Create a more powerful VM and start it immediately
        .\clone-vm.exe my-powerful-pi --ram 4096 --cpus 4 --start

Your new virtual Pi will be created and will appear in the Oracle VM VirtualBox Manager. After it starts, it will be visible on your local network, ready for use.
