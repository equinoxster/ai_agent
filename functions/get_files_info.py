import os
from google import genai

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = working_directory
    
    working_dir_abs = os.path.abspath(working_directory)
    
    # If directory is relative, resolve it relative to the working directory
    if not os.path.isabs(directory):
        target_dir_abs = os.path.abspath(os.path.join(working_directory, directory))
    else:
        target_dir_abs = os.path.abspath(directory)
    
    # Normalize paths to handle .. and . properly
    working_dir_abs = os.path.normpath(working_dir_abs)
    target_dir_abs = os.path.normpath(target_dir_abs)
    
    # Check if target directory is within or is the working directory
    if not (target_dir_abs == working_dir_abs or target_dir_abs.startswith(working_dir_abs + os.sep)):
        return f"Error: Directory '{directory}' is outside the working directory '{working_directory}'"
    
    if not os.path.isdir(target_dir_abs):
        return f"Error: '{directory}' is not a valid directory"
    
    try:
        items = os.listdir(target_dir_abs)
        items.sort()  # Sort alphabetically
        
        result = f"Contents of '{directory}':\n"
        
        for item in items:
            item_path = os.path.join(target_dir_abs, item)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path)
            result += f"- {item}: file_size={file_size} bytes, is_dir={is_dir}\n"
        
        return result.rstrip()  # Remove trailing newline
        
    except PermissionError:
        return f"Error: Permission denied accessing directory '{directory}'"
    except Exception as e:
        return f"Error: Could not read directory '{directory}': {str(e)}"
    
schema_get_files_info = genai.types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "directory": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

