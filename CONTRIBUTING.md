# How to Contribute to Pi Server VM

First, thank you for considering a contribution! We welcome any help, whether it is reporting a bug, proposing a new feature, or submitting code changes.

## Reporting Bugs and Suggesting Enhancements

The best way to contribute is to start a discussion.

-   **Found a Bug?** Please check the [Issues page](https://github.com/HenkVanHoek/pi-server-vm/issues) to see if it has already been reported. If not, please open a new issue with a clear description, your OS and software versions, and steps to reproduce the problem.
-   **Have an Idea?** If you have a proposal for a new feature or an improvement, please open an issue to discuss it.

## Development Environment Setup

To ensure consistency and the ability to perform a full end-to-end test cycle, the official and sole supported development environment for this project is **Windows (10 or 11)**.

While the Python code is cross-platform, the final release assets (the Windows installer and the VirtualBox appliance) must be created and validated on a Windows machine. Contributors on other platforms are welcome to submit code changes, but they will need access to a Windows environment (either physical or in a VM) to verify their changes completely.

### Step 1: Install Core Software

You will need to install the following tools on your Windows machine:

1.  **Git for Windows:** From [git-scm.com](https://git-scm.com/).
2.  **Python 3.11:** From [python.org](https://www.python.org/). **Important:** During installation, ensure you check the box to **"Add python.exe to PATH"**.
3.  **PyCharm Community Edition:** The recommended IDE for this project.
4.  **Oracle VirtualBox:** The latest version, from [virtualbox.org](https://www.virtualbox.org/).
5.  **Inno Setup 6:** The installer compiler, from [jrsoftware.org](https://jrsoftware.org/).
6.  **GitHub CLI (`gh`):** From [cli.github.com](https://cli.github.com/).

### Step 2: Configure Your Environment

After installing the software, a few one-time configuration steps are required:

1.  **Authenticate GitHub CLI:** Open a Command Prompt or PowerShell and run `gh auth login`. Follow the on-screen prompts to log in to your GitHub account.
2.  **Set Default Repository:** After you have forked and cloned the project (see next step), navigate to your local project directory in a terminal and run the following command. This links the `gh` tool to your repository fork.

        gh repo set-default YourUsername/pi-server-vm

### Step 3: Set Up the Project

1.  **Fork and Clone:** Fork the `HenkVanHoek/pi-server-vm` repository on GitHub, then clone your personal fork to your local machine.
2.  **Create Virtual Environment:** It is highly recommended to let PyCharm create a new virtual environment (named `.venv`) for the project when you first open it.
3.  **Install Dependencies:** Open the Terminal within PyCharm (which will automatically activate your virtual environment) and run the following commands to install the project dependencies:

        pip install uv
        uv pip install -e .[dev]

### Step 4: Create the Master VM Template

Before you can test the cloning functionality, you must have a master template. Run the creation script from the PyCharm Terminal:

    python -m scripts.create_master_vm

Follow the on-screen prompts to complete the manual Debian installation.

### Step 5: Verify Your Setup

Your development environment is now complete. You can verify that everything is working by running the entire test suite from the PyCharm Terminal:

    pytest

If all tests pass, your environment is perfectly configured, and you are ready to start developing.

## Submitting Changes (Pull Requests)

1.  Create a new branch for your feature or bugfix (`git checkout -b feature/my-new-feature`).
2.  Make your changes and commit them with a clear, descriptive commit message.
3.  Push the branch to your fork on GitHub (`git push origin feature/my-new-feature`).
4.  Open a **Pull Request** from your branch to the `main` branch of the original `HenkVanHoek/pi-server-vm` repository.
5.  Please provide a clear description of the changes you have made in the Pull Request.

Thank you again for your contribution!
