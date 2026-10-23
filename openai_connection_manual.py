
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load the secret key from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print("Key found:", bool(api_key))
print("Key prefix:", repr(api_key[:12]) if api_key else "Missing")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found. Check your .env file."
    )

client = OpenAI(api_key=api_key)

try:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input="Reply with exactly: OpenAI connection successful."
    )

    print(response.output_text)

except Exception as error:
    print("OpenAI request failed.")
    print(f"Error type: {type(error).__name__}")
    print(f"Error details: {error}")