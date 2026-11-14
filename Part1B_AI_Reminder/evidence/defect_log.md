# AI Reminder Agent - Defect Log

## DEF-B001: Incorrect Relative Date Extraction

Test Case: TC009

Expected Date: 2026-11-20
Actual Date: 2026-11-15

Root Cause Hypothesis:
The model may not have correctly interpreted
the relative date "next Friday".

Proposed Fix:
Provide an explicit reference date and timezone.

Status: Open

## DEF-B002: Empty AI Response

Test Case: TC013

Expected:
Valid structured JSON response.

Actual:
ValueError: AI returned an empty response.

Root Cause:
Not yet confirmed.

Investigation:
Inspect raw API response metadata and finish reason.

Status: Open

## DEF-B003: Incorrect Snooze Handling

Test Case: TC014

Expected:
needs_clarification

Actual:
scheduled

Root Cause Hypothesis:
The model generated a snooze time without
access to the original reminder schedule.

Proposed Fix:
Require original reminder information before
calculating a snoozed time.

Status: Open