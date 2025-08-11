# build.py (Final, CI-aware version)
import os
import subprocess
import sys


def main():
    """Finds all spec files and runs PyInstaller for each one."""
    print("--- Starting build process ---")

    # On GitHub Actions, the code is in a subdirectory with the repo name.
    # We check if we are in that environment.
    repo_name = os.environ.get("GITHUB_REPOSITORY_NAME", "")
    project_dir = "."
    if repo_name and os.path.isdir(repo_name):
        project_dir = repo_name
        print(
            f"GitHub Actions environment detected. Setting project dir to: {project_dir}"
        )

    # Find all .spec files inside the correct project directory.
    spec_files = [
        os.path.join(project_dir, f)
        for f in os.listdir(project_dir)
        if f.endswith(".spec")
    ]

    if not spec_files:
        print("Error: No .spec files found.", file=sys.stderr)
        return 1

    print(f"--- Found {len(spec_files)} spec file(s) to build ---")
    for spec_file_path in spec_files:
        print(f"\nBuilding from: {spec_file_path}")
        try:
            # We must run pyinstaller with the project directory as the current working directory
            # so that all the relative paths in the .spec files work correctly.
            subprocess.run(["pyinstaller", spec_file_path], check=True, cwd=project_dir)
            print(f"Successfully built: {os.path.basename(spec_file_path)}")
        except subprocess.CalledProcessError:
            print(
                f"--- ERROR building {os.path.basename(spec_file_path)} ---",
                file=sys.stderr,
            )
            return 1

    print("\n--- Build process completed successfully! ---")
    return 0


if __name__ == "__main__":
    sys.exit(main())
