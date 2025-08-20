# tests/test_build_process.py
import unittest

# import subprocess
import os
import sys
import shutil

# This test should be run from the root of the project, not the 'tests' directory.
# We will configure PyCharm or the command line to do this.
# This ensures that 'build.py' can find all its files.
sys.path.insert(0, ".")

# Import the main function from the build script
from build import main as build_main


class TestBuildProcessIntegration(unittest.TestCase):

    def setUp(self):
        """This method is called before each test."""
        print("\n--- SETUP: Cleaning up old build artifacts ---")
        if os.path.isdir("build"):
            shutil.rmtree("build")
        if os.path.isdir("dist"):
            shutil.rmtree("dist")
        print("✅ Setup complete.")

    def test_build_script_runs_successfully_and_creates_artifacts(self):
        """
        Tests that the build.py script runs without errors and that the
        expected output directories and executables are created.
        """
        # --- 1. ACT: Run the build.py script ---
        print("\n--- ACT: Running the main build script ---")

        # We call the main function directly.
        # We check its return code to see if it succeeded.
        return_code = build_main()

        # --- 2. ASSERT: Check that the script reported success ---
        print("\n--- ASSERT: Verifying build script success ---")
        self.assertEqual(
            return_code, 0, "The build.py script did not return a success code (0)."
        )
        print("✅ Build script reported success.")

        # --- 3. ASSERT: Check that the output directories exist ---
        print("\n--- ASSERT: Verifying output directories and files ---")
        self.assertTrue(
            os.path.isdir("dist"), "The 'dist' directory was " "not created."
        )

        expected_apps = ["clone-vm", "create-master-vm", "pi-selfhosting-web"]
        for app in expected_apps:
            app_dir = os.path.join("dist", app)
            self.assertTrue(
                os.path.isdir(app_dir),
                f"The application directory '{app_dir}' was " f"not created.",
            )

            # Determine the executable name based on the OS
            exe_name = app
            if sys.platform == "win32":
                exe_name += ".exe"

            exe_path = os.path.join(app_dir, exe_name)
            self.assertTrue(
                os.path.isfile(exe_path), f"The executable '{exe_path}' was not found."
            )
            print(f"✅ Found application: {app_dir}")

        print("✅ All expected artifacts were created.")

    def tearDown(self):
        """This method is called after each test."""
        print("\n--- TEARDOWN: Cleaning up build artifacts ---")
        if os.path.isdir("build"):
            shutil.rmtree("build")
        if os.path.isdir("dist"):
            shutil.rmtree("dist")
        print("✅ Teardown complete.")


if __name__ == "__main__":
    # This allows you to run the test directly from the command line
    unittest.main()
