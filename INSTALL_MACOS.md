# Installation and Usage on macOS

This guide provides instructions for using the `pi-server-vm` executables on a macOS system.

### Prerequisites

#### 1. Install VirtualBox

The scripts rely on the `VBoxManage` command-line tool. Download and install the latest version of VirtualBox for macOS from the official website.

- **[Download VirtualBox](https://www.virtualbox.org/wiki/Downloads)**

During installation, you may be prompted to allow kernel extensions in your "System Settings -> Privacy & Security". Please approve this for VirtualBox to function correctly.

#### 2. Configure VirtualBox Networking (One-Time Setup)

The virtual machines require a private network for management and discovery. This "Host-Only Network" must be created once.

1.  Open the **VirtualBox** application from your `/Applications` folder.
2.  Go to the main menu: **Tools -> Network Manager**.
3.  Select the **Host-only Networks** tab. If this is a fresh installation, this list will be empty.
4.  Click the **Create** button.
5.  A new network adapter will appear, likely named **"vboxnet0"**. Select it.
6.  Ensure the **DHCP Server** is enabled for this network. Click on the "DHCP Server" tab on the right, check the **"Enable Server"** box, and click **"Apply"**. The default IP settings (e.g., `192.168.56.x`) are perfectly fine.

Your system is now ready to host the virtual machines.

### Procedure

#### 1. Download the Release Files

Go to the [GitHub Releases page](https://github.com/HenkVanHoek/pi-server-vm/releases/latest) for this project.

You will need to download **two** files for the latest release:
-   `pi-master-template-vX.X.X.ova` (The virtual machine template)
-   `executables-macOS.tar.gz` (The command-line tools)

#### 2. Extract the Executables

1.  Open the **Terminal** app.
2.  Navigate to your `Downloads` folder.
3.  Run the `tar` command to extract the archive:

        tar -xvzf executables-macOS.tar.gz

    This will create a new folder containing the `create-master-vm` and `clone-vm` tools, which will already be executable.

#### 3. Import the Master Template Appliance

You must first import the pre-built `.ova` file into VirtualBox.

1.  Open the VirtualBox application.
2.  Go to the menu **File -> Import Appliance...**
3.  Select the `pi-master-template-vX.X.X.ova` file you downloaded.
4.  Follow the on-screen prompts to complete the import. When reviewing the settings, ensure that **Adapter 2** is correctly assigned to the "Host-only Adapter" (`vboxnet0`) you just created.

#### 4. Run the Cloning Executable

Now you are ready to create your first clone.

1.  In your Terminal, navigate into the folder where you extracted the executables.
2.  Run the `clone-vm` executable, providing a name for your new VM and any optional parameters.

        # Example: Create a new VM named 'pi-test-macos'
        ./clone-vm pi-test-macos

Your new virtual Pi will be created and will appear in the VirtualBox Manager.
