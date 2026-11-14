# AI Reminder Agent - Technical Design

## 1. Objective

Build an AI-powered reminder agent that converts
natural-language instructions into structured JSON.

## 2. Architecture

The application consists of four components:

1. User Input
2. Reminder Agent
3. Groq LLM API
4. JSON Response Validator

## 3. Technology Stack

- Python 3.12
- Groq Python SDK
- Model: openai/gpt-oss-20b
- JSON
- python-dotenv
- Automated evaluation harness

## 4. Supported Operations

### Create Reminder

Example:
"Remind me to submit my assignment tomorrow at 9 PM."

### Reschedule Reminder

Example:
"Move my assignment reminder to Monday at 10 AM."

### Snooze Reminder

Example:
"Snooze my assignment reminder for 30 minutes."

### Missing Information

Example:
"Remind me to call my friend."

The agent must identify missing scheduling information
rather than inventing a date or time.

## 5. Output Schema

The agent must return JSON containing:

- action
- title
- date
- time
- status
- missing_fields
- duration_minutes
- clarification_question

Example:

{
  "action": "create",
  "title": "Submit assignment",
  "date": "2026-11-15",
  "time": "21:00",
  "status": "scheduled",
  "missing_fields": [],
  "duration_minutes": null,
  "clarification_question": null
}

## 6. Validation Rules

- Output must be valid JSON.
- Action must be create, reschedule, or snooze.
- Dates must use YYYY-MM-DD.
- Times must use HH:MM in 24-hour format.
- Missing information must not be fabricated.
- Ambiguous instructions must request clarification.
- Relative dates must be interpreted using an
  explicitly supplied reference date and timezone.

  ## Snooze Validation Rules

- Snooze duration must be represented using duration_minutes.
- A duration of one hour must be represented as 60.
- A duration of 30 minutes must be represented as 30.
- The agent must not claim that an existing reminder
  has been modified.
- A reminder identifier or existing reminder context
  is required before applying a snooze operation.
- When the existing reminder cannot be identified,
  status must be needs_clarification.
- The agent may still extract the requested duration
  even when clarification is required.
- The agent only interprets reminder instructions.
  It does not execute or persist reminder changes.

## 7. Evaluation Strategy

The evaluation harness must contain at least
15 test cases covering:

- Simple reminders
- Relative dates
- Explicit dates
- Missing information
- Ambiguous instructions
- Rescheduling
- Snoozing
- Invalid inputs


## 8. Evaluation Metrics

The harness will measure:

1. JSON validity
2. Schema compliance
3. Action classification accuracy
4. Date extraction accuracy
5. Time extraction accuracy
6. Missing-information detection accuracy
7. Snooze-duration extraction accuracy
8. Clarification behavior accuracy
9. Overall evaluation pass rate

## 9. Non-Deterministic Behavior

LLM responses may vary between executions.

The evaluation harness must validate observable
behavior rather than relying exclusively on
exact text matching.

## 10. Security

- API keys must be stored in .env.
- API keys must never appear in logs.
- User input must not override system instructions.
- API errors must be handled safely.