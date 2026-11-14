import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Corporate proxy
os.environ["HTTP_PROXY"] = "http://rb-proxy-in.bosch.com:8080"
os.environ["HTTPS_PROXY"] = "http://rb-proxy-in.bosch.com:8080"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    timeout=30.0,
    max_retries=0
)

print("Fetching available Groq models...\n")

models = client.models.list()

for model in models.data:
    print(model.id)