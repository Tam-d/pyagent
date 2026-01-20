import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file given the file name relative to the working directory, and arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to a python file to run, relative to the working directory",
            ),

            "args": types.Schema(
                type=types.Type.ARRAY,
                description="list of arguments to use when running the specified python file (default is None)",
                items= types.Schema(
                    type= types.Type.STRING,
                    description="argument to pass when running the specified python file"
                ),
            ),
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=None):
        try: 
            work_path_abs = os.path.abspath(working_directory)
            joined_path = os.path.join(work_path_abs, file_path)
            target_path = os.path.normpath(joined_path)
            valid_target = os.path.commonpath([work_path_abs, target_path]) == work_path_abs

            if not valid_target:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            
            if not os.path.isfile(target_path):
                return f'Error: "{file_path}" does not exist or is not a regular file'
            
            if not target_path.endswith(".py"):
                return f'Error: "{file_path}" is not a Python file'
            
            

            command = ["python", target_path]

            if args != None:
                command.extend(args)

            # print(f"Executing: {target_path} with args: {args}")
            # print(f"Command: {command}")

            completed_process = subprocess.run(command, capture_output=True, text=True, timeout=30)
            
            result = ""

            if completed_process.returncode == 0:
                result += f"Process exited with code {completed_process.returncode}\n"

            if not completed_process.stdout and not completed_process.stderr:
                result += f"No output produced"

            else:
                if completed_process.stdout:
                    result += f"STDOUT: {completed_process.stdout}\n"
                
                if completed_process.stderr:
                    result += f"STDERR: {completed_process.stderr}\n"
            


            return result
        
        except Exception as e:
            return f"Error: executing Python file: {e}"