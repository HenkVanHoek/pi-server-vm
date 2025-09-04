# Pi Server VM

The Pi-Server VM provides a virtual machine (VM) specifically designed for testing the PiSelfhosting project and its services. It’s a universal testing platform, capable of running on a diverse range of hardware – from the Raspberry Pi 5 to powerful systems supporting demanding applications like Nextcloud with multiple camera streams (e.g., for NVR systems), Jellyfin, Plex, GitLab runners, and Home Assistant. **In my home setup, the Raspberry Pi 5 with 8GB of RAM and a 1TB M2 SSD was perfectly capable of running Home Assistant, Frigate with 4 cameras and person detection, and Nextcloud – even with the Google TPU – demonstrating the project’s versatility.**

The PiSelfhosting project was conceived with a focus on simplicity and flexibility. Recognizing the potential complexity of managing numerous services, the initial design leveraged Docker to isolate each component – Nextcloud, Jellyfin, Plex, Frigate, and more – within its own environment. This approach eliminated dependency conflicts and simplified troubleshooting.

    graph TD
        A["User runs create-master-vm tool"] --> B["pi-master-template VM is created in VirtualBox"];
        B --> C["User runs clone-vm tool"];
        C --> D["New Clone VM (e.g., 'my-dev-pi') is created"];
        D --> E["Clone boots for the first time"];
        E --> F["First-boot service runs, sets unique hostname & identity"];
        F --> G["Clone is ready on the network at my-dev-pi.local"];

## Features

This project provides a complete ecosystem for virtual machine management, from creation to deployment.

#### Core Functionality
- **Automated Master Template Creation:** A command-line tool, **create-master-vm**, that downloads the latest Debian ISO and builds a "golden master" VM template from scratch.
- **One-Command Cloning:** A tool, **clone-vm**, to create new, independent development VMs from the master template in seconds.
- **Web UI for VM Creation:** A simple web interface to create and customize new clone VMs directly from your browser, without needing to use the command line.

#### Professional User Experience
- **Professional Windows Installer:** A single, easy-to-use **setup.exe** for a one-click setup on Windows, complete with Start Menu shortcuts.
- **Pre-Built Virtual Appliance:** A ready-to-import **.ova** file is included in each release, allowing users on any platform to get started instantly without building the template themselves.
- **Cross-Platform Tools:** All command-line tools are provided as standalone executables for Windows, macOS, and Linux.

#### VM & Network Features
- **LAN Accessible:** Cloned VMs are configured as full citizens on your local network, discoverable and accessible from any other computer.
- **Network Discovery (mDNS):** Clones announce themselves on the network using Avahi, appearing as **hostname.local**, just like a real Raspberry Pi.
- **User-Friendly Console:** The IP address of the VM is displayed directly on the console login screen for immediate, easy SSH access.
- **Secure by Default:** The master template is configured with a locked root account and a standard user with **sudo** privileges.
- **Ecosystem Integration:** Each clone is automatically provisioned with a unique identity file at **/etc/piselfhosting-virtual-pi-server**. This file contains the model name, a unique serial number, and the hostname, allowing for easy discovery and management by other tools in the PiSelfhosting ecosystem, such as the **pi-scanner**.

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
## Glossary of Terms & Technologies

This project sits at the intersection of several different technologies. This glossary explains the key terms and tools used.

### Core Project Components
*   **Raspberry Pi OS:** The official, Debian-based operating system for the Raspberry Pi single-board computer. While this project does not use Raspberry Pi OS directly, its primary goal is to **emulate** a minimal, headless server environment that behaves just like a fresh installation of Raspberry Pi OS Lite.
*   **Debian:** A robust and stable Linux distribution. We use the official Debian "netinst" image as the base for our virtual machines because it is the direct ancestor of Raspberry Pi OS and provides a clean, minimal foundation.
*   **Pi-Server-VM:** This project. A collection of tools for creating and managing virtual machines for testing server software.
*   **PiSelfhosting:** The parent project. A suite of self-hosted services (like Nextcloud, Home Assistant) designed to run on low-power hardware like a Raspberry Pi, typically using Docker.
*   **pi-scanner:** A tool from the PiSelfhosting ecosystem that scans the local network to discover running Pi servers and virtual machines.

### Virtualization

*   **VirtualBox:** A free and open-source virtualization software from Oracle. It allows you to run entire operating systems (like Debian Linux) as "guest" machines inside your main "host" operating system (like Windows).
*   **VM (Virtual Machine):** A complete, self-contained computer system that is emulated in software.
*   **.ova (Open Virtual Appliance):** A standard file format for packaging and distributing a complete, pre-configured virtual machine. The `.ova` files from this project can be easily imported into VirtualBox.

### Development & Build Tools

*   **PyInstaller:** A tool that bundles a Python application and all its dependencies into a single, standalone executable (`.exe` on Windows) that can be run on a computer without Python installed.
*   **Inno Setup:** A free tool for creating professional, user-friendly `setup.exe` installers for Windows applications.
*   **uv:** A modern, extremely fast Python package installer and resolver, used in this project's development and build process.
*   **bump-my-version:** A command-line tool that automates the process of incrementing version numbers in project files.
*   **GitHub Actions:** The continuous integration and continuous delivery (CI/CD) platform provided by GitHub. This project uses it to automatically build the executables for Windows, macOS, and Linux whenever a new version is released.
*   **Docker:** A platform for building and running applications in isolated environments called containers. This is the core technology used by the parent **PiSelfhosting** project.

### Networking

*   **mDNS (Multicast DNS):** A zero-configuration networking protocol that allows devices to discover each other on a local network without a central DNS server. This is what allows you to access your VMs at an address like **hostname.local**.
*   **Avahi:** The specific software service running inside the Debian VMs that implements mDNS.
## Contributing
We welcome contributions! Please see the **[CONTRIBUTING.md](CONTRIBUTING.md)** file for details on how to get started, report bugs, and submit changes.

## Support This Project
If you find this project useful, please consider becoming a sponsor. Your support is greatly appreciated!

➡️ **[Sponsor @HenkVanHoek on GitHub](https://github.com/sponsors/HenkVanHoek)**
