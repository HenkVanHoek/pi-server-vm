# How to Contribute to Pi Server VM

First, thank you for considering a contribution! We welcome any help, whether it is reporting a bug, proposing a new feature, or submitting code changes.

## Reporting Bugs

- If you find a bug, please check the [Issues](https://github.com/HenkVanHoek/pi-server-vm/issues) page to see if it has already been reported.
- If it has not, please open a new issue. Be sure to include:
    - Your operating system (e.g., Windows 11, macOS Sonoma).
    - The versions of VirtualBox and Python you are using.
    - A clear description of the bug and the steps to reproduce it.
    - Any relevant error messages or logs.

## Suggesting Enhancements

If you have an idea for a new feature or an improvement to an existing one, feel free to open an issue to start a discussion.

## Development Setup

To get started with developing the scripts locally, follow these steps:

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** to your local machine:

        git clone https://github.com/YourUsername/pi-server-vm.git
        cd pi-server-vm

3.  **Prerequisites:** Ensure you have [Python 3.8+](https://www.python.org/) and [VirtualBox 7.x](https://www.virtualbox.org/wiki/Downloads) installed.
4.  **Create a Virtual Environment:**

        python -m venv .venv
        # On Windows
        .venv\Scripts\activate
        # On macOS/Linux
        source .venv/bin/activate

5.  **Install Dependencies:**

        pip install requests pytest bump2version

## Setting Up the Release Mastering Environment

While day-to-day development of the Python scripts can be done on any operating system (Windows, macOS, or Linux), creating an official, complete release requires a **Windows environment**. This is because the final steps of the process involve packaging the Windows installer and exporting the master VirtualBox appliance.

This environment can be a physical Windows PC or, for developers on other platforms, a dedicated Windows Virtual Machine.

To set up your mastering environment, you will need to install the following software **inside your Windows environment**:

1.  **Git for Windows**
2.  **Python 3.11**
3.  **`uv`** (e.g., via `pipx install uv`)
4.  **Project Dependencies** (run `uv pip install -e .[dev]` in the project root)
5.  **Oracle VirtualBox for Windows**
6.  **Inno Setup 6** (from [jrsoftware.org](https://jrsoftware.org/isinfo.php))
7.  **GitHub CLI** (`gh`)

Before you can run the `finalize` command, you must first use the `create-master-vm` tool within this environment to generate the `pi-master-template` that VirtualBox will use for the export.

## Submitting Changes (Pull Requests)

1.  Create a new branch for your feature or bugfix. For example:

        git checkout -b feature/my-new-feature

2.  Make your changes and commit them with a clear, descriptive commit message.
3.  Push the branch to your fork on GitHub. For example:

        git push origin feature/my-new-feature

4.  Open a **Pull Request** from your branch to the **main** branch of the original repository.
5.  Please provide a clear description of the changes you have made in the Pull Request.

## macOS Development

When you build the executables on your Mac using the build.py script, the resulting applications in the dist folder will not be code-signed. The macOS Gatekeeper security feature will prevent them from running correctly.

To test your local builds, you must clear the quarantine attribute after each build. Run the following commands from the root of the project directory in your terminal.

    xattr -cr dist/clone-vm
    xattr -cr dist/create-master-vm
    xattr -cr dist/pi-selfhosting-web

This will allow you to run and test your locally-built executables. The official releases will be signed in the future, but this is the required step for all local development and testing.
Thank you again for your contribution!
