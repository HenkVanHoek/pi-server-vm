# Installation and Usage on macOS

This guide provides instructions for using the `pi-server-vm` executables on a macOS system.

### Prerequisites

#### 1. Install VirtualBox

The scripts rely on the `VBoxManage` command-line tool. Download and install the latest version of VirtualBox for macOS from the official website.

- **[Download VirtualBox](https://www.virtualbox.org/wiki/Downloads)**

After installing, VirtualBox is typically located in your `/Applications` folder, and its command-line tools are often automatically added to the system PATH.

### Procedure

#### 1. Download the Release Files

Go to the [GitHub Releases page](https://github.com/HenkVanHoek/pi-server-vm/releases/latest) for this project.

Download the following files for the latest release:
-   `pi-master-template-vX.X.X.ova`
-   `create-master-vm-macos-amd64`
-   `clone-vm-macos-amd64`

#### 2. Make the Executables Runnable

By default, downloaded files are not marked as executable. You need to set the permission.

1.  Open the **Terminal** app.
2.  Navigate to your `Downloads` folder (or wherever you saved the files).
3.  Run the `chmod` command to add the execute permission:

        chmod +x create-master-vm-macos-amd64
        chmod +x clone-vm-macos-amd64

#### 3. Import the Master Template Appliance

You must first import the pre-built `.ova` file into VirtualBox. This will create the `pi-master-template` VM that the cloning script depends on.

1.  Open the VirtualBox application.
2.  Go to the menu **File -> Import Appliance...**
3.  Select the `pi-master-template-vX.X.X.ova` file you downloaded.
4.  Follow the on-screen prompts to complete the import.

#### 4. Run the Cloning Executable

Now you are ready to create your first clone.

1.  In your Terminal, from the same folder where you downloaded the files, run the `clone-vm` executable.
2.  Provide a name for your new VM and any optional parameters.

        # Example: Create a new VM named 'pi-test-macos'
        ./clone-vm-macos-amd64 pi-test-macos

        # Example: Create a more powerful VM and start it immediately
        ./clone-vm-macos-amd64 my-powerful-pi --ram 4096 --cpus 4 --start

Your new virtual Pi will be created and will appear in the VirtualBox Manager, ready to use.
