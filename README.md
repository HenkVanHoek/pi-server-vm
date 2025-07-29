# pi-server-vm

A virtual Raspberry Pi lab environment for automated testing and deployment of containerized services — designed to behave like real Pi devices on the network.

🍀 **About**  
`pi-server-vm` is a toolset and framework to simulate realistic Raspberry Pi devices using VirtualBox VMs. It was created to support [PiSelfhosting](https://github.com/hvhoek/piselfhosting), an open source platform for managing and deploying Docker-based services across multiple Raspberry Pi systems.

Because real Pi devices can be slow to test, manage, or replicate, this project uses Debian-based VMs that mimic real Raspberry Pis on a network. This includes:

- Simulated Raspberry Pi MAC address OUIs  
- Consistent virtual serial numbers  
- Realistic network behavior using Bridge Mode  
- Easily reproducible and scriptable VM templates  
- Designed for manual use, Python-driven automation, and CI-based testing  

🛠️ **Project Structure**  
This project is designed in two layers:

- `pi-server-vm`: Provides generic Pi-like VMs for local network simulation.  
- `piselfhosting-vm-test`: Adds logic to test [PiSelfhosting](https://github.com/hvhoek/piselfhosting) installation and services on the PiVMs.

---

## 🚀 Setup (Quick Start)

1. **Clone the repo:**

   ```bash
   git clone https://github.com/your-org/pi-server-vm.git
   cd pi-server-vm
   ```

2. **Build master VM template:**

   ```bash
   python scripts/create_master_vm.py
   ```

   This sets up the base Debian VM in Bridge Mode with required configuration.

3. **Create a new PiVM clone:**

   ```bash
   python scripts/create_pivm.py --name pivm-1
   ```

   This clones the master VM and assigns it a simulated Raspberry Pi MAC address and virtual serial number.

4. **Start the VM:**

   You can start the VM manually in VirtualBox, or via:

   ```bash
   VBoxManage startvm pivm-1 --type headless
   ```

---

## 📁 Folder Structure

```
pi-server-vm/
├── scripts/                # Python scripts for VM automation
├── vm_templates/           # Base VM image configurations
├── docs/                   # Optional documentation files
└── README.md
```

---
## Installation Guide for the Master Template

This guide walks through the manual steps required to install Debian on the `pi-master-template` virtual machine.

### 1. Initial Setup

The script will automatically start the VM, and the Debian installer will boot. Proceed through the initial screens for:
- Language
- Location
- Keyboard Layout
- Network Configuration (should be automatic)
- Hostname (e.g., `pi-master-template`)
- Domain Name (can be left blank)
- Root Password (set a strong password)
- User Creation (create a user and password)

### 2. Disk Partitioning

When you reach the "Partition disks" step, follow this guided process. These choices will erase the virtual disk and set up a standard layout.

**Step 1: Choose Guided Method**  
Select **Guided - use entire disk**.
> ![Choose Guided Partitioning](docs/images/VirtualBox_pi-master-template-partition-disks.png)

**Step 2: Select the Disk**  
Select the only disk available, which will be the `VBOX HARDDISK`.
> ![Select VirtualBox Hard Disk](docs/images/VirtualBox_pi-master-template-partition-disks-2.png)

**Step 3: Choose Partitioning Scheme**  
For simplicity, select **All files in one partition**.
> ![Choose All Files in One Partition](docs/images/VirtualBox_pi-master-template-partition-disks-3.png)

**Step 4: Finish and Write Changes**  
Review the proposed layout and select **Finish partitioning and write changes to disk**. Then, confirm **<Yes>** on the final confirmation screen to proceed.
> ![Finish Partitioning and Write Changes](docs/images/VirtualBox_pi-master-template-partition-disks-4.png)

### 3. Software Selection (Critical Step)

This is the most important step for creating a minimal server. On the "Software selection" screen, ensure your choices match the image below. Use the spacebar to select/deselect items.

- **UNCHECK** `[ ] Debian desktop environment`
- **CHECK** `[X] SSH server`
- **CHECK** `[X] standard system utilities`

> ![Debian Software Selection for a minimal server](docs/images/VirtualBox_pi-master-template-software-selection.png)

### 4. GRUB Boot Loader Installation (Critical Step)

The GRUB boot loader allows the virtual machine to start.

**Step 1: Install GRUB**  
When asked to "Install the GRUB boot loader to the primary drive?", you must select **<Yes>**.
> ![Confirm GRUB Installation](docs/images/VirtualBox_pi-master-template-configure-grub-pc.png)

**Step 2: Select the Boot Device**  
This is crucial. Do not choose "Enter device manually". You must select the virtual hard disk, which will be listed as `/dev/sda`.
> ![Select /dev/sda for GRUB](docs/images/VirtualBox_pi-master-template-configure-grub-pc-3.png)

### 5. Finalizing the Installation

The installation will now complete. When you see the "Installation complete" message, you can select **<Continue>**. The virtual machine will reboot and then shut down (as it ejects the installation media).

Your `pi-master-template` is now ready! You can take a snapshot of it in VirtualBox to preserve its clean state before cloning.

### Verifying the VM Configuration

After you have created the `pi-master-template`, you can verify that the custom MAC address and unique serial number were assigned correctly.

There are two primary ways to check these settings: through the VirtualBox graphical user interface or via the command line.

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
## 🧪 Integration with PiSelfhosting

You can combine this with [`piselfhosting-vm-test`](https://github.com/your-org/piselfhosting-vm-test) to validate the deployment of services to simulated Raspberry Pi devices in CI or manual test environments.

---

## 📜 License

This project is licensed under the MIT License.
