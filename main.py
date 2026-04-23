import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")


def verbose_output(args, response):
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if not response.function_calls:
        print(response.text)
    else:
        for fc in response.function_calls:
            print(f"Calling function: {fc.name}({fc.args})")


def normal_output(response):
    for fc in response.function_calls:
        print(f"Calling function: {fc.name}({fc.args})")


def main():
    client = genai.Client(api_key=api_key)
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    for _ in range(20):
        response = client.models.generate_content(
            # model="gemma-4-26b-a4b-it",
            model="gemini-2.5-flash",
            contents=messages,
            # config=types.GenerateContentConfig(system_instruction=system_prompt),
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        if response.candidates:
            for c in response.candidates:
                messages.append(c.content)

        if not response.function_calls:
            print("Final response:")
            print(response.text)
            return

        if response.usage_metadata is None:
            raise RuntimeError("missing usage_metadata")
        verbose_output(args, response) if args.verbose else normal_output(response)
        function_responses = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            inner_response = function_call_result.parts[0].function_response.response
            if inner_response is None:
                raise Exception("no response in function call result")
            function_responses.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        messages.append(types.Content(role="user", parts=function_responses))
    else:
        print("Max iterations reached without a final response")
        sys.exit(1)


if __name__ == "__main__":
    main()
