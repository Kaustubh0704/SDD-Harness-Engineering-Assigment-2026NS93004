import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

# Load API key from parent folder
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

# Configure Bosch corporate proxy for this process
os.environ["HTTP_PROXY"] = "http://rb-proxy-in.bosch.com:8080"
os.environ["HTTPS_PROXY"] = "http://rb-proxy-in.bosch.com:8080"

# Initialize Groq
client = Groq(
    api_key=api_key,
    timeout=30.0,
    max_retries=0
)

print("Connecting to Groq...", flush=True)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly one word: Hello"
        }
    ],
    max_tokens=100
)

print("Groq Response:")

message = response.choices[0].message

print("Content:", repr(message.content))
print("Finish Reason:", response.choices[0].finish_reason)
print("Model:", response.model)