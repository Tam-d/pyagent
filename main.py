import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

def handle_args():
    parser = argparse.ArgumentParser(description="pyagent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    print("*********Arguments*********")
    for arg, val in vars(args).items():
        print(f"{arg}: {val}")

    return args

def main():
    load_dotenv()
    args = handle_args()

    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("Key not found")
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0
        ),
    )

    #print(f"---GenerateContentResponse---\n{response}\n")

    prompt_tokens = 0
    response_tokens = 0
    usage_mdt = response.usage_metadata
    function_calls = response.function_calls

    if usage_mdt is not None:
        prompt_tokens = usage_mdt.prompt_token_count
        response_tokens = usage_mdt.candidates_token_count
    else:
        raise RuntimeError("Usage metadata not found")
    
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    function_results = []

    if function_calls:
        for function_call in function_calls:
            # print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call)

            function_parts = function_call_result.parts
            
            if not function_call_result.parts or len(function_parts) == 0:
                raise Exception("Function call result did not have any parts")
            
            function_part = function_call_result.parts[0]
            function_response = function_part.function_response

            if not function_response:
                raise Exception("Function call parts did not have a function response")
            
            if not function_response.response:
                raise Exception("The functions response was empty")
            
            function_results.append(function_part)

            if args.verbose == True:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(f"Response:\n {response.text}")


if __name__ == "__main__":
    main()
