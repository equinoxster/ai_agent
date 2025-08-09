import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

    model = "gemini-2.0-flash-001"
    contents = messages
    response = client.models.generate_content(
        model=model, 
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=system_prompt),)
    print(response.text)

    if verbose:
        print(f"User prompt: {user_prompt} ")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


main()
