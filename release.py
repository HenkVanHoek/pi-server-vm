# release.py (Final, Robust Version)
"""
A failsafe, multi-command release script for the project.

This script automates the entire release process to prevent manual errors.
It has two main modes of operation:

1. Create a New Release:
   Performs a series of pre-flight checks to ensure the repository is in a
   clean and ready state. If all checks pass, it then:
     - Bumps the version number in all configured files.
     - Creates a version bump commit and a corresponding Git tag.
     - Pushes the new commit and tag to the remote repository, which in turn
       triggers the GitHub Actions build workflow for the executables.

   Usage: python release.py [patch|minor|major]

2. Upload Release Assets:
   Finds the latest Git tag, exports the master VirtualBox VM to a .ova file,
   and uploads this file as an asset to the corresponding GitHub Release. This
   command is robust and can handle race conditions with the CI/CD pipeline.

   Usage: python release.py upload
"""
import os
import sys
import subprocess
import time


def check_git_sync_status():
    """
    Performs a pre-flight check to ensure the local repository is in sync with
    the remote.
    """
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
                "\n❌ GIT SYNC ERROR: Your local branch is behind the remote.",
                file=sys.stderr,
            )
            print(
                "   Please run 'git pull' to update your local code.", file=sys.stderr
            )
            sys.exit(1)
        elif "Your branch is ahead" in output:
            print(
                "\n❌ GIT SYNC ERROR: Your local branch has unpushed commits.",
                file=sys.stderr,
            )
            print("   Please run 'git push' to publish your changes.", file=sys.stderr)
            sys.exit(1)
        elif "have diverged" in output:
            print(
                "\n❌ GIT SYNC ERROR: Your local branch has diverged from "
                "the remote.",
                file=sys.stderr,
            )
            print("   Please rebase or merge with the remote branch.", file=sys.stderr)
            sys.exit(1)
        else:
            print(
                "\n⚠️  Could not determine Git sync status. Please check manually.",
                file=sys.stderr,
            )
            return True
    except subprocess.CalledProcessError as e:
        print(
            f"\n❌ An error occurred while checking Git status: {e.stderr}",
            file=sys.stderr,
        )
        sys.exit(1)


def run_and_check(command, check_name):
    """Runs a command, checks for errors, and exits on failure."""
    print(f"--- CHECK: {check_name} ---")
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("--- PASSED ---")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n--- FAILED: {check_name} ---")
        print("--- REASON ---")
        print(e.stderr)
        print("\nAborting release. No files have been changed.")
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
    except subprocess.CalledProcessError as e:
        print("❌ Could not find any Git tags in the repository.", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)


