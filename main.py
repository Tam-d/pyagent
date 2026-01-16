import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    if api_key is None:
        raise RuntimeError("Key not found")
    
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=user_prompt
    )


    prompt_tokens = 0
    response_tokens = 0
    usage_mdt = response.usage_metadata

    if usage_mdt is not None:
        prompt_tokens = usage_mdt.prompt_token_count
        response_tokens = usage_mdt.candidates_token_count
    else:
        raise RuntimeError("Usage metadata not found")
    
    print(f"User Prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print(f"Response:\n {response.text}")


if __name__ == "__main__":
    main()
