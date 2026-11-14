import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

# Load the existing API key
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found")

# Corporate proxy
os.environ["HTTP_PROXY"] = "http://rb-proxy-in.bosch.com:8080"
os.environ["HTTPS_PROXY"] = "http://rb-proxy-in.bosch.com:8080"

client = Groq(
    api_key=api_key,
    timeout=30.0,
    max_retries=0
)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly one word: Hello"
        }
    ],
    reasoning_effort="low",
    max_tokens=200
)

print("Groq Response:", response.choices[0].message.content)