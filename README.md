# Pi Server VM

A set of cross-platform Python scripts to fully automate the creation and cloning of secure, minimal Debian virtual machines in **Oracle VirtualBox**. This project is designed to emulate a Raspberry Pi server environment, making it ideal for testing server software, network configurations, or any project designed for a Raspberry Pi without needing physical hardware.
This project allows you to quickly provision new, unique VM instances from a "golden master" template, making it ideal for testing server software, network configurations, or any project designed for a Raspberry Pi environment.

## Features

- **Cross-Platform:** Works on Windows, macOS, and Linux without any configuration changes.
- **Fully Automated Creation:** Creates a new VirtualBox VM and dynamically downloads the latest stable Debian OS installer.
- **Idempotent "Golden Master":** The master template is self-healing and can be safely started and updated without breaking its ability to be cloned.
- **Intelligent Cloning:** Cloned VMs automatically configure a unique hostname on their first boot, making them distinct devices on your network.
- **Network Discoverable:** Clones announce themselves on the local network using Avahi (mDNS), appearing as `hostname.local`, just like a real Raspberry Pi.
- **User-Friendly Console:** The IP address of the VM is displayed on the console login screen for easy, immediate SSH access.
- **Secure by Default:** The template is configured with a locked root account and a standard user with `sudo` privileges whose password must be changed on first login.

## Scope and Limitations

It is important to understand what this project is designed for and what its limitations are.

### CPU Emulation vs. Allocation

The virtual machines created by this project run on the **x86-64 architecture** of your host computer, not the **ARM architecture** of a physical Raspberry Pi.

When you specify the number of CPUs (e.g., `--cpus 4`), you are **allocating host CPU cores** to the VM. This is excellent for simulating the multicore environment of a modern Raspberry Pi to test the performance of multithreaded server applications.

However, this setup cannot run software that is compiled exclusively for the ARM architecture.

### Real-Time Processing

This virtual environment is **not suitable for hard real-time applications**. Real-time processing requires precise, deterministic timing guarantees that are impossible to achieve through the multiple layers of software (Host OS, VirtualBox, Guest OS) involved in virtualization.

This project is intended for testing server-side applications, web services, and other software that does not rely on microsecond-precision timing or direct hardware access (like GPIO pins).
## Downloads

For users who want to skip the manual installation, a ready-to-use virtual appliance (`.ova` file) is available.

➡️ **[Download the latest release (v1.1.0)](https://github.com/HenkVanHoek/pi-server-vm/releases/latest)**

After downloading, import the appliance using the **File -> Import Appliance** menu in VirtualBox.

**Default Credentials:**
- **Username:** `pivm`
- **Password:** `PivmPwd` (You will be forced to change this on first login).

## Usage

### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/)
- [VirtualBox 7.x](https://www.virtualbox.org/wiki/Downloads)
- Required Python packages:

    pip install requests

### 1. Create the Master Template

This only needs to be done once. The script will download the Debian installer and create the `pi-master-template` VM.

    python scripts/create_master_vm.py

A new VM window will open. Follow the on-screen instructions to complete the manual part of the Debian installation. A detailed guide with screenshots is available in `INSTALLATION_GUIDE.md`.

### 2. Clone the Master Template

Once the master template is ready, you can create as many unique clones as you need.

    # Example: Create a new VM named 'pi-web-server'
    python scripts/clone_vm.py pi-web-server

Start your new VM from the VirtualBox Manager. It will automatically configure itself with the new hostname on its first boot.

## Verifying the VM Configuration

(The verification section we wrote earlier can go here)

## Contributing

We welcome contributions! Please see the `CONTRIBUTING.md` file for details on how to get started, report bugs, and submit changes.
