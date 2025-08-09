# version.py
import sys
import subprocess

# A dictionary mapping simple commands to the full bump2version arguments
COMMANDS = {
    # Actual bump commands
    "patch": ["patch"],
    "minor": ["minor"],
    "major": ["major"],
    # Dry run commands for previewing
    "dry-run-patch": ["patch", "--dry-run", "--allow-dirty", "--verbose"],
    "dry-run-minor": ["minor", "--dry-run", "--allow-dirty", "--verbose"],
    "dry-run-major": ["major", "--dry-run", "--allow-dirty", "--verbose"],
}

HELP_MESSAGE = f"""
PiSelfhosting Versioning Helper

Usage: python version.py [COMMAND]

Available Commands:
  - patch, minor, major:                Bumps the version and modifies files.
  - dry-run-patch, dry-run-minor, ...:  Shows a preview of what will be changed.
  - help:                               Shows this message.

Example:
  python version.py dry-run-patch
"""


def main():
    """Parses command line arguments and runs the corresponding bump2version command."""
    if len(sys.argv) < 2 or sys.argv[1] in ("help", "-h", "--help"):
        print(HELP_MESSAGE)
        return

    command = sys.argv[1]
    if command not in COMMANDS:
        print(f"Error: Unknown command '{command}'\n")
        print(HELP_MESSAGE)
        sys.exit(1)

    # The base command to run
    base_command = ["bump2version"]
    # Add the specific arguments for the chosen command
    args_to_add = COMMANDS[command]

    full_command = base_command + args_to_add

    print(f"--- Running command: {' '.join(full_command)} ---\n")

    try:
        # Run the command. The terminal from which this script is run
        # should have the virtual environment activated.
        subprocess.run(full_command, check=True)
    except FileNotFoundError:
        print("Error: 'bump2version' command not found.")
        print("Please ensure your virtual environment is activated.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("\n--- The command failed to complete. ---")
        sys.exit(1)


if __name__ == "__main__":
    main()
