import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    parser = argparse.ArgumentParser(description="pyagent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if api_key is None:
        raise RuntimeError("Key not found")
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages
    )

    print(f"---GenerateContentResponse---\n{response}\n")

    prompt_tokens = 0
    response_tokens = 0
    usage_mdt = response.usage_metadata

    if usage_mdt is not None:
        prompt_tokens = usage_mdt.prompt_token_count
        response_tokens = usage_mdt.candidates_token_count
    else:
        raise RuntimeError("Usage metadata not found")
    
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    print(f"Response:\n {response.text}")


if __name__ == "__main__":
    main()
