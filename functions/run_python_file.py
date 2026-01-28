import os
import subprocess
from google import genai

def run_python_file(working_directory, file_path, args=None):
        try:
            working_dir_abs = os.path.abspath(working_directory)
            target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
            common_dir = os.path.commonpath([working_dir_abs, target_file])
            
            if common_dir != working_dir_abs:
                  return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            if not os.path.isfile(target_file):
                  return f'Error: "{file_path}" does not exist or is not a regular file'
            if not target_file.endswith('.py'):
                  return f'Error: "{file_path}" is not a Python file'
            
            command = ["python",file_path]
            if args is not None:
                  command.extend(args)

            result = subprocess.run(
            command,
            cwd=working_dir_abs,    # Set the working directory
            capture_output=True,     # Capture stdout and stderr
            text=True,               # Decode output to strings
            timeout=30               # Prevent infinite execution
        )
            output_parts = []

            if result.returncode != 0:
                  output_parts.append(f"Process exited with code {result.returncode}")

            if not result.stdout.strip() and not result.stderr.strip():
                  output_parts.append("No output produced")
            else:
                  if result.stdout:
                        output_parts.append(f"STDOUT: {result.stdout.strip()}")
                  if result.stderr:
                        output_parts.append(f"STDERR: {result.stderr.strip()}")

            return "\n".join(output_parts)

            
        except Exception as e:
              return f'Error: executing Python file: {e}'
        

schema_run_python_file = genai.types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified Python file",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type= genai.types.Type.STRING,
                description="File path containing the python file (eg., ./test.py)",
            ),
            "args": genai.types.Schema(
                  type=genai.types.Type.ARRAY,
                  description="Optional arguments to be passed with the python file",
                  items=genai.types.Schema(
                        type=genai.types.Type.STRING,
                        description="Single argument string"
                  ),
            )
,
        },
        required=["file_path"],
    ),
)