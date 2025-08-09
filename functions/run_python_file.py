import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    timeout_seconds = 30
    cmd = ["python3", abs_file_path] + args
    try:
        completed_process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            cwd=abs_working_dir
        )
        output = ""
        if completed_process.stdout:
            output += f"STDOUT:\n{completed_process.stdout}"
        if completed_process.stderr:
            output += f"\nSTDERR:\n{completed_process.stderr}"
        if completed_process.returncode != 0:
            output += f"\nProcess exited with code {completed_process.returncode}"
        if not output.strip():
            return "No output produced."
        return output.strip()
    except Exception as e:
        return f"Error: executing Python file: {e}"