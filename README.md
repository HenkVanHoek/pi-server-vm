# Pi Server VM

A set of cross-platform Python scripts to fully automate the creation and cloning of secure, minimal Debian virtual machines in **Oracle VirtualBox**. This project is designed to emulate a Raspberry Pi server environment, making it ideal for testing server software, network configurations, or any project designed for a Raspberry Pi without needing physical hardware.

## Features

- **Cross-Platform:** The tools work on Windows, macOS, and Linux.
- **LAN Accessible:** Creates virtual machines as full citizens on your local network, discoverable and accessible from any other computer.
- **Idempotent "Golden Master":** The master template is self-healing and can be safely started and updated without breaking the cloning process.
- **Intelligent & Configurable Cloning:** Cloned VMs automatically configure a unique hostname on first boot. Optional command-line flags allow customization of RAM, CPUs, secondary disks, username, and password.
- **Network Discoverable:** Clones announce themselves on the local network using Avahi (mDNS), appearing as **hostname.local**, just like a real Raspberry Pi.
- **User-Friendly Console:** The IP address of the VM is displayed on the console login screen for easy, immediate SSH access.
- **Secure by Default:** The template is configured with a locked root account and a standard user with **sudo** privileges whose password must be changed on first login (if not set during cloning).

## Downloads

For users who want to skip the manual installation, a ready-to-use virtual appliance (**ova** file) is available.

➡️ **[Download the latest release (v1.4.0)](https://github.com/HenkVanHoek/pi-server-vm/releases/latest)**

## Quick Start & Usage

This project provides executables for easy use. For detailed, step-by-step instructions for your specific operating system, please see the guides below. These guides are the recommended starting point.

-   ➡️ **[Installation Guide for Windows](INSTALL_WINDOWS.md)**
-   ➡️ **[Installation Guide for macOS](INSTALL_MACOS.md)**
-   ➡️ **[Installation Guide for Linux](INSTALL_LINUX.md)**

## Scope and Limitations

It is important to understand what this project is designed for and what its limitations are.

### CPU Emulation vs. Allocation
The virtual machines run on the **x86-64 architecture** of your host computer, not the **ARM architecture** of a physical Raspberry Pi. This is excellent for testing the performance of **multithreaded** server applications in a **multicore** environment, but it cannot run software that is compiled exclusively for ARM.

### Real-Time Processing
This virtual environment is **not suitable for hard real-time applications** that require microsecond-precision timing or direct hardware access like GPIO pins.

## Contributing
We welcome contributions! Please see the **CONTRIBUTING.md** file for details on how to get started, report bugs, and submit changes.

## Support This Project
If you find this project useful and would like to help support its continued development, please consider becoming a sponsor. Your support is greatly appreciated!

➡️ **[Sponsor @HenkVanHoek on GitHub](https://github.com/sponsors/HenkVanHoek)**
