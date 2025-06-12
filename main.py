import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def main():
    if len(sys.argv) < 2 or sys.argv[1] == None:
        print("Prompt value not found!")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"
    contents = sys.argv[1]
    response = client.models.generate_content(model=model, contents=contents)
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


main()
