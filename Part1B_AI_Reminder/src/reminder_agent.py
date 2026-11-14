import json
import os
import re

from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from groq import Groq


class ReminderAgent:

    def __init__(self):
        env_path = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(env_path)

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found")

        os.environ["HTTP_PROXY"] = "http://rb-proxy-in.bosch.com:8080"
        os.environ["HTTPS_PROXY"] = "http://rb-proxy-in.bosch.com:8080"
        self.client = Groq(
            api_key=api_key,
            timeout=30.0,
            max_retries=0
        )
    self.model = "openai/gpt-oss-20b"
    def resolve_relative_date(self, user_input, reference_datetime):

        reference = datetime.fromisoformat(reference_datetime)

        text = user_input.lower()

        if re.search(r"\btomorrow\b", text):
            return (
                reference + timedelta(days=1)
            ).strftime("%Y-%m-%d")

        if re.search(r"\btoday\b", text):
            return reference.strftime("%Y-%m-%d")

        weekdays = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6
        }

        for day_name, target_weekday in weekdays.items():

            if re.search(rf"\bnext {day_name}\b", text):

                days_ahead = (
                    target_weekday - reference.weekday()
                ) % 7

                if days_ahead == 0:
                    days_ahead = 7

                return (
                    reference + timedelta(days=days_ahead)
                ).strftime("%Y-%m-%d")

        return None


    def process_reminder(self, user_input, reference_datetime=None):

        if not isinstance(user_input, str) or not user_input.strip():
            raise ValueError("Reminder instruction cannot be empty")

        if reference_datetime is None:
            reference_datetime = datetime.now(
                ZoneInfo("Asia/Kolkata")
            ).isoformat()

        system_prompt = """
You are an AI Reminder Agent.

Convert natural-language reminder instructions into
structured JSON.

Supported actions:
- create
- reschedule
- snooze

Return exactly these 8 JSON fields:
- action
- title
- date
- time
- status
- missing_fields
- duration_minutes
- clarification_question

Rules:

1. Return valid JSON only.
2. Do not include Markdown formatting.
3. Date format must be YYYY-MM-DD.
4. Time format must be HH:MM in 24-hour format.
5. Use null for missing dates and times.
6. Never invent missing information.
7. Use the supplied reference datetime and Asia/Kolkata timezone.
8. Interpret relative dates carefully.

For CREATE:
- Extract the reminder title, date and time.
- If the date or time is missing, request clarification.
- Set duration_minutes to null.

For RESCHEDULE:
- Extract the requested new date and time.
- Do not claim an existing reminder was modified.
- Set duration_minutes to null.

For SNOOZE:
- Extract the snooze duration in minutes.
- One hour means 60 minutes.
- Thirty minutes means 30 minutes.
- Do not calculate a new reminder date or time
  without the existing reminder schedule.
- Set date and time to null when unavailable.
- If the target reminder cannot be uniquely identified,
  use status needs_clarification.
- Include reminder_id in missing_fields when the
  existing reminder cannot be identified.
- Ask a clarification question.

RELATIVE DATE RULES:

1. "Today" is an explicit relative date.
   Resolve it to the reference calendar date.

2. "Tomorrow" is an explicit relative date.
   Resolve it to the day after the reference date.

3. "Next Friday" means the first Friday strictly
   after the reference date.

4. If the instruction contains only a time without
   a date expression, do not invent a date.

5. When a date is provided but the time is vague
   (such as "morning"), resolve the date but
   set time to null and request clarification.

6. Never substitute tomorrow for a requested weekday.

7. Return valid JSON directly without explanations.

Allowed status values:
- scheduled
- needs_clarification

The agent only interprets reminder instructions.
It does not execute or persist reminder changes.
"""


        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": (
                        f"Reference datetime: {reference_datetime}\n"
                        f"Instruction: {user_input}"
                    ),
                },
            ],
            temperature=0,
            reasoning_effort="low",
            max_tokens=1200,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "reminder_result",
                    "strict": False,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "enum": ["create", "reschedule", "snooze"],
                            },
                            "title": {
                                "type": ["string", "null"],
                            },
                            "date": {
                                "type": ["string", "null"],
                            },
                            "time": {
                                "type": ["string", "null"],
                            },
                            "status": {
                                "type": "string",
                                "enum": [
                                    "scheduled",
                                    "needs_clarification",
                                ],
                            },
                            "missing_fields": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "duration_minutes": {
                                "type": ["integer", "null"],
                            },
                            "clarification_question": {
                                "type": ["string", "null"],
                            },
                        },
                        "required": [
                            "action",
                            "title",
                            "date",
                            "time",
                            "status",
                            "missing_fields",
                            "duration_minutes",
                            "clarification_question",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
        )

        choice = response.choices[0]
        content = choice.message.content

        if not content:
            finish_reason = choice.finish_reason
            usage = response.usage

            raise ValueError(
                "AI returned an empty response. "
                f"Finish reason: {finish_reason}. "
                f"Token usage: {usage}"
            )

        try:
            result = json.loads(content)

        except json.JSONDecodeError as error:
            raise ValueError(
                "AI returned invalid JSON"
            ) from error

        resolved_date = self.resolve_relative_date(
            user_input,
            reference_datetime
        )

        if resolved_date and result.get("action") == "create":

            result["date"] = resolved_date

            missing_fields = result.get("missing_fields", [])

            result["missing_fields"] = [
                field for field in missing_fields
                if field != "date"
            ]

            if result.get("time") is not None:
                result["status"] = "scheduled"
                result["clarification_question"] = None

            else:
                result["status"] = "needs_clarification"

                if "time" not in result["missing_fields"]:
                    result["missing_fields"].append("time")

                result["clarification_question"] = (
                    "What exact time should I set for this reminder?"
                )

        if (
            result.get("action") == "create"
            and resolved_date is None
            and result.get("date") is not None
        ):
            # Only clear an inferred date when the input
            # contains no explicit calendar date.
            has_explicit_date = bool(
                re.search(
                    r"\b\d{4}-\d{2}-\d{2}\b"
                    r"|\b\d{1,2}\s+"
                    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|"
                    r"apr(?:il)?|may|jun(?:e)?|jul(?:y)?|"
                    r"aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|"
                    r"nov(?:ember)?|dec(?:ember)?)"
                    r"\s+\d{4}\b",
                    user_input,
                    flags=re.IGNORECASE,
                )
            )

            if not has_explicit_date:
                result["date"] = None
                result["status"] = "needs_clarification"

                missing = result.get("missing_fields") or []

                if "date" not in missing:
                    missing.append("date")

                result["missing_fields"] = missing
                result["clarification_question"] = (
                    "On which date should I remind you?"
                )


        return result
