# Installation and Usage on Linux (Ubuntu Desktop)

This guide provides instructions for using the `pi-server-vm` executables on a Linux system, such as Ubuntu Desktop.

### Prerequisites

#### 1. Update Your System

Open a terminal and run the following commands to update your package lists and installed packages:

    sudo apt update
    sudo apt upgrade -y

#### 2. Install VirtualBox & Required Components

Install VirtualBox, the Guest Additions ISO, and ensure your user is in the correct group.

    sudo apt install virtualbox virtualbox-guest-additions-iso -y

    # Replace 'your-username' with your actual Ubuntu username
    sudo adduser your-username vboxusers

**IMPORTANT:** You must **log out and log back in** for the group change to take effect.

#### 3. Configure VirtualBox Networking (One-Time Setup)

The virtual machines require a private network for management and discovery. This "Host-Only Network" is not created by default and must be set up once.

1.  Open the **VirtualBox** application.
2.  Go to the main menu: **File -> Tools -> Network Manager**.
3.  Select the **Host-only Networks** tab.
4.  Click the **Create** button.
5.  A new network (e.g., 'vboxnet0') will appear. Select it.
6.  Ensure the **DHCP Server** is enabled for this network. You can check this on the "DHCP Server" tab and click "Apply" if you make changes. The default IP settings are fine.

Your system is now ready to host the virtual machines.

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

    This will create a new folder containing the `create-master-vm` and `clone-vm` tools, which will already be executable.

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

Your new virtual Pi will be created and will appear in the VirtualBox Manager, ready to use.
