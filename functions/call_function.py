
from google.genai import types

from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .run_python_file import run_python_file
from .write_file import write_file


def call_function(function_call_part, verbose=False):
	"""
	Dispatch and execute a tool function based on a FunctionCall part.

	Args:
		function_call_part: types.FunctionCall with .name and .args
		verbose (bool): whether to print detailed call information

	Returns:
		types.Content: A tool response content with a function_response part.
	"""

	function_name = getattr(function_call_part, "name", None)
	raw_args = getattr(function_call_part, "args", {}) or {}

	# Print according to verbosity
	if verbose:
		print(f"Calling function: {function_name}({raw_args})")
	else:
		print(f" - Calling function: {function_name}")

	# Build kwargs, always inject working_directory
	try:
		kwargs = dict(raw_args)
	except Exception:
		# Fallback if args isn't a standard mapping
		kwargs = raw_args

	# Security-controlled working directory (LLM cannot override)
	kwargs["working_directory"] = "./calculator"

	# Optional arg compatibility shims
	if function_name in ("run_python_file", "get_file_content"):
		if "file_path" not in kwargs and "file" in kwargs:
			kwargs["file_path"] = kwargs.pop("file")

	# Function registry
	registry = {
		"get_files_info": get_files_info,
		"get_file_content": get_file_content,
		"run_python_file": run_python_file,
		"write_file": write_file,
	}

	func = registry.get(function_name)
	if func is None:
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=function_name,
					response={"error": f"Unknown function: {function_name}"},
				)
			],
		)

	try:
		function_result = func(**kwargs)
	except TypeError as e:
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=function_name,
					response={"error": f"Argument error: {str(e)}"},
				)
			],
		)
	except Exception as e:
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=function_name,
					response={"error": f"Execution error: {str(e)}"},
				)
			],
		)

	return types.Content(
		role="tool",
		parts=[
			types.Part.from_function_response(
				name=function_name, response={"result": function_result}
			)
		],
	)



