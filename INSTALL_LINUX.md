## Installation and Usage on Linux (Ubuntu Desktop)

This guide provides instructions for using the `pi-server-vm` executables on a Linux system, such as Ubuntu Desktop.

### Prerequisites

Before you begin, ensure your system is up to date and has the necessary software installed.

#### 1. Update Your System

Open a terminal and run the following commands to update your package lists and installed packages:

    sudo apt update
    sudo apt upgrade -y

#### 2. Install VirtualBox

The scripts rely on the `VBoxManage` command-line tool, which is part of the main VirtualBox package.

    sudo apt install virtualbox -y

#### 3. Install VirtualBox Guest Additions (Required for VM Features)

For the cloned VMs to function correctly (especially for automatic hostname configuration), you need the Guest Additions CD image available.

    sudo apt install virtualbox-guest-additions-iso -y

#### 4. Add Your User to the `vboxusers` Group

To run VirtualBox and its command-line tools without needing `sudo` for every command, you must add your user account to the `vboxusers` group.

    # Replace 'your-username' with your actual Ubuntu username
    sudo adduser your-username vboxusers

**IMPORTANT:** You must **log out and log back in** (or fully reboot your computer) for this group change to take effect.

### Procedure

#### 1. Download the Release Files

Go to the [GitHub Releases page](https://github.com/HenkVanHoek/pi-server-vm/releases/latest) for this project.

Download the following files for the latest release:
-   `pi-master-template-vX.X.X.ova`
-   `create-master-vm-linux-amd64`
-   `clone-vm-linux-amd64`

#### 2. Make the Executables Runnable

By default, downloaded files are not marked as executable. You need to set the permission.

1.  Open your terminal and navigate to your `Downloads` folder (or wherever you saved the files).
2.  Run the `chmod` command to add the execute permission:

        chmod +x create-master-vm-linux-amd64
        chmod +x clone-vm-linux-amd64

#### 3. Import the Master Template Appliance

You must first import the pre-built `.ova` file into VirtualBox. This will create the `pi-master-template` VM that the cloning script depends on.

1.  Open the VirtualBox application.
2.  Go to the menu **File -> Import Appliance...**
3.  Select the `pi-master-template-vX.X.X.ova` file you downloaded.
4.  Follow the on-screen prompts to complete the import.

#### 4. Run the Cloning Executable

Now you are ready to create your first clone.

1.  In your terminal, from the same folder where you downloaded the files, run the `clone-vm` executable.
2.  Provide a name for your new VM and any optional parameters.

        # Example: Create a new VM named 'pi-test-linux'
        ./clone-vm-linux-amd64 pi-test-linux

        # Example: Create a more powerful VM and start it immediately
        ./clone-vm-linux-amd64 my-powerful-pi --ram 4096 --cpus 4 --start

Your new virtual Pi will be created and will appear in the VirtualBox Manager, ready to use.
