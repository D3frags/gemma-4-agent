import os

from google.genai import types

from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a specified files contents, printing the content as well as character length.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File to read content from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # print(target_file)
        if not os.path.isfile(target_file):
            return Exception(f'Error: "{file_path}" is not a file or does not exist.')
        if not os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs:
            return Exception(
                f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            )
        # return f"File OK: {target_file}"
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += (
                    f'[...File "{target_file}" truncated at {MAX_CHARS} characters]'
                )
        return file_content_string
    except Exception as e:
        return f"Error: {e}"


# print(get_file_content("calculator", "pkg/calculator.py"))
