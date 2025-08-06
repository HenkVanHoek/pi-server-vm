# Installation and Usage on Linux (Ubuntu Desktop)

This guide provides instructions for using the `pi-server-vm` executables on a Linux system, such as Ubuntu Desktop.

### Prerequisites

(The Prerequisites section is still correct and does not need to be changed)

### Procedure

#### 1. Download the Release Files

Go to the [GitHub Releases page](https://github.com/HenkVanHoek/pi-server-vm/releases/latest) for this project.

You will need to download **two** files for the latest release:
-   `pi-master-template-vX.X.X.ova` (The virtual machine template)
-   `executables-Linux.tar.gz` (The command-line tools)

#### 2. Extract the Executables

The command-line tools are provided in a standard tarball archive.

1.  Open your terminal and navigate to your `Downloads` folder.
2.  Run the `tar` command to extract the archive:

        tar -xvzf executables-Linux.tar.gz

    This will create a new folder (likely named `dist` or similar) containing the `create-master-vm` and `clone-vm` tools. The files will already be executable.

#### 3. Import the Master Template Appliance

You must first import the pre-built `.ova` file into VirtualBox.

1.  Open the VirtualBox application.
2.  Go to the menu **File -> Import Appliance...**
3.  Select the `pi-master-template-vX.X.X.ova` file you downloaded.
4.  Follow the on-screen prompts to complete the import.

#### 4. Run the Cloning Executable

Now you are ready to create your first clone.

1.  In your terminal, navigate into the folder where you extracted the executables.
2.  Run the `clone-vm` executable, providing a name for your new VM and any optional parameters.

        # Example: Create a new VM named 'pi-test-linux'
        ./clone-vm pi-test-linux

        # Example: Create a more powerful VM and start it immediately
        ./clone-vm my-powerful-pi --ram 4096 --cpus 4 --start

Your new virtual Pi will be created and will appear in the VirtualBox Manager, ready to use.
