import argparse
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")


def main():
    client = genai.Client(api_key=api_key)
    args = parser.parse_args()
    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents=args.user_prompt,
    )
    if response.usage_metadata is None:
        raise RuntimeError("")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)


if __name__ == "__main__":
    main()
