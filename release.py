# release.py
"""
A failsafe, one-command release script for the project.

This script automates the entire release process to prevent manual errors.
It performs a series of pre-flight checks to ensure the repository is in
a clean and ready state.

If all checks pass, it then executes the "point of no return":
  1. Bumps the version number using `bump-my-version`.
  2. Creates a version bump commit and a corresponding Git tag.
  3. Pushes the new commit and tag to the remote repository, which in turn
     triggers the GitHub Actions release workflow.

Usage: python release.py [patch|minor|major]
"""
import sys
import subprocess


def check_git_sync_status():
    """
    Performs a pre-flight check to ensure the local repository is in sync with the remote.
    """
    print("🔎 Checking Git repository sync status...")
    try:
        # Step 1: Fetch the latest info from the remote without merging
        subprocess.run(["git", "fetch"], check=True, capture_output=True, text=True)

        # Step 2: Check the status. '-uno' simplifies output to the bare minimum.
        status_result = subprocess.run(
            ["git", "status", "-uno"], check=True, capture_output=True, text=True
        )
        output = status_result.stdout

        # Step 3: Analyze the output
        if "Your branch is up to date" in output:
            print("✅ Git repository is in sync with the remote.")
            return True
        elif "Your branch is behind" in output:
            print(
                "\n❌ GIT SYNC ERROR: Your local branch is behind the remote.",
                file=sys.stderr,
            )
            print(
                "   Please run 'git pull' to update your local code before creating a new release.",
                file=sys.stderr,
            )
            sys.exit(1)  # Exit the script
        elif "Your branch is ahead" in output:
            print(
                "\n❌ GIT SYNC ERROR: Your local branch has commits that have not been pushed.",
                file=sys.stderr,
            )
            print(
                "   Please run 'git push' to publish your changes before creating a new release.",
                file=sys.stderr,
            )
            sys.exit(1)
        elif "have diverged" in output:
            print(
                "\n❌ GIT SYNC ERROR: Your local branch has diverged from the remote.",
                file=sys.stderr,
            )
            print(
                "   Please rebase or merge with the remote branch before creating a new release.",
                file=sys.stderr,
            )
            sys.exit(1)
        else:
            # Fallback for any other unexpected status
            print(
                "\n⚠️  Could not determine Git sync status. Please check manually.",
                file=sys.stderr,
            )
            return True  # Allow to continue but with a warning

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
        # We capture output for checks to keep the console clean
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("--- PASSED ---")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n--- FAILED: {check_name} ---")
        print("--- REASON ---")
        print(e.stderr)  # Print the actual error message
        print("\nAborting release. No files have been changed.")
        sys.exit(1)


def main():
    """Performs a fully automated, failsafe release using bump-my-version."""

    if len(sys.argv) < 2 or sys.argv[1] not in ("patch", "minor", "major"):
        print("Usage: python release.py [patch|minor|major]")
        sys.exit(1)

    part = sys.argv[1]
    part_command = part
    print(part_command)

    print(f"🚀 Starting fully automated release process for a " f"'{part}' update...")

    check_git_sync_status()

    # PRE-FLIGHT CHECK 1: Is the Git working directory clean?
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

    # PRE-FLIGHT CHECK 2: Can we connect to the remote and push?
    run_and_check(["git", "push", "--dry-run"], "Can connect and push to remote?")

    # PRE-FLIGHT CHECK 3: Can bump-my-version run without errors?
    run_and_check(
        ["bump-my-version", "bump", part_command, "--tag", "--dry-run"],
        f"Can bump-my-version perform a '{part}' bump?",
    )

    print("\n✅ All pre-flight checks passed. Proceeding with release.")

    # --- THE POINT OF NO RETURN ---

    # STEP 1: Perform the actual version bump, commit, and tag.
    print(f"\n--- ACTION: Bumping version with bump-my-version ({part}) ---")
    try:
        # Run the real command, showing its output directly to the user
        subprocess.run(
            ["bump-my-version", "bump", part_command, "--tag"], check=True, text=True
        )
        print("--- ACTION SUCCEEDED ---")
    except subprocess.CalledProcessError as e:
        print("\nFATAL ERROR: bump-my-version failed unexpectedly after checks passed.")
        print(e.stderr)
        sys.exit(1)

    # STEP 2: Push the new commit and tag to the remote.
    print("\n--- ACTION: Pushing new commit and tag to remote ---")
    try:
        # Run the final push command, showing its output
        subprocess.run(["git", "push", "--follow-tags"], check=True, text=True)
        print("--- ACTION SUCCEEDED ---")
    except subprocess.CalledProcessError as e:
        print("\nFATAL ERROR: Failed to push after tagging.")
        print("Your local repository has the new tag, but the remote does not.")
        print(e.stderr)
        sys.exit(1)

    print("\n🎉 Release successful! A new version has been tagged and pushed. 🎉")


if __name__ == "__main__":
    main()
