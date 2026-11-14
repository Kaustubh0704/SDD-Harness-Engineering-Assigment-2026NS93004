# AI-Powered Reminder Agent

## 1. Objective

Develop an AI-powered reminder agent using Python
and the Google Gemini API.

The application shall interpret natural-language
reminder requests and return structured JSON.

## 2. Functional Requirements

FR-01: Accept natural-language reminder requests.

FR-02: Extract the reminder title.

FR-03: Extract dates and times from user requests.

FR-04: Support relative dates such as tomorrow.

FR-05: Identify missing information.

FR-06: Support reminder creation.

FR-07: Support reminder rescheduling.

FR-08: Support reminder snoozing.

FR-09: Return structured JSON responses.

FR-10: Handle Gemini API failures gracefully.

## 3. Non-Functional Requirements

NFR-01: Use Python.

NFR-02: Use the Gemini API.

NFR-03: Protect API credentials.

NFR-04: Validate the structure of AI responses.

NFR-05: Support automated evaluation.

NFR-06: Handle non-deterministic AI outputs.

## 4. Acceptance Criteria

AC-01: Extract reminder titles correctly.

AC-02: Extract explicit dates and times.

AC-03: Resolve relative dates using a supplied
reference date and timezone.

AC-04: Return valid JSON.

AC-05: Identify missing required information.

AC-06: Recognize create, reschedule, and snooze intents.

AC-07: Return a controlled error when the API fails.

AC-08: Evaluate at least 15 test cases.

AC-09: Generate an automated evaluation report.

AC-10: Record actual evaluation results.