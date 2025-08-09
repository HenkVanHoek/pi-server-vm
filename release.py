# release.py
import sys
import subprocess


def run_and_check(command, check_name):
    """Runs a command, checks for errors, and exits on failure."""
    print(f"--- CHECK: {check_name} ---")
    try:
        # We capture output to keep the console clean for checks
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("--- PASSED ---")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n--- FAILED: {check_name} ---")
        print("--- REASON ---")
        # Print stderr to show the user the actual error message
        print(e.stderr)
        print("\nAborting release. No files have been changed.")
        sys.exit(1)


def main():
    """Performs a fully automated, failsafe release."""
    if len(sys.argv) < 2 or sys.argv[1] not in ("patch", "minor", "major"):
        print("Usage: python release.py [patch|minor|major]")
        sys.exit(1)

    part = sys.argv[1]

    print("🚀 Starting fully automated release process...")

    # PRE-FLIGHT CHECK 1: Is the Git working directory clean?
    run_and_check(["git", "status", "--porcelain"], "Is Git working directory clean?")

    # PRE-FLIGHT CHECK 2: Can we connect to the remote and push?
    run_and_check(["git", "push", "--dry-run"], "Can connect and push to remote?")

    # PRE-FLIGHT CHECK 3: Can bump2version run without errors?
    run_and_check(
        ["bump2version", part, "--dry-run", "--allow-dirty", "--verbose"],
        f"Can bump2version perform a '{part}' bump?",
    )

    print("\n✅ All pre-flight checks passed. Proceeding with release.")

    # --- THE POINT OF NO RETURN ---

    # STEP 1: Perform the actual version bump, commit, and tag.
    print(f"\n--- ACTION: Bumping version, committing, and tagging ({part}) ---")
    try:
        # We show the output of the real command
        subprocess.run(["bump2version", part], check=True)
        print("--- ACTION SUCCEEDED ---")
    except subprocess.CalledProcessError:
        print("\nFATAL ERROR: bump2version failed unexpectedly after checks passed.")
        sys.exit(1)

    # STEP 2: Push the new commit and tag to the remote.
    print("\n--- ACTION: Pushing new commit and tag to remote ---")
    try:
        subprocess.run(["git", "push", "--follow-tags"], check=True)
        print("--- ACTION SUCCEEDED ---")
    except subprocess.CalledProcessError:
        print("\nFATAL ERROR: Failed to push after tagging.")
        print("Your local repository has the new tag, but the remote does not.")
        sys.exit(1)

    print("\n🎉 Release successful! New version has been tagged and pushed. 🎉")


if __name__ == "__main__":
    main()
