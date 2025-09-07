# release.py (The Final, Definitive Version)
"""
A failsafe, multi-command release script for the pi-server-vm project.

This script automates the entire release process, separating the remote CI/CD
build from the local "mastering" of final release assets.

--- WORKFLOW ---

Step 1: Create the Software Release
  This command bumps the version, creates a commit and tag, and pushes to GitHub.
  This triggers the GitHub Actions workflow which builds the raw, unpackaged
  executables for Windows, macOS, and Linux.

  Usage: python release.py [patch|minor|major]

Step 2: Finalize the Release (Windows Only)
  After the GitHub Action from Step 1 is complete, this command performs all
  the final local mastering tasks. It must be run on a Windows machine with
  the required tools (VirtualBox, Inno Setup, etc.) installed.

  This command will:
    1. Download the raw Windows executables from the GitHub release.
    2. Package them into a professional setup.exe installer.
    3. Export the master VirtualBox VM template to a .ova file.
    4. Upload both the setup.exe and the .ova file to the GitHub release.

  Usage: python release.py finalize

Step 3: Deploy Documentation
  This command builds the documentation and copies it to the production web
  server. It requires a .env file with the DOCS_DEPLOY_PATH variable set.

  Usage: python release.py deploy-docs
"""
import os
import sys
import subprocess
import time
import shutil
import argparse
from dotenv import load_dotenv


# --- Logic Functions (Designed for Testability) ---


def is_git_clean():
    """
    Runs 'git status --porcelain' and returns True if the output is empty
    (indicating a clean directory), and False otherwise.
    """
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    return not result.stdout.strip()


# --- Helper Functions (Action-Takers) ---


def check_git_sync_status():
    """Performs a pre-flight check to ensure the local repository is in sync with the remote."""
    print("🔎 Checking Git repository sync status...")
    try:
        subprocess.run(["git", "fetch"], check=True, capture_output=True, text=True)
        status_result = subprocess.run(
            ["git", "status", "-uno"], check=True, capture_output=True, text=True
        )
        output = status_result.stdout
        if "Your branch is up to date" in output:
            print("✅ Git repository is in sync with the remote.")
            return True
        elif "Your branch is behind" in output:
            print(
                "❌ GIT SYNC ERROR: Your local branch is behind the remote.",
                file=sys.stderr,
            )
            print(
                "   Please run 'git pull' to update your local code.", file=sys.stderr
            )
            sys.exit(1)
        elif "Your branch is ahead" in output:
            print(
                "❌ GIT SYNC ERROR: Your local branch has unpushed commits.",
                file=sys.stderr,
            )
            print("   Please run 'git push' to publish your changes.", file=sys.stderr)
            sys.exit(1)
        elif "have diverged" in output:
            print(
                "❌ GIT SYNC ERROR: Your local branch has diverged from the remote.",
                file=sys.stderr,
            )
            print("   Please rebase or merge with the remote branch.", file=sys.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(
            f"❌ An error occurred while checking Git status: {e.stderr}",
            file=sys.stderr,
        )
        sys.exit(1)


def run_and_check(command, check_name):
    """Runs a command, checks for errors, and exits on failure."""
    print(f"--- CHECK: {check_name} ---")
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("--- PASSED ---")
    except subprocess.CalledProcessError as e:
        print(f"--- FAILED: {check_name} ---")
        print("--- REASON ---")
        print(e.stderr)
        print("Aborting release. No files have been changed.")
        sys.exit(1)


def get_latest_tag():
    """Finds the latest Git tag in the repository."""
    print("🔎 Finding latest Git tag...")
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            check=True,
            capture_output=True,
            text=True,
        )
        tag_name = result.stdout.strip()
        print(f"✅ Found latest tag: {tag_name}")
        return tag_name
    except subprocess.CalledProcessError:
        print("❌ Could not find any Git tags in the repository.", file=sys.stderr)
        sys.exit(1)


def get_current_version_from_tag(tag_name):
    """Extracts the version number from a git tag like v1.2.3."""
    if tag_name.startswith("v"):
        return tag_name[1:]
    return tag_name


# --- Asset Management Functions ---


def download_windows_artifacts(tag_name):
    """Downloads and prepares the raw Windows executables from a release."""
    print(f"--- ACTION: Downloading Windows artifacts for {tag_name} ---")
    if os.path.isdir("dist"):
        shutil.rmtree("dist")
    os.makedirs("dist")
    try:
        subprocess.run(
            [
                "gh",
                "release",
                "download",
                tag_name,
                "--pattern",
                "executables-Windows.zip",
                "--dir",
                ".",
            ],
            check=True,
            text=True,
        )
        print("✅ Download complete. Unzipping artifact...")
        shutil.unpack_archive("executables-Windows.zip", "dist")
        os.remove("executables-Windows.zip")
        print("✅ Artifacts are ready in the 'dist' directory.")
    except subprocess.CalledProcessError:
        print(
            f"❌ FATAL ERROR: Failed to download release assets for tag {tag_name}.",
            file=sys.stderr,
        )
        print(
            "   Does the release exist and does it contain the 'executables-Windows.zip' asset?",
            file=sys.stderr,
        )
        sys.exit(1)