def export_and_upload_vm(tag_name):
    """
    Configures, exports, and uploads the master VM. Handles pre-existing files
    and waits for the GitHub release to be created.
    """
    # --- Configuration ---
    MASTER_VM_NAME = "pi-master-template"

    # Ensure the standard output directory exists.
    os.makedirs("dist", exist_ok=True)
    OVA_FILENAME = os.path.join("dist", f"pi-server-template-{tag_name}.ova")

    # --- Pre-flight Check: Clean up old artifact before starting ---
    if os.path.exists(OVA_FILENAME):
        print(f"   -> Found pre-existing artifact. Deleting: {OVA_FILENAME}")
        try:
            os.remove(OVA_FILENAME)
        except OSError as e:
            print(
                f"❌ FATAL ERROR: Could not delete old .ova file: {e}", file=sys.stderr
            )
            sys.exit(1)

    # --- ACTION 1: Export the VM using VBoxManage ---
    print(
        f"\n--- ACTION: Exporting master template "
        f"Virtual Machine '{MASTER_VM_NAME}' ---"
    )
    print(f"         -> This may take several minutes...")
    try:
        subprocess.run(
            ["VBoxManage", "export", MASTER_VM_NAME, f"--output={OVA_FILENAME}"],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"✅ VM exported successfully to '{OVA_FILENAME}'")
    except FileNotFoundError:
        print("❌ FATAL ERROR: 'VBoxManage' command not found.", file=sys.stderr)
        print(
            "   Is VirtualBox installed and its directory in your system's PATH?",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ FATAL ERROR: Failed to export the VM.", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)

    # --- ACTION 2: Upload the .ova file with a retry mechanism ---
    print(f"\n--- ACTION: Uploading '{OVA_FILENAME}' to release {tag_name} ---")

    max_retries = 10  # Try for 5 minutes (10 * 30 seconds)
    for attempt in range(max_retries):
        try:
            # We must capture output to check for the specific error
            result = subprocess.run(
                ["gh", "release", "upload", tag_name, OVA_FILENAME, "--clobber"],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"✅ '{OVA_FILENAME}' uploaded successfully.")
            # Add the stdout from the gh command for user confirmation
            print(result.stdout)
            return  # Success, exit the function
        except FileNotFoundError:
            print("❌ FATAL ERROR: 'gh' command not found.", file=sys.stderr)
            print(
                "   Have you installed the GitHub CLI and "
                "authenticated with 'gh auth login'?",
                file=sys.stderr,
            )
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            # Check if the error is the specific "release not found" error
            if "release not found" in e.stderr:
                if attempt < max_retries - 1:
                    print(
                        f"   -> Release page not found yet. "
                        f"Waiting 30 seconds... ({attempt + 1}/{max_retries})"
                    )
                    time.sleep(30)
                else:
                    print(
                        "❌ FATAL ERROR: Release was not found after 5 minutes.",
                        file=sys.stderr,
                    )
                    print(e.stderr, file=sys.stderr)
                    sys.exit(1)
            else:
                # It was a different, unexpected error
                print(
                    f"❌ FATAL ERROR: Failed to upload the release asset.",
                    file=sys.stderr,
                )
                print(e.stderr, file=sys.stderr)
                sys.exit(1)


def main():
    """Handles the different release commands."""

    if len(sys.argv) < 2:
        print("Usage: python release.py [patch|minor|major|upload]")
        sys.exit(1)

    command = sys.argv[1]

    # --- Mode 1: Create a New Release ---
    if command in ("patch", "minor", "major"):
        part = command
        print(f"🚀 Starting fully automated release process for a '{part}' update...")

        check_git_sync_status()

        git_status_output = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True
        ).stdout
        if git_status_output:
            print(f"\n--- FAILED: Is Git working directory clean? ---")
            print("--- REASON ---")
            print("Your working directory has uncommitted changes:")
            print(git_status_output)
            print("\nPlease commit or stash your changes before creating a release.")
            sys.exit(1)
        print("--- CHECK: Is Git working directory clean? ---")
        print("--- PASSED ---")

        run_and_check(["git", "push", "--dry-run"], "Can connect and push to remote?")
        run_and_check(
            ["bump-my-version", "bump", part, "--tag", "--dry-run"],
            f"Can bump-my-version perform a '{part}' bump?",
        )

        print("\n✅ All pre-flight checks passed. Proceeding with release.")

        print(f"\n--- ACTION: Bumping version with bump-my-version ({part}) ---")
        try:
            subprocess.run(
                ["bump-my-version", "bump", part, "--tag"], check=True, text=True
            )
            print("--- ACTION SUCCEEDED ---")
        except subprocess.CalledProcessError as e:
            print("\nFATAL ERROR: bump-my-version failed unexpectedly.")
            print(e.stderr)
            sys.exit(1)

        print("\n--- ACTION: Pushing new commit and tag to remote ---")
        try:
            subprocess.run(["git", "push", "--follow-tags"], check=True, text=True)
            print("--- ACTION SUCCEEDED ---")
        except subprocess.CalledProcessError as e:
            print("\nFATAL ERROR: Failed to push after tagging.")
            print(e.stderr)
            sys.exit(1)

        print("\n🎉 Release successful! A new version has been tagged and pushed.")
        print("   To upload the VM image, now run: python release.py upload")

    # --- Mode 2: Upload Assets to the Latest Release ---
    elif command == "upload":
        print("🚀 Starting VM export and upload process...")
        latest_tag = get_latest_tag()
        export_and_upload_vm(latest_tag)
        print("\n🎉 All assets have been successfully uploaded. 🎉")

    # --- Handle Invalid Commands ---
    else:
        print(f"❌ Unknown command: '{command}'")
        print("Usage: python release.py [patch|minor|major|upload]")
        sys.exit(1)


if __name__ == "__main__":
    main()
