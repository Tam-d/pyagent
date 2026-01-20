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
        required=["directory"]
    ),
)

def get_files_info(working_directory, directory="."):
    
    work_path_abs = os.path.abspath(working_directory)
    joined_path = os.path.join(work_path_abs, directory)
    target_path = os.path.normpath(joined_path)
    valid_target = os.path.commonpath([work_path_abs, target_path]) == work_path_abs

    if not valid_target:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    directory_is_dir = os.path.isdir(target_path)

    if not directory_is_dir:
        return f'Error: "{directory}" is not a directory'

    # print(f"Directory is dir?: {directory_is_dir}")
    # print(f"Path: {work_path_abs}")
    # print(f"Joined: {joined_path}")
    # print(f"Target: {target_path}")
    # print(f"Valid Target: {valid_target}")

    dir_info = ""

    for item in os.listdir(target_path):
        try:
            item_path = os.path.join(target_path, item)
            item_is_dir = os.path.isdir(item_path)
            item_size = os.path.getsize(item_path)

            item_info = f"- {item}: file_size={item_size} bytes, is_dir={item_is_dir}"
            dir_info += f"{item_info}\n"

        except Exception as e:
            return f"Error: {e}"
    
    return dir_info