## Quick Start

1.  **Download** the latest `.ova` appliance and the executable for your operating system from the [**GitHub Releases page**](https://github.com/HenkVanHoek/pi-server-vm/releases/latest).
2.  **Import** the `.ova` file into VirtualBox.
3.  **Run** the `clone-vm` executable from your terminal to create a new virtual machine.

    # Example:
    ./clone-vm-executable-name my-first-pi --ram 2048 --start

For detailed, step-by-step instructions for your specific operating system, please see the guides below:
[dist](../dist)
-   ➡️ **[Installation Guide for Windows](INSTALL_WINDOWS.md)**
-   ➡️ **[Installation Guide for macOS](INSTALL_MACOS.md)**
-   ➡️ **[Installation Guide for Linux](INSTALL_LINUX.md)**

### Prerequisites

#### 1. Install VirtualBox

The scripts rely on the `VBoxManage.exe` command-line tool. Download and install the latest version of VirtualBox for Windows from the official website.

- **[Download VirtualBox](https://www.virtualbox.org/wiki/Downloads)**

During installation, ensure that the "VirtualBox Application" and "VirtualBox Command Line Utilities" are selected for installation. It is also recommended to allow the installer to add its location to the system PATH.

### Procedure

#### 1. Download the Release Files

Go to the [GitHub Releases page](https://github.com/HenkVanHoek/pi-server-vm/releases/latest) for this project.

Download the following files for the latest release:
-   `pi-master-template-vX.X.X.ova`
-   `create-master-vm-windows-amd64.exe`
-   `clone-vm-windows-amd64.exe`

#### 2. Import the Master Template Appliance

You must first import the pre-built `.ova` file into VirtualBox. This will create the `pi-master-template` VM that the cloning script depends on.

1.  Open the VirtualBox application.
2.  Go to the menu **File -> Import Appliance...**
3.  Select the `pi-master-template-vX.X.X.ova` file you downloaded.
4.  Follow the on-screen prompts to complete the import.

#### 3. Run the Cloning Executable

You are now ready to create your first clone. The executables can be run directly from a Command Prompt (cmd) or PowerShell.

1.  Open a terminal and navigate to your `Downloads` folder (or wherever you saved the files).
2.  Run the `clone-vm` executable.
3.  Provide a name for your new VM and any optional parameters.

        # Example: Create a new VM named 'pi-test-windows'
        .\clone-vm-windows-amd64.exe pi-test-windows

        # Example: Create a more powerful VM and start it immediately
        .\clone-vm-windows-amd64.exe my-powerful-pi --ram 4096 --cpus 4 --start

Your new virtual Pi will be created and will appear in the Oracle VM VirtualBox Manager, ready to use.
