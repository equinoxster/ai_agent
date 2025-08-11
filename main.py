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

    When a user asks a question or makes a request, make a function call plan and use the available tools to accomplish the task end-to-end:

    - List files and directories (get_files_info)
    - Read file contents (get_file_content)
    - Write or modify files (write_file)
    - Run a Python file with optional args (run_python_file)

    For bug fixes or changes:
    1) Reproduce the issue (e.g., run a file or tests),
    2) Propose a minimal code change,
    3) Apply the change by writing the file,
    4) Re-run to verify the fix,
    5) Summarize what changed and the result.

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    model = "gemini-2.0-flash-001"

    # Iteratively call the model, append candidates, run tools, append tool responses
    max_iterations = 20
    step = 0
    response = None

    while step < max_iterations:
        step += 1
        try:
            response = client.models.generate_content(
                model=model,
                contents=messages,  # Always pass the full conversation so the model continues from current state
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )

            # Add each candidate's content to the conversation history
            candidates = getattr(response, "candidates", None) or []
            for cand in candidates:
                content = getattr(cand, "content", None)
                if content is not None:
                    messages.append(content)

            # Execute any function calls and append tool responses
            function_calls = getattr(response, "function_calls", None) or []
            if len(function_calls) > 0:
                for function_call_part in function_calls:
                    function_call_result = call_function(function_call_part, verbose=verbose)

                    # Validate structure
                    try:
                        if not function_call_result.parts or not getattr(
                            function_call_result.parts[0], "function_response", None
                        ):
                            raise RuntimeError(
                                "Invalid tool response structure: missing function_response part"
                            )
                    except Exception:
                        # Print and stop if tool response is malformed
                        print(
                            "Error: Invalid tool response structure: missing function_response part",
                            file=sys.stderr,
                        )
                        break

                    if verbose:
                        print(
                            f"-> {function_call_result.parts[0].function_response.response}"
                        )

                    # Append tool response message back into the conversation
                    messages.append(function_call_result)

                # Continue loop to let the model consume the tool outputs
                continue

            # If the model returned final text and there are no tool calls, we're done
            if getattr(response, "text", None):
                print(response.text)
                break

            # Neither final text nor tool calls: iterate again until max iterations
            continue

        except Exception as e:
            print(f"Error during generate_content at step {step}: {e}", file=sys.stderr)
            break

    if verbose and response is not None:
        print(f"User prompt: {user_prompt} ")
        if getattr(response, "usage_metadata", None):
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(
                f"Response tokens: {response.usage_metadata.candidates_token_count}"
            )


main()
