# Installation and Usage on macOS

This guide provides instructions for using the `pi-server-vm` executables on a macOS system.

### Prerequisites

#### 1. Install VirtualBox

The scripts rely on the `VBoxManage` command-line tool. Download and install the latest version of VirtualBox for macOS from the official website.

- **[Download VirtualBox](https://www.virtualbox.org/wiki/Downloads)**

The installer will place VirtualBox in your `/Applications` folder and make its command-line tools available in the system PATH.

### Procedure

#### 1. Download the Release Files

Go to the [GitHub Releases page](https://github.com/HenkVanHoek/pi-server-vm/releases/latest) for this project.

You will need to download **two** files for the latest release:
-   `pi-master-template-vX.X.X.ova` (The virtual machine template)
-   `executables-macOS.tar.gz` (The command-line tools)

#### 2. Extract the Executables

The command-line tools are provided in a standard tarball archive.

1.  Open the **Terminal** app.
2.  Navigate to your `Downloads` folder.
3.  Run the `tar` command to extract the archive:

        tar -xvzf executables-macOS.tar.gz

    This will create a new folder (likely named `dist` or similar) containing the `create-master-vm` and `clone-vm` tools. The files will already be executable.

#### 3. Import the Master Template Appliance

You must first import the pre-built `.ova` file into VirtualBox.

1.  Open the VirtualBox application.
2.  Go to the menu **File -> Import Appliance...**
3.  Select the `pi-master-template-vX.X.X.ova` file you downloaded.
4.  Follow the on-screen prompts to complete the import.

#### 4. Run the Cloning Executable

Now you are ready to create your first clone.

1.  In your Terminal, navigate into the folder where you extracted the executables.
2.  Run the `clone-vm` executable, providing a name for your new VM and any optional parameters.

        # Example: Create a new VM named 'pi-test-macos'
        ./clone-vm pi-test-macos

        # Example: Create a more powerful VM and start it immediately
        ./clone-vm my-powerful-pi --ram 4096 --cpus 4 --start

Your new virtual Pi will be created and will appear in the VirtualBox Manager, ready to use.
