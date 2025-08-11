import os
from google import genai

def get_file_content(working_directory, file_path):
    """
    Read and return the content of a file within the working directory.
    
    Args:
        working_directory (str): The base directory to work within
        file_path (str): Path to the file (relative to working_directory or absolute)
    
    Returns:
        str: The file content or an error message
    """
    working_dir_abs = os.path.abspath(working_directory)
    
    # If file_path is relative, resolve it relative to the working directory
    if not os.path.isabs(file_path):
        target_file_abs = os.path.abspath(os.path.join(working_directory, file_path))
    else:
        target_file_abs = os.path.abspath(file_path)
    
    # Normalize paths to handle .. and . properly
    working_dir_abs = os.path.normpath(working_dir_abs)
    target_file_abs = os.path.normpath(target_file_abs)
    
    # Check if target file is within the working directory
    if not (target_file_abs == working_dir_abs or target_file_abs.startswith(working_dir_abs + os.sep)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Check if the path exists and is a regular file
    if not os.path.exists(target_file_abs) or not os.path.isfile(target_file_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file_abs, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Truncate if content is longer than 10000 characters
        if len(content) > 10000:
            content = content[:10000] + f'\n\n[...File "{file_path}" truncated at 10000 characters]'
        
        return content
        
    except PermissionError:
        return f"Error: Permission denied reading file '{file_path}'"
    except UnicodeDecodeError:
        return f"Error: Cannot decode file '{file_path}' as UTF-8 text"
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found"
    except IsADirectoryError:
        return f"Error: '{file_path}' is a directory, not a file"
    except OSError as e:
        return f"Error: OS error reading file '{file_path}': {str(e)}"
    except IOError as e:
        return f"Error: I/O error reading file '{file_path}': {str(e)}"
    except Exception as e:
        return f"Error: Could not read file '{file_path}': {str(e)}"

schema_get_file_content = genai.types.FunctionDeclaration(
    name="get_file_content",
    description="Reads specified files content.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="Name of the file.",
            ),
        },
    ),
)