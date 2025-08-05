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

➡️ **[Download the latest release (v1.2.0)](https://github.com/HenkVanHoek/pi-server-vm/releases/latest)**

After downloading, import the appliance using the **File -> Import Appliance** menu in VirtualBox.

**Default Credentials:**
- **Username:** `pivm`
- **Password:** `PivmPwd` (You will be forced to change this on first login).

## Usage

### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/)
- [VirtualBox 7.x](https://www.virtualbox.org/wiki/Downloads)
- Required Python packages:

    pip install requests flask

### 1. Create the Master Template

This only needs to be done once. The script will download the Debian installer and create the `pi-master-template` VM.

    python -m scripts.create_master_vm

A new VM window will open. Follow the on-screen instructions to complete the manual part of the Debian installation. A detailed guide with screenshots is available in `INSTALLATION_GUIDE.md`.

### 2. Clone a VM

Once the master template is ready, you can create as many unique clones as you need using either the command line or the new web interface.

#### Option A: Using the Command Line
This method is ideal for scripting and automation. All arguments (`--ram`, `--cpus`, `--disk-size`) are optional.

    # Example: Create a new VM named 'pi-web-server'
    python -m scripts.clone_vm pi-web-server

Start your new VM from the VirtualBox Manager. It will automatically configure itself with the new hostname on its first boot.

#### Option B: Using the Web Interface
This method provides a user-friendly graphical interface for cloning.

**1. Start the web server:**
Navigate to the project root directory in your terminal and run the following command:

    python -m webapp.app

**2. Open your browser:**
Navigate to `http://127.0.0.1:5000`.

You will see a web form where you can enter the name and optional specifications for your new VM. The results of the clone operation will be displayed on the page.

## Understanding the Network Configuration

To ensure reliability and prevent conflicts, the virtual machines created by this project use a **two-adapter network configuration**.

#### Adapter 1: NAT (Internet Access)

-   **Purpose:** This adapter connects the VM to the internet through a private, virtual router inside VirtualBox.
-   **Function:** It allows the VM to download software and updates (e.g., using `apt`). The IP address on this adapter (usually `10.0.2.15`) is **not reachable** from your local network.

#### Adapter 2: Host-Only (Management & Discovery)

-   **Purpose:** This adapter connects the VM to a private, stable network that exists **only between your computer (the host) and your VMs.**
-   **Function:** This is the interface used for management tasks like SSH and for discovery by other tools.
-   **IP Range:** The VMs will get a stable IP address in the `192.168.56.0/24` range by default.

### How to Find Your Virtual Pis

Because the VMs live on this separate Host-Only network, you must scan that specific network to discover them. A standard network scan of your main home network (e.g., `192.168.178.0/24`) will **not** find them.

**Example using `nmap`:**

To discover all running virtual Pi VMs, run the following command from your host machine:

    nmap -Pn 192.168.56.0/24

This command will scan the Host-Only network and report all the virtual machines that are currently running, allowing you to find their IP addresses for SSH or for use with management tools like `PiSelfhosting`.
## Verifying the VM Configuration

After you have created the `pi-master-template`, you can verify that the custom MAC address and unique serial number were assigned correctly.

#### Method 1: Using the VirtualBox GUI (Easiest)

1.  Open the VirtualBox Manager.
2.  Select the `pi-master-template` VM from the list.
3.  Click on **Settings**.

**To Check the MAC Address:**
- Navigate to the **Network** section.
- Select the **Adapter 1** tab.
- Click **Advanced** to expand the details.
- The **MAC Address** field will display the value. Verify that it begins with a Raspberry Pi prefix (e.g., `DCA632...` or `B827EB...`).

**To Check the Serial Number:**
- Navigate to the **General** section.
- Select the **Basic** tab.
- The **Description** field will contain the custom serial number, prefixed with `serial:`.

#### Method 2: Using the Command Line

Open your Windows Command Prompt (cmd) or PowerShell and use the following commands.

**To Check the MAC Address:**

    VBoxManage showvminfo pi-master-template | findstr "MAC"

*Expected output:*

    NIC 1:           MAC: DCA632A1B2C3, ...

**To Check the Serial Number:**

    VBoxManage showvminfo pi-master-template | findstr "serial"

*Expected output:*

    Description:     serial:1a2b3c4d5e6f7890
## Contributing

We welcome contributions! Please see the `CONTRIBUTING.md` file for details on how to get started, report bugs, and submit changes.
