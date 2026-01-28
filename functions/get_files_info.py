import os
from google import genai

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        common_dir = os.path.commonpath([working_dir_abs, target_dir])
        if common_dir == working_dir_abs:
            if os.path.isdir(target_dir):
                dir_list = os.listdir(target_dir)
                print_list = []
                for i in dir_list:
                    is_dir = os.path.isdir(os.path.normpath(os.path.join(target_dir,i)))
                    # is_file = os.path.isfile(os.path.normpath(os.path.join(target_dir,i)))
                    size = os.path.getsize(os.path.normpath(os.path.join(target_dir,i)))
                    #  Result for current directory:
                    #   - main.py: file_size=719 bytes, is_dir=False
                    #   - tests.py: file_size=1331 bytes, is_dir=False
                    #   - pkg: file_size=44 bytes, is_dir=True
                    print_list.append(f'- {i}: file_size={size} bytes, is_dir={is_dir}')
                result = '\n'.join(print_list)
                return result


            else:
                return f'Error: "{directory}" is not a directory'
        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: getting file info: {e}"


schema_get_files_info = genai.types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "directory": genai.types.Schema(
                type= genai.types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)