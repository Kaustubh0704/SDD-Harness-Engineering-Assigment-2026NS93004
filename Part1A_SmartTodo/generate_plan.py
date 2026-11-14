import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR.parent / ".env")

os.environ["HTTP_PROXY"] = "http://rb-proxy-in.bosch.com:8080"
os.environ["HTTPS_PROXY"] = "http://rb-proxy-in.bosch.com:8080"

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    timeout=30.0,
    max_retries=0,
)

spec_path = BASE_DIR / "specs" / "001-smart-todo-manager" / "spec.md"
design_path = BASE_DIR / "specs" / "design.md"
constitution_path = BASE_DIR / ".specify" / "memory" / "constitution.md"

spec = spec_path.read_text(encoding="utf-8")
design = design_path.read_text(encoding="utf-8")
constitution = constitution_path.read_text(encoding="utf-8")

prompt = f"""
Prepare a retrospective implementation plan for an existing
Python Smart Todo Manager application.

Use the following project documentation.

CONSTITUTION:
{constitution}

FEATURE SPECIFICATION:
{spec}

TECHNICAL DESIGN:
{design}

Generate Markdown with these sections:

1. Project Overview
2. Technology Stack
3. Architecture
4. Data Model
5. JSON Persistence Strategy
6. Implementation Components
7. Testing Harness Strategy
8. Quality and Security Validation
9. Requirement-to-Implementation Traceability
10. Known Limitations

Important:
- This application is already implemented.
- Do not claim that implementation occurred after this plan.
- Do not invent test results.
- Do not invent source files or methods.
- Clearly identify any assumptions requiring verification.
- Do not include API keys.
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a software architecture documentation assistant. "
                "Generate accurate, structured Markdown."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ],
    reasoning_effort="low",
    max_tokens=3500,
)

content = response.choices[0].message.content

if not content:
    raise ValueError("Groq returned an empty response")

output_path = BASE_DIR / "specs" / "001-smart-todo-manager" / "plan.md"

if output_path.exists():
    raise FileExistsError(
        "plan.md already exists. Review it before replacing."
    )

output_path.write_text(content, encoding="utf-8")

print("Draft implementation plan generated:")
print(output_path)