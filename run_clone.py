# run_clone.py
"""
Entry point for the clone_vm executable.

This script is designed to be the target for PyInstaller to correctly
bundle the 'scripts' package and its modules. It simply imports and
executes the main function from the actual script.
"""
import sys
from scripts.clone_vm import main

if __name__ == "__main__":
    sys.exit(main())
