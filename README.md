# Pi Server VM

A set of cross-platform Python scripts to fully automate the creation and cloning of secure, minimal Debian virtual machines in **Oracle VirtualBox**. This project is designed to emulate a Raspberry Pi server environment, making it ideal for testing server software, network configurations, or any project designed for a Raspberry Pi without needing physical hardware.

## Features

- **Cross-Platform:** Works on Windows, macOS, and Linux without any configuration changes.
- **Fully Automated Creation:** Creates a new VirtualBox VM and dynamically downloads the latest stable Debian OS installer.
- **Idempotent "Golden Master":** The master template is self-healing and can be safely started and updated without breaking its ability to be cloned.
- **Intelligent Cloning:** Cloned VMs automatically configure a unique hostname on their first boot, making them distinct devices on your network.
- **Network Discoverable:** Clones announce themselves on the local network using Avahi (mDNS), appearing as **hostname.local**, just like a real Raspberry Pi.
- **User-Friendly Console:** The IP address of the VM is displayed on the console login screen for easy, immediate SSH access.
- **Secure by Default:** The template is configured with a locked root account and a standard user with **sudo** privileges whose password must be changed on first login.

## Downloads

For users who want to skip the manual installation, a ready-to-use virtual appliance (**ova** file) is available.

➡️ **[Download the latest release (v1.3.1)](https://github.com/HenkVanHoek/pi-server-vm/releases/latest)**

After downloading, import the appliance using the **File -> Import Appliance** menu in VirtualBox.

**Default Credentials:**
- **Username:** pivm
- **Password:** PivmPwd (You will be forced to change this on first login).

## Quick Start

1.  **Download** the latest `.ova` appliance and the executable for your operating system from the [**GitHub Releases page**](https://github.com/HenkVanHoek/pi-server-vm/releases/latest).
2.  **Import** the `.ova` file into VirtualBox.
3.  **Run** the `clone-vm` executable from your terminal to create a new virtual machine.

        # Example:
        ./clone-vm-executable-name my-first-pi --ram 2048 --start

For detailed, step-by-step instructions for your specific operating system, please see the guides below:

-   ➡️ **[Installation Guide for Windows](./docs/INSTALL_WINDOWS.md)**
-   ➡️ **[Installation Guide for macOS](./docs/INSTALL_MACOS.md)**
-   ➡️ **[Installation Guide for Linux](./docs/INSTALL_LINUX.md)**

## Scope and Limitations

It is important to understand what this project is designed for and what its limitations are.

### CPU Emulation vs. Allocation

The virtual machines created by this project run on the **x86-64 architecture** of your host computer, not the **ARM architecture** of a physical Raspberry Pi.

When you specify the number of CPUs (e.g., `--cpus 4`), you are **allocating host CPU cores** to the VM. This is excellent for simulating the **multicore** environment of a modern Raspberry Pi to test the performance of **multithreaded** server applications.

However, this setup cannot run software that is compiled exclusively for the ARM architecture.

### Real-Time Processing

This virtual environment is **not suitable for hard real-time applications**. Real-time processing requires precise, deterministic timing guarantees that are impossible to achieve through the multiple layers of software (Host OS, VirtualBox, Guest OS) involved in virtualization.

This project is intended for testing server-side applications, web services, and other software that does not rely on microsecond-precision timing or direct hardware access (like GPIO pins).

## Verifying the VM Configuration

(The verification section we wrote earlier can go here)

## Contributing

We welcome contributions! Please see the **CONTRIBUTING.md** file for details on how to get started, report bugs, and submit changes.

## Support This Project

If you find this project useful and would like to help support its continued development, please consider becoming a sponsor. Your support is greatly appreciated!

➡️ **[Sponsor @HenkVanHoek on GitHub](https://github.com/sponsors/HenkVanHoek)**
