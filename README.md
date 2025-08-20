# Pi Server VM

A set of cross-platform tools to fully automate the creation and management of secure, minimal Debian virtual machines in **Oracle VirtualBox**. This project is designed to emulate a Raspberry Pi server environment, making it ideal for testing server software, network configurations, or any project designed for a headless server without needing physical hardware.

## Features

This project provides a complete ecosystem for virtual machine management, from creation to deployment.

#### Core Functionality
- **Automated Master Template Creation:** A command-line tool, create-master-vm, that downloads the latest Debian ISO and builds a "golden master" VM template from scratch.
- **One-Command Cloning:** A tool, clone-vm, to create new, independent development VMs from the master template in seconds.
- **Web UI for VM Creation:** A simple web interface to create and customize new clone VMs directly from your browser, without needing to use the command line.

#### Professional User Experience
- **Professional Windows Installer:** A single, easy-to-use setup.exe for a one-click setup on Windows, complete with Start Menu shortcuts.
- **Pre-Built Virtual Appliance:** A ready-to-import .ova file is included in each release, allowing users on any platform to get started instantly without building the template themselves.
- **Cross-Platform Tools:** All command-line tools are provided as standalone executables for Windows, macOS, and Linux.

#### VM & Network Features
- **LAN Accessible:** Cloned VMs are configured as full citizens on your local network, discoverable and accessible from any other computer.
- **Network Discovery (mDNS):** Clones announce themselves on the network using Avahi, appearing as hostname.local, just like a real Raspberry Pi.
- **User-Friendly Console:** The IP address of the VM is displayed directly on the console login screen for immediate, easy SSH access.
- **Secure by Default:** The master template is configured with a locked root account and a standard user with **sudo** privileges.

---

## Installation

### Windows (Recommended)

For the easiest and most reliable setup, use the provided installer.

1.  Navigate to the **[latest release page](https://github.com/HenkVanHoek/pi-server-vm/releases/latest)**.
2.  Under the "Assets" section, download the installer, which will be named pi-server-vm-setup-vX.X.X.exe.
3.  Run the downloaded setup.exe and follow the on-screen instructions.

> **Note on Security Warnings:** The Windows installer is not yet digitally code-signed. Therefore, you may see a security warning from Windows Defender SmartScreen when you run it. Please click **"More info"** and then **"Run anyway"** to proceed with the installation. The executables are built transparently via our public GitHub Actions workflow for your security.

### macOS & Linux

1.  Navigate to the **[latest release page](https://github.com/HenkVanHoek/pi-server-vm/releases/latest)**.
2.  Download the appropriate archive for your OS (executables-macOS.tar.gz or executables-Linux.tar.gz).
3.  Extract the archive. This will create a folder for each tool.
4.  It is recommended to move these tool folders to a convenient location and add their parent directory to your system PATH for easy access.

---

## Quick Start & Usage

For detailed, step-by-step instructions for your specific operating system, including how to handle potential anti-virus warnings, please see the full guides:

-   ➡️ **[Installation Guide for Windows](INSTALL_WINDOWS.md)**
-   ➡️ **[Installation Guide for macOS](INSTALL_MACOS.md)**
-   ➡️ **[Installation Guide for Linux](INSTALL_LINUX.md)**

---

## Compatibility

The pre-built executables are tested to run on the following operating systems or newer:

*   **Windows:** Windows 10
*   **macOS:** macOS 10.15 (Catalina)
*   **Linux:** Ubuntu 22.04 (glibc 2.35)

---

## Scope and Limitations

It is important to understand what this project is designed for and what its limitations are.

*   **CPU Architecture:** The virtual machines run on the **x86-64 architecture** of your host computer, not the **ARM architecture** of a physical Raspberry Pi. This is excellent for testing multi-threaded server applications but cannot run software compiled exclusively for ARM.
*   **Real-Time Processing:** This virtual environment is **not suitable for hard real-time applications** that require microsecond-precision timing or direct hardware access like GPIO pins.

---

## Contributing
We welcome contributions! Please see the **[CONTRIBUTING.md](CONTRIBUTING.md)** file for details on how to get started, report bugs, and submit changes.

## Support This Project
If you find this project useful, please consider becoming a sponsor. Your support is greatly appreciated!

➡️ **[Sponsor @HenkVanHoek on GitHub](https://github.com/sponsors/HenkVanHoek)**