def create_windows_installer(version):
    """Uses Inno Setup to create the installer. Returns the path to the installer."""
    print("--- ACTION: Creating Windows installer with Inno Setup ---")
    iss_file = "installer.iss"
    iscc_path = "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe"
    installer_path = os.path.join("dist", f"pi-server-vm-setup-{version}.exe")
    command = [iscc_path, "/Q", f"/DMyVersion={version}", iss_file]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ Windows installer created: {installer_path}")
        return installer_path
    except FileNotFoundError:
        print(
            f"❌ FATAL ERROR: Inno Setup compiler not found at '{iscc_path}'.",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print("❌ FATAL ERROR: Inno Setup compiler failed.", file=sys.stderr)
        print(e.stdout)
        print(e.stderr)
        sys.exit(1)


def export_vm(tag_name):
    """Exports the master VM. Returns the path to the .ova file."""
    print("--- ACTION: Exporting master template Virtual Machine ---")
    print(f"         -> This may take several minutes...")
    MASTER_VM_NAME = "pi-master-template"
    ova_path = os.path.join("dist", f"pi-server-template-{tag_name}.ova")
    if os.path.exists(ova_path):
        print(f"   -> Found pre-existing artifact. Deleting: {ova_path}")
        os.remove(ova_path)
    try:
        subprocess.run(
            ["VBoxManage", "export", MASTER_VM_NAME, f"--output={ova_path}"],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"✅ VM exported successfully: {ova_path}")
        return ova_path
    except FileNotFoundError:
        print("❌ FATAL ERROR: 'VBoxManage' command not found.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ FATAL ERROR: Failed to export the VM.", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)


def upload_assets(tag_name, asset_paths):
    """Uploads a list of asset files to a specific GitHub release."""
    print(f"--- ACTION: Uploading final assets to release {tag_name} ---")
    max_retries = 10
    for attempt in range(max_retries):
        try:
            command = ["gh", "release", "upload", tag_name]
            command.extend(asset_paths)
            command.append("--clobber")
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print("✅ All assets uploaded successfully.")
            print(result.stdout)
            return
        except FileNotFoundError:
            print("❌ FATAL ERROR: 'gh' command not found.", file=sys.stderr)
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            if "release not found" in e.stderr:
                if attempt < max_retries - 1:
                    print(
                        f"   -> Release page not found yet. Waiting 30 seconds... ({attempt + 1}/{max_retries})"
                    )
                    time.sleep(30)
                else:
                    print(
                        "❌ FATAL ERROR: Release was not found after 5 minutes.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
            else:
                print(
                    f"❌ FATAL ERROR: Failed to upload release assets.", file=sys.stderr
                )
                print(e.stderr, file=sys.stderr)
                sys.exit(1)


def handle_deploy_docs():
    """Builds the MkDocs site and deploys it to the production webserver."""
    print("--- ACTION: Building and deploying documentation website ---")

    # 1. Load environment variables and check for the destination path
    load_dotenv()
    deploy_path = os.getenv("DOCS_DEPLOY_PATH")
    if not deploy_path:
        print(
            "❌ FATAL ERROR: 'DOCS_DEPLOY_PATH' not set in your .env file.",
            file=sys.stderr,
        )
        print(
            "   Please create a .env file and add the full path to your webserver's document root.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"   -> Target deployment path: {deploy_path}")
    if not os.path.isdir(deploy_path):
        print(
            f"❌ FATAL ERROR: The path specified in DOCS_DEPLOY_PATH is not a valid directory.",
            file=sys.stderr,
        )
        sys.exit(1)

    # 2. Build the static site
    print("   -> Building static site with 'mkdocs build'...")
    try:
        subprocess.run(
            ["python", "-m", "mkdocs", "build", "--clean"],
            check=True,
            capture_output=True,
        )
        print("✅ MkDocs build complete. Output is in 'site/' directory.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(
            "❌ FATAL ERROR: 'mkdocs build' failed. Is MkDocs installed?",
            file=sys.stderr,
        )
        if isinstance(e, subprocess.CalledProcessError):
            print(e.stderr, file=sys.stderr)
        sys.exit(1)

    # 3. Copy the site to the destination
    source_dir = "site/"
    print(f"   -> Copying '{source_dir}' to '{deploy_path}'...")
    try:
        # Use shutil.copytree for a robust, cross-platform directory copy
        shutil.copytree(source_dir, deploy_path, dirs_exist_ok=True)
        print("✅ Documentation deployed successfully!")
    except Exception as e:
        print(f"❌ FATAL ERROR: Failed to copy site directory.", file=sys.stderr)
        print(f"   Reason: {e}", file=sys.stderr)
        sys.exit(1)


def handle_version_bump(part):
    """Handles the 'patch', 'minor', or 'major' commands."""
    print(f"🚀 Starting fully automated release process for a '{part}' update...")
    check_git_sync_status()
    print("--- CHECK: Is Git working directory clean? ---")
    if not is_git_clean():
        print("--- FAILED: Is Git working directory clean? ---", file=sys.stderr)
        print("Your working directory has uncommitted changes.", file=sys.stderr)
        sys.exit(1)
    print("--- PASSED ---")
    run_and_check(["git", "push", "--dry-run"], "Can connect and push to remote?")
    run_and_check(
        ["bump-my-version", "bump", part, "--tag", "--dry-run"],
        f"Can bump-my-version perform a '{part}' bump?",
    )
    print("✅ All pre-flight checks passed. Proceeding with release.")
    print(f"--- ACTION: Bumping version with bump-my-version ({part}) ---")
    subprocess.run(["bump-my-version", "bump", part, "--tag"], check=True, text=True)
    print("--- ACTION SUCCEEDED ---")
    print("--- ACTION: Pushing new commit and tag to remote ---")
    subprocess.run(["git", "push", "--follow-tags"], check=True, text=True)
    print("--- ACTION SUCCEEDED ---")
    print("🎉 Release successful! A new version has been tagged and pushed.")
    print(
        "   Wait for the GitHub Action to complete, then run: python release.py finalize"
    )


def handle_finalize():
    """Handles the 'finalize' command."""
    if sys.platform != "win32":
        print(
            "Error: The 'finalize' command can only be run on a Windows machine.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("🚀 Starting final release mastering process...")

    latest_tag = get_latest_tag()
    version = get_current_version_from_tag(latest_tag)

    download_windows_artifacts(latest_tag)
    installer_path = create_windows_installer(version)
    ova_path = export_vm(latest_tag)

    # The downloader executable is built on CI and included in the downloaded zip.
    downloader_path = os.path.join("dist", "download-assets.exe")

    upload_assets(latest_tag, [installer_path, ova_path, downloader_path])

    print("\n🎉 Final release mastering complete! All assets are uploaded. 🎉")
    print("\nTo deploy the documentation, run: python release.py deploy-docs")


def handle_finalize():
    """Handles the 'finalize' command."""
    if sys.platform != "win32":
        print(
            "Error: The 'finalize' command can only be run on a Windows machine.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("🚀 Starting final release mastering process...")

    latest_tag = get_latest_tag()
    version = get_current_version_from_tag(latest_tag)

    download_windows_artifacts(latest_tag)
    installer_path = create_windows_installer(version)
    downloader_path = create_downloader_executable()
    ova_path = export_vm(latest_tag)

    upload_assets(latest_tag, [installer_path, ova_path, downloader_path])

    print("\n🎉 Final release mastering complete! All assets are uploaded. 🎉")
    print("\nTo deploy the documentation, run: python release.py deploy-docs")


# --- Main Command Router ---
def main():
    """Handles the different release commands using argparse."""
    parser = argparse.ArgumentParser(
        description="A release script for the pi-server-vm project."
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="The command to execute."
    )

    # Subparser for version bumps
    parser_bump = subparsers.add_parser(
        "patch", help="Bump patch version, tag, and push."
    )
    parser_bump.set_defaults(func=lambda _: handle_version_bump("patch"))
    parser_minor = subparsers.add_parser(
        "minor", help="Bump minor version, tag, and push."
    )
    parser_minor.set_defaults(func=lambda _: handle_version_bump("minor"))
    parser_major = subparsers.add_parser(
        "major", help="Bump major version, tag, and push."
    )
    parser_major.set_defaults(func=lambda _: handle_version_bump("major"))

    # Subparser for finalize
    parser_finalize = subparsers.add_parser(
        "finalize", help="Finalize a release on Windows."
    )
    parser_finalize.set_defaults(func=lambda _: handle_finalize())

    # Subparser for deploying docs
    parser_deploy = subparsers.add_parser(
        "deploy-docs", help="Build and deploy documentation."
    )
    parser_deploy.set_defaults(func=lambda _: handle_deploy_docs())

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
