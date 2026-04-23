import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a specified python file. Example: 'run main.py'",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Specifiy the file to run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY.STRING,
                description="Arguments to append to the file being run.",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if not os.path.isfile(target_file):
            return Exception(
                f'Error: "{file_path}" does not exist or is not a regular file'
            )
        if not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs:
            return Exception(
                f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            )
        if not target_file.endswith(".py"):
            return Exception(f'Error: "{file_path}" is not a Python file')
        command = ["python3", target_file]
        if args is not None:
            command.extend(args)
        output = subprocess.run(
            command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30
        )
        term_out = []
        if output.returncode != 0:
            term_out.append(f"Process exited with code {output.returncode}")
        if output.stderr is None and output.stdout is None:
            term_out.append("No output produced")
        if output.stdout:
            term_out.append(f"STDOUT:\n{output.stdout}")
        if output.stderr:
            term_out.append(f"STDERR:\n{output.stderr}")
        return "\n".join(term_out)
    except Exception as e:
        return f"Error: executing Python file: {e}"
