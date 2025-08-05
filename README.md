# Pi Server VM

Python scripts to automate the creation and cloning of Raspberry Pi virtual machine templates in VirtualBox. This project simplifies setting up multiple, consistent Debian-based VMs for development and testing.

## Features

-   **`create_master_vm.py`**: A script to automate the creation of a base Debian VM template (`pi-master-template`). It handles unattended installation, configures SSH, and installs VirtualBox Guest Additions.
-   **`clone_vm.py`**: A powerful, cross-platform script to clone the master template. Customize the name of the new VM, RAM, CPUs, add a secondary disk, and set the default user/password, all from the command line.
-   **Cross-Platform**: Designed to work on Windows, macOS, and Linux.

## Requirements

-   **Python 3.8+**
-   **Oracle VirtualBox**: The scripts rely on the `VBoxManage` command-line interface. Ensure VirtualBox is installed and `VBoxManage` is in the system PATH.
-   **Debian Netinstall ISO**: A network installation image for Debian is required for creating the master template.

## Installation

1.  **Clone the repository:**

    git clone https://github.com/HenkVanHoek/pi-server-vm.git
    cd pi-server-vm

2.  **Set up a virtual environment (recommended):**

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3.  **Install the package in editable mode with development dependencies:**

    pip install -e .[dev]

## Usage

### 1. Create the Master VM Template

First, create the base template. You will need a Debian netinstall ISO.

    python scripts/create_master_vm.py /path/to/your/debian-12-netinst.iso

### 2. Clone the Master VM

Once the `pi-master-template` exists, you can clone it to create new VMs.

**Basic clone:**

    python scripts/clone_vm.py my-new-vm

**Clone with customizations:**

    python scripts/clone_vm.py my-powerful-vm \
        --ram 4096 \
        --cpus 4 \
        --disk-size 32 \
        --user myuser \
        --password mypassword \
        --start

## Building the Executables

This project uses PyInstaller to create standalone executables. A simple build script is provided to automate the process.

1.  **Ensure you have installed the development dependencies:**

    pip install -e .[dev]

2.  **Run the build script:**

    python build.py

The final executables will be placed in the `dist/` directory.

## Using the Pre-compiled Executables

For users who do not have a Python environment, pre-compiled executables are available. These tools allow you to manage VMs without any programming knowledge.

### Prerequisites

**You MUST have Oracle VirtualBox installed on your system.**

The scripts depend on the `VBoxManage` command-line tool that is included with VirtualBox. The executable will automatically search for it in the system PATH and in the default VirtualBox installation directory.

-   Download VirtualBox: [https://www.virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
