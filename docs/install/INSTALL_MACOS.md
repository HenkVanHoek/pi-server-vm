# Installing on macOS

This guide will walk you through the installation and setup of the Pi-Server-VM tools on a macOS system.

## Prerequisites

Before you begin, please ensure you have the latest version of Oracle VirtualBox installed on your Mac. The Pi-Server-VM tools are designed to manage VirtualBox, so it must be present on your machine.

## Step 1: Download the Latest Release

Navigate to the project official releases page to find the latest version.

➡️ **[Download the latest release](https://github.com/HenkVanHoek/pi-server-vm/releases/latest)**

On the release page, find the "Assets" section and download the file named executables-macOS.tar.gz.

## Step 2: Extract the Archive

1.  Open the Terminal application.
2.  Navigate to the directory where you saved the downloaded file. For most users, this will be the Downloads directory.

        cd ~/Downloads

3.  Use the tar command to extract the contents of the archive.

        tar -xzvf executables-macOS.tar.gz

This will create a new directory named dist. Inside the dist directory, you will find a separate folder for each of the tools, for example, clone-vm and create-master-vm.

## Step 3: Authorize the Applications

Because this software is not downloaded from the Mac App Store, a macOS security feature called Gatekeeper will prevent it from running at first. You must perform a one-time action to tell macOS that you trust these tools.

1.  Make sure you are still in the same directory in your terminal (for example, the Downloads folder).
2.  Run the following commands for each of the tool folders you extracted. This command removes the quarantine attribute that macOS adds to downloaded files.

    For the clone-vm tool:

        xattr -cr dist/clone-vm

    For the create-master-vm tool:

        xattr -cr dist/create-master-vm

    For the web-app tool:

        xattr -cr dist/pi-selfhosting-web

After running these commands, you will be able to run the executables from inside each folder without any security warnings.

## Step 4: Add Tools to Your System PATH (Recommended)

For convenience, it is highly recommended to add the tool directories to your system PATH. This allows you to run commands like clone-vm from any location in your terminal without having to type the full path.

1.  Move the extracted dist folder to a more permanent location. A common choice is to place it in your home directory.

        mv dist ~/pi-server-vm-tools

2.  Open the configuration file for your shell in a text editor. On modern macOS versions, the default shell is Zsh, and the file is .zshrc.

        nano ~/.zshrc

3.  Add the following lines to the very end of the file. This tells your terminal where to find the new executables. Make sure to replace /Users/your-username with the actual path to your home directory.

        # Add Pi-Server-VM tools to the system PATH
        export PATH="$PATH:/Users/your-username/pi-server-vm-tools/clone-vm"
        export PATH="$PATH:/Users/your-username/pi-server-vm-tools/create-master-vm"
        export PATH="$PATH:/Users/your-username/pi-server-vm-tools/pi-selfhosting-web"

4.  Save the file and close the editor. For the changes to take effect, you can either close and reopen your terminal, or run the following command:

        source ~/.zshrc

You can now run the commands clone-vm, create-master-vm, and pi-selfhosting-web directly from your terminal.
