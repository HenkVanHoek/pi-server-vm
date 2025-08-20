# tests/test_installer_creation.py
import unittest
import subprocess
import os
import sys
import shutil

# This test should be run from the root of the project.
sys.path.insert(0, ".")

# Import the functions we want to test from release.py
from release import create_windows_installer, get_current_version_from_tag

# We also need the build script to create the prerequisites
from build import main as build_main


class TestInstallerCreationIntegration(unittest.TestCase):

    # We use a class-level setup because the build process is slow.
    # It will run once for all tests in this class.
    @classmethod
    def setUpClass(cls):
        """This method is called once before any tests in this class run."""
        print("\n--- CLASS SETUP: Building raw executables (prerequisite) ---")
        # Clean up any old artifacts first
        if os.path.isdir("build"):
            shutil.rmtree("build")
        if os.path.isdir("dist"):
            shutil.rmtree("dist")

        # Run the main build script to create the contents for the installer
        return_code = build_main()
        if return_code != 0:
            raise RuntimeError(
                "Prerequisite build failed. Cannot proceed with installer test."
            )
        print("✅ Raw executables built successfully.")

    def test_installer_creation_succeeds(self):
        """
        Tests that create_windows_installer() runs without errors and
        produces the final setup.exe file.
        """
        # This test can only run on Windows where Inno Setup is installed
        if sys.platform != "win32":
            self.skipTest("Installer creation test is Windows-only.")

        # --- 1. ARRANGE: Get the current version for the filename ---
        print("\n--- ARRANGE: Getting current version ---")
        # For a test, we can use a dummy tag as we don't have a real one
        # Or, even better, we read it from the source of truth if available
        # Let's use a dummy version for simplicity and predictability in tests.
        test_version = "0.0.0-test"

        # --- 2. ACT: Call the create_windows_installer function ---
        print("\n--- ACT: Running the create_windows_installer function ---")
        installer_path = create_windows_installer(test_version)

        # --- 3. ASSERT: Verify the installer was created ---
        print("\n--- ASSERT: Verifying setup.exe exists ---")
        self.assertTrue(
            os.path.exists(installer_path),
            f"The installer was not created at {installer_path}",
        )
        print(f"✅ Installer created successfully: {installer_path}")

        # (Optional advanced smoke test could be added here)

    @classmethod
    def tearDownClass(cls):
        """This method is called once after all tests in this class have run."""
        print("\n--- CLASS TEARDOWN: Cleaning up all build artifacts ---")
        if os.path.isdir("build"):
            shutil.rmtree("build")
        if os.path.isdir("dist"):
            shutil.rmtree("dist")
        print("✅ Teardown complete.")


if __name__ == "__main__":
    unittest.main()
