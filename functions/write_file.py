import os

def write_file(working_directory, file_path, content):
    """
    Write content to a file within the working directory.
    
    Args:
        working_directory (str): The base directory to work within
        file_path (str): Path to the file (relative to working_directory or absolute)
        content (str): The content to write to the file
    
    Returns:
        str: Success message or an error message
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
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # Check if the path would create a file in a directory (not the file itself being a directory)
    if os.path.exists(target_file_abs) and os.path.isdir(target_file_abs):
        return f'Error: "{file_path}" is a directory, cannot write file content to it'
    
    # Create parent directories if they don't exist
    parent_dir = os.path.dirname(target_file_abs)
    if parent_dir and not os.path.exists(parent_dir):
        try:
            os.makedirs(parent_dir)
        except PermissionError:
            return f"Error: Permission denied creating directory structure for '{file_path}'"
        except Exception as e:
            return f"Error: Could not create directory structure for '{file_path}': {str(e)}"
    
    try:
        with open(target_file_abs, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except PermissionError:
        return f"Error: Permission denied writing to file '{file_path}'"
    except IsADirectoryError:
        return f"Error: '{file_path}' is a directory, not a file"
    except Exception as e:
        return f"Error: Could not write to file '{file_path}': {str(e)}"
