# webapp/app.py
import subprocess
import sys
import os
from flask import Flask, render_template, request, flash
from waitress import serve


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore
    except AttributeError:
        # In a development environment, the base path is the app's root directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# --- Flask App Initialization ---
template_dir = resource_path("templates")
static_dir = resource_path("static")

app = Flask(
    __name__, template_folder=template_dir, static_folder=static_dir
)  # A secret key is required for flashing messages, which securely signs the session cookie.
app.config["SECRET_KEY"] = "a-random-and-secure-secret-key-for-this-project"


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles both displaying the form (GET) and processing its submission (POST).
    """
    form_data = request.form

    if request.method == "POST":
        # --- Retrieve Form Data (including new fields) ---
        vm_name = form_data.get("vm_name")
        ram = form_data.get("ram")
        cpus = form_data.get("cpus")
        disk_size = form_data.get("disk_size")
        user = form_data.get("user")
        password = form_data.get("password")
        start = form_data.get("start")  # Will be 'on' if checked, otherwise None

        # --- Build the Command (Modern Package-Aware Approach) ---
        command = [sys.executable, "-m", "scripts.clone_vm"]

        # Add the required vm_name argument.
        if vm_name:
            command.append(vm_name)
        else:
            flash("VM Name is a required field.", "error")
            return render_template("index.html", form_data=form_data)

        # Add optional arguments if they were provided in the form.
        if ram:
            command.extend(["--ram", ram])
        if cpus:
            command.extend(["--cpus", cpus])
        if disk_size:
            command.extend(["--disk-size", disk_size])
        if user:
            command.extend(["--user", user])
        if password:
            command.extend(["--password", password])
        if start:
            command.append("--start")

        try:
            # --- Run the Backend Script ---
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,  # Do not raise an exception on error; we will handle it.
            )

            # --- Process the Result ---
            if result.returncode == 0:
                flash(result.stdout, "success")
            else:
                flash(result.stderr, "error")

        except Exception as e:
            # Catch any other unexpected errors during subprocess execution.
            flash(f"An unexpected application error occurred: {str(e)}", "error")

    # Re-render the template with any flashed messages and form data.
    return render_template("index.html", form_data=form_data)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
