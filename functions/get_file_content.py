import os
import config
from google import genai

def get_file_content(working_directory, file_path):
        try:
            working_dir_abs = os.path.abspath(working_directory)
            target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
            common_dir = os.path.commonpath([working_dir_abs, target_file])
            if common_dir != working_dir_abs:
                    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            if not os.path.isfile(target_file):
                    return f'Error: File not found or is not a regular file: "{file_path}"'
            
            MAX_CHARS = config.MAX_CHARS

            with open(target_file, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                if f.read(1):
                    file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return file_content_string
        except Exception as e:
              return f"Error: getting file content: {e}"


schema_get_file_content = genai.types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the file contents of a file given the file path",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type= genai.types.Type.STRING,
                description="File path containing the file to be read",
            ),
        },
        required=["file_path"],
    ),
)

                

                