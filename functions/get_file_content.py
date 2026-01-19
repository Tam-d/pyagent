import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        work_path_abs = os.path.abspath(working_directory)
        joined_path = os.path.join(work_path_abs, file_path)
        target_path = os.path.normpath(joined_path)
        valid_target = os.path.commonpath([work_path_abs, target_path]) == work_path_abs
        is_file = os.path.isfile(target_path)

        print(f"Path: {work_path_abs}")
        print(f"Joined: {joined_path}")
        print(f"Target: {target_path}")
        print(f"Valid Target: {valid_target}")
        print(f"Is file: {is_file}")

        if not valid_target:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not is_file:
            return  f'Error: File not found or is not a regular file: "{file_path}"'
        
        content = ""

        with open(target_path, "r") as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
        return content
    
    except Exception as e:
        return f"Error: {e}"