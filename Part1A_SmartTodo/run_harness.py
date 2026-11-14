import subprocess
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = BASE_DIR / "evidence"

EVIDENCE_DIR.mkdir(exist_ok=True)

TEST_FILES = [
    "test_crud.py",
    "test_validation.py",
    "test_edge_cases.py"
]

results = []

print("SMART TODO - AUTOMATED TEST HARNESS")
print("=" * 45)

for test_file in TEST_FILES:

    print(f"\nExecuting: {test_file}")

    process = subprocess.run(
        [
            sys.executable,
            str(BASE_DIR / "tests" / test_file)
        ],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    status = "PASS" if process.returncode == 0 else "FAIL"

    results.append({
        "test": test_file,
        "status": status,
        "exit_code": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr
    })

    print(f"Result: {status}")

passed = sum(
    result["status"] == "PASS"
    for result in results
)

failed = len(results) - passed

report_lines = [
    "SMART TODO - HARNESS EXECUTION REPORT",
    "=" * 45,
    f"Execution Time: {datetime.now().isoformat()}",
    f"Test Suites: {len(results)}",
    f"Passed Suites: {passed}",
    f"Failed Suites: {failed}",
    ""
]

for result in results:

    report_lines.extend([
        f"Test: {result['test']}",
        f"Status: {result['status']}",
        f"Exit Code: {result['exit_code']}",
        "STDOUT:",
        result["stdout"],
        "STDERR:",
        result["stderr"],
        "-" * 45
    ])

report = "\n".join(report_lines)

report_path = EVIDENCE_DIR / "harness_report.txt"

report_path.write_text(report, encoding="utf-8")

print("\n" + "=" * 45)
print("HARNESS SUMMARY")
print(f"Passed Suites: {passed}")
print(f"Failed Suites: {failed}")
print(f"Report: {report_path}")

sys.exit(1 if failed else 0)