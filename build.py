# build.py
"""
A simple, cross-platform build script for the project.

This script automates the process of building the standalone executables
using PyInstaller. It performs the following steps:
1. Cleans up old build artifacts (the 'dist' and 'build' directories).
2. Finds all PyInstaller *.spec files in the root directory.
3. Runs PyInstaller for each spec file found.
4. Reports the final location of the executables.
"""

import glob
import os
import shutil
import subprocess
import sys

# Directories to clean before a new build
BUILD_DIRS = ["build", "dist"]


def clean():
    """Removes previous build artifacts."""
    print("--- Cleaning up old build artifacts ---")
    for directory in BUILD_DIRS:
        if os.path.isdir(directory):
            print(f"Removing directory: {directory}")
            shutil.rmtree(directory)
    print("Cleanup complete.\n")


def build():
    """Finds all spec files and runs PyInstaller for each one."""
    spec_files = glob.glob("*.spec")

    if not spec_files:
        print("Error: No .spec files found in the root directory.", file=sys.stderr)
        print(
            "Please run 'pyinstaller your_script.py' first to generate them.",
            file=sys.stderr,
        )
        return False

    print(f"--- Found {len(spec_files)} spec file(s) to build ---")
    for spec in spec_files:
        print(f"Building from: {spec}")
        try:
            subprocess.run(["pyinstaller", spec], check=True)
            print(f"Successfully built: {spec}\n")
        except subprocess.CalledProcessError as e:
            print(f"--- ERROR building {spec} ---", file=sys.stderr)
            print(f"PyInstaller failed with exit code: {e.returncode}", file=sys.stderr)
            return False
        except FileNotFoundError:
            print("Error: 'pyinstaller' command not found.", file=sys.stderr)
            print(
                "Please ensure PyInstaller is installed in your active virtual environment.",
                file=sys.stderr,
            )
            return False
    return True


def main():
    """Main execution function."""
    clean()
    if build():
        print("--- Build process completed successfully! ---")
        print(
            f"Executables can be found in the '{os.path.join(os.getcwd(), 'dist')}' directory."
        )
        return 0
    else:
        print(
            "\n--- Build process failed. Please see the errors above. ---",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
