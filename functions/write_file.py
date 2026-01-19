import os

def write_file(working_directory, file_path, content):

    try:

        work_path_abs = os.path.abspath(working_directory)
        joined_path = os.path.join(work_path_abs, file_path)
        target_path = os.path.normpath(joined_path)
        valid_target = os.path.commonpath([work_path_abs, target_path]) == work_path_abs
        is_dir = os.path.isdir(target_path)

        if not valid_target:
            return f'Error: Cannot read "{target_path}" as it is outside the permitted working directory'
        
        if is_dir:
            return f'Error: Cannot write to "{target_path}" as it is a directory'
        

        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{target_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"