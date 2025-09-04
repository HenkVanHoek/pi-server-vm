# Welcome to the Pi-Server-VM Documentation

This site contains the complete documentation for the Pi-Server-VM project.

## What is Pi-Server-VM?

Pi-Server-VM is a set of cross-platform tools to fully automate the creation and management of secure, minimal Debian virtual machines in Oracle VirtualBox. This project is designed to emulate a Raspberry Pi server environment, making it ideal for testing server software and network configurations without needing physical hardware.

This project is a core component of the PiSelfhosting ecosystem.

## Project Workflow

This diagram shows the core lifecycle of creating and using a virtual machine with this project.
```mermaid
graph TD
    A["User runs the create-master-vm tool"] --> B["A pi-master-template VM is created in VirtualBox"];
        B --> C["User runs the clone-vm tool"];
        C --> D["A new Clone VM, for example 'my-dev-pi', is created"];
        D --> E["The Clone boots for the first time"];
        E --> F["The first-boot service runs inside the VM, setting a unique hostname and identity"];
        F --> G["The Clone is now ready on the network at my-dev-pi.local"];
```
## Getting Started

To get started, please use the navigation menu to find the detailed installation guide for your operating system.

-   For the easiest setup on Windows, please see the guide for our professional setup.exe installer.
-   For macOS and Linux users, the guides will walk you through setting up the command-line executables.
-   For advanced users, we also provide a pre-built .ova virtual appliance for an instant start on any platform.

## Contributing

We welcome contributions! If you would like to help improve the project, please see our detailed Contributing Guide in the navigation menu.
