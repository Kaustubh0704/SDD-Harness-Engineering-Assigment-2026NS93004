import json
import time
from datetime import datetime
from pathlib import Path

from src.reminder_agent import ReminderAgent

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "evals" / "reminder_cases.json"
EVIDENCE_DIR = BASE_DIR / "evidence"

EVIDENCE_DIR.mkdir(exist_ok=True)

REQUIRED_FIELDS = {
    "action",
    "title",
    "date",
    "time",
    "status",
    "missing_fields",
    "duration_minutes",
    "clarification_question",
}


def validate_schema(result):
    if not isinstance(result, dict):
        return False

    if set(result.keys()) != REQUIRED_FIELDS:
        return False

    if result["action"] not in {"create", "reschedule", "snooze"}:
        return False

    if result["status"] not in {"scheduled", "needs_clarification"}:
        return False

    if result["title"] is not None:
        if not isinstance(result["title"], str):
             return False

    if not isinstance(result["missing_fields"], list):
        return False

    if result["clarification_question"] is not None:
        if not isinstance(result["clarification_question"], str):
            return False


    duration = result["duration_minutes"]

    if duration is not None:
        if type(duration) is not int or duration <= 0:
            return False

    return True


def evaluate_case(expected, actual):
    checks = {}

    for field in [
    "action",
    "date",
    "time",
    "status",
    "duration_minutes"
    ]:
        checks[field] = actual.get(field) == expected.get(field)

    return checks


def main():
    cases = json.loads(DATASET_PATH.read_text(encoding="utf-8"))

    agent = ReminderAgent()
    results = []

    print("AI REMINDER AGENT - EVALUATION HARNESS")
    print("=" * 45)

    for case in cases:
        print(f"\nEvaluating {case['id']}...", flush=True)

        record = {
            "id": case["id"],
            "input": case["input"],
            "expected": case["expected"],
        }

        try:
            actual = agent.process_reminder(
                case["input"],
                reference_datetime=case["reference_datetime"],
            )

            schema_valid = validate_schema(actual)

            checks = (
                evaluate_case(case["expected"], actual)
                if schema_valid
                else {}
            )

            passed = schema_valid and all(checks.values())

            record.update({
                "actual": actual,
                "schema_valid": schema_valid,
                "checks": checks,
                "passed": passed,
            })

            print("PASS" if passed else "FAIL")

        except Exception as error:
            record.update({
                "actual": None,
                "schema_valid": False,
                "checks": {},
                "passed": False,
                "error": f"{type(error).__name__}: {error}",
            })

            print(f"ERROR: {type(error).__name__}")

        results.append(record)

        # Avoid sending requests too quickly
        time.sleep(2)

    total = len(results)
    passed = sum(result["passed"] for result in results)
    failed = total - passed

    report = {
        "timestamp": datetime.now().isoformat(),
        "model": agent.model,
        "total_cases": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / total * 100, 2) if total else 0,
        "results": results,
    }

    report_path = EVIDENCE_DIR / "evaluation_report.json"

    report_path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )

    print("\n" + "=" * 45)
    print("EVALUATION SUMMARY")
    print(f"Total Cases: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Pass Rate: {report['pass_rate']}%")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()