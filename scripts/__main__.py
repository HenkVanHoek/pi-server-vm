"""
This file makes the 'scripts' package runnable.

You can now execute the package directly:
python -m scripts <clone-name> [options]
"""

from scripts import clone_vm

if __name__ == "__main__":
    clone_vm.main()
