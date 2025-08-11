import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def main():
    if len(sys.argv) < 2 or sys.argv[1] is None:
        print("Prompt value not found!")
        sys.exit(1)

    user_prompt = sys.argv[1]
    verbose = False
    for arg in sys.argv:
        if arg.startswith("--"):
            match arg[2:]:
                case "verbose":
                    verbose = True
                case _:
                    pass
    client = genai.Client(api_key=api_key)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )


    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    model = "gemini-2.0-flash-001"
    contents = messages
    response = client.models.generate_content(
        model=model, 
        contents=contents,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),)
    print(response.text)
    if (len(response.function_calls) > 0):
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose=verbose)
            # Validate structure
            try:
                if not function_call_result.parts or not getattr(function_call_result.parts[0], "function_response", None):
                    raise RuntimeError("Invalid tool response structure: missing function_response part")
            except Exception:
                raise RuntimeError("Invalid tool response structure: missing function_response part")

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    

    if verbose:
        print(f"User prompt: {user_prompt} ")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


main()
