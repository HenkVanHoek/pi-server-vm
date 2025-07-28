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

## 🧪 Integration with PiSelfhosting

You can combine this with [`piselfhosting-vm-test`](https://github.com/your-org/piselfhosting-vm-test) to validate the deployment of services to simulated Raspberry Pi devices in CI or manual test environments.

---

## 📜 License

This project is licensed under the MIT License.
