# webapp/app.py
import subprocess
import sys
from flask import Flask, render_template, request, flash

# --- Flask App Initialization ---
app = Flask(__name__)
# A secret key is required for flashing messages, which securely signs the session cookie.
app.config["SECRET_KEY"] = "a-random-and-secure-secret-key-for-this-project"


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles both displaying the form (GET) and processing its submission (POST).
    """
    form_data = request.form

    if request.method == "POST":
        # --- Retrieve Form Data ---
        vm_name = form_data.get("vm_name")
        ram = form_data.get("ram")
        cpus = form_data.get("cpus")
        disk_size = form_data.get("disk_size")

        # --- Build the Command (Modern Package-Aware Approach) ---
        # Run the script as a module to respect the installed package structure.
        command = [sys.executable, "-m", "scripts.clone_vm"]

        # Add the required vm_name argument.
        if vm_name:
            command.append(vm_name)
        else:
            # If vm_name is missing, flash an error and reload the page.
            flash("VM Name is a required field.", "error")
            return render_template("index.html", form_data=form_data)

        # Add optional arguments if they were provided in the form.
        if ram:
            command.extend(["--ram", ram])
        if cpus:
            command.extend(["--cpus", cpus])
        if disk_size:
            command.extend(["--disk-size", disk_size])

        try:
            # --- Run the Backend Script ---
            # Execute the command and capture stdout and stderr.
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
    # This block allows running the app directly for development.
    # For production, a proper WSGI server like Gunicorn or Waitress should be used.
    # host='0.0.0.0' makes the app accessible on your local network.
    app.run(debug=True, host="0.0.0.0")
