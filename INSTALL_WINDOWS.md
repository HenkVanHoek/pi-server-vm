# Installation and Usage on Windows

This guide provides instructions for using the `pi-server-vm` executables on a Windows 10 or Windows 11 system.

### Prerequisites

#### 1. Install VirtualBox

The scripts rely on the `VBoxManage.exe` command-line tool. Download and install the latest version of VirtualBox for Windows from the official website.

- **[Download VirtualBox](https://www.virtualbox.org/wiki/Downloads)**

During installation, ensure that the "VirtualBox Application" and "VirtualBox Command Line Utilities" are selected for installation.

### Procedure

#### 1. Download the Release Files

Go to the [GitHub Releases page](https://github.com/HenkVanHoek/pi-server-vm/releases/latest) for this project.

You will need to download **two** files for the latest release:
-   `pi-master-template-vX.X.X.ova` (The virtual machine template)
-   `executables-Windows.zip` (The command-line tools)

#### 2. Extract the Executables

The command-line tools are provided in a zip archive.

1.  Navigate to your `Downloads` folder.
2.  Right-click on `executables-Windows.zip` and select **"Extract All..."**.
3.  This will create a new folder containing the `create-master-vm.exe` and `clone-vm.exe` tools.

#### 3. Import the Master Template Appliance

You must first import the pre-built `.ova` file into VirtualBox.

1.  Open the VirtualBox application.
2.  Go to the menu **File -> Import Appliance...**
3.  Select the `pi-master-template-vX.X.X.ova` file you downloaded.
4.  Follow the on-screen prompts to complete the import.

#### 4. Run the Cloning Executable

You are now ready to create your first clone. The executables can be run directly from a Command Prompt (cmd) or PowerShell.

1.  Open a terminal and navigate into the folder where you extracted the executables.
2.  Run the `clone-vm` executable, providing a name for your new VM and any optional parameters.

        # Example: Create a new VM named 'pi-test-windows'
        .\clone-vm.exe pi-test-windows

        # Example: Create a more powerful VM and start it immediately
        .\clone-vm.exe my-powerful-pi --ram 4096 --cpus 4 --start

Your new virtual Pi will be created and will appear in the Oracle VM VirtualBox Manager, ready to use.
