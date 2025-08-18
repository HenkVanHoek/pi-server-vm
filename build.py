# build.py (Forensic Debugging Version)
import os
import subprocess
import sys


def main():
    """Finds all spec files and runs PyInstaller for each one with max debug output."""
    print("--- Starting build process in FORENSIC DEBUG MODE ---")

    spec_files = [f for f in os.listdir(".") if f.endswith(".spec")]

    if not spec_files:
        print("Error: No .spec files found.", file=sys.stderr)
        return 1

    print(f"--- Found {len(spec_files)} spec file(s) to build ---")
    for spec_file in spec_files:
        print(f"\nBuilding from: {spec_file}")
        try:
            # THE CRUCIAL CHANGE: Add "--debug=all" to get maximum verbosity
            command = ["pyinstaller", "--debug=all", spec_file]
            print(f"Running command: {' '.join(command)}")
            subprocess.run(command, check=True)
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
