import os
from google import genai

def write_file(working_directory, file_path, content):
    try:
            working_dir_abs = os.path.abspath(working_directory)
            target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
            common_dir = os.path.commonpath([working_dir_abs, target_file])
            
            if common_dir != working_dir_abs:
                  return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            if os.path.isdir(target_file):
                  return f'Error: Cannot write to "{file_path}" as it is a directory'
            
            os.makedirs(os.path.dirname(target_file), exist_ok= True)
            with open(target_file, "w") as f:
                  f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

      
            
    except Exception as e:
          return f'Error: writing to file: {e}'
    

schema_write_file = genai.types.FunctionDeclaration(
    name="write_file",
    description="Writes content into the specified file",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type= genai.types.Type.STRING,
                description="File path containing the file to be modified/created",
            ),
            "content": genai.types.Schema(
                type= genai.types.Type.STRING,
                description="Content to be written in the specified file",
            )
        },
        required=["file_path", "content"],
    ),
)