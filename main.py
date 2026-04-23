import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")


def verbose_output(args, response):
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if not response.function_calls:
        print(response.text)
    else:
        for fc in response.function_calls:
            print(f"Calling function: {fc.name}({fc.args})")


def normal_output(response):
    if not response.function_calls:
        print(response.text)
    else:
        for fc in response.function_calls:
            print(f"Calling function: {fc.name}({fc.args})")


def main():
    client = genai.Client(api_key=api_key)
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        # model="gemini-2.5-pro",
        contents=messages,
        # config=types.GenerateContentConfig(system_instruction=system_prompt),
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.usage_metadata is None:
        raise RuntimeError("")
    verbose_output(args, response) if args.verbose else normal_output(response)


if __name__ == "__main__":
    main()
