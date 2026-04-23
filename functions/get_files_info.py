import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        if not os.path.isdir(target_dir):
            return Exception(f'Error: "{directory}" is not a directory')
        if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
            return Exception(
                f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            )
        items = os.listdir(target_dir)
        contents = []
        for item in items:
            item_path = os.path.join(target_dir, item)
            line = (
                f"{item}: "
                + f"file_size={str(os.path.getsize(item_path))} bytes "
                + f"is_dir={str(os.path.isdir(item_path))}"
            )
            contents.append(line)
        return "\n".join(contents)
    except Exception as e:
        return f"Error: {e}"
