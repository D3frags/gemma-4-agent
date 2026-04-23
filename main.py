import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    print(f"{response.text}")


def normal_output(response):
    print(f"{response.text}")


def main():
    client = genai.Client(api_key=api_key)
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    if response.usage_metadata is None:
        raise RuntimeError("")
    verbose_output(args, response) if args.verbose else normal_output(response)


if __name__ == "__main__":
    main()
