# build.py (Simplified and Robust Version)
import os
import subprocess
import sys


def main():
    """Finds all spec files and runs PyInstaller for each one."""
    print("--- Starting build process ---")

    # Find all .spec files in the current directory.
    spec_files = [f for f in os.listdir(".") if f.endswith(".spec")]

    if not spec_files:
        print("Error: No .spec files found in the root directory.", file=sys.stderr)
        return 1

    print(f"--- Found {len(spec_files)} spec file(s) to build ---")
    for spec_file in spec_files:
        print(f"\nBuilding from: {spec_file}")
        try:
            # We run the command from the root of the checkout.
            # The .spec files and their referenced scripts are all in the same directory.
            subprocess.run(["pyinstaller", spec_file], check=True)
            print(f"Successfully built: {spec_file}")
        except subprocess.CalledProcessError:
            print(
                f"--- ERROR building {spec_file} ---",
                file=sys.stderr,
            )
            return 1

    print("\n--- Build process completed successfully! ---")
    return 0


if __name__ == "__main__":
    sys.exit(main())
