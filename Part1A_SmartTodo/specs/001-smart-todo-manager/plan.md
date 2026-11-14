# Smart Todo Manager - Retrospective Implementation Plan

## 1. Project Overview

Smart Todo Manager is a deterministic Python application
for managing tasks.

The application supports:

- Task creation
- Task retrieval
- Task updates
- Task deletion
- Filtering by priority, status, and tags
- JSON persistence
- Input validation

This document was prepared retrospectively after the
initial implementation and testing activities.

## 2. Technology Stack

- Python 3.12
- JSON file storage
- Python standard library
- Ruff for static code analysis
- Bandit for security scanning
- Custom Python testing harness
- PowerShell for local execution

## 3. Architecture

The application uses a simple structure:

1. TaskManager business logic
2. Input validation
3. JSON persistence
4. Independent testing harness

The TaskManager class contains the application logic
and persistence methods.

No separate database or web framework is used.

## 4. Data Model

Each task contains:

- id: Unique integer
- title: Non-empty string
- description: String
- priority: High, Medium, or Low
- status: Pending, In Progress, or Completed
- tags: List of strings

## 5. JSON Persistence

File:
data/tasks.json

The application stores:

- next_id
- tasks

The next_id counter prevents reuse of task IDs
after deletion.

Existing tasks are loaded when TaskManager initializes.

Successful mutations are saved to JSON.

The implementation also supports reading the earlier
list-based JSON structure for backward compatibility.

## 6. Implementation Components

### src/todo.py

Contains the TaskManager class.

Implemented methods:

- __init__()
- load_tasks()
- save_tasks()
- create_task()
- get_all_tasks()
- update_task()
- delete_task()
- filter_tasks()

Validation uses built-in Python exceptions.

## 7. Testing Strategy

Three test scripts are used:

### tests/test_crud.py

Validates:

- Create
- View
- Update
- Filter
- Persistence
- Delete

### tests/test_validation.py

Validates:

- Empty titles
- Invalid priorities
- Invalid statuses
- Nonexistent task updates
- Nonexistent task deletion
- Invalid filtering

### tests/test_edge_cases.py

Validates:

- Invalid title types
- Task ID uniqueness
- Update persistence
- Delete persistence

Tests use temporary directories to avoid modifying
the application's normal task data.

## 8. Automated Testing Harness

File:
run_harness.py

The harness:

1. Executes three Python test scripts.
2. Captures standard output and errors.
3. Records exit codes.
4. Reports suite-level pass/fail results.
5. Generates evidence/harness_report.txt.
6. Returns a nonzero exit code when a suite fails.

The latest verified execution completed with:

- 3 test suites passed
- 0 test suites failed
- 16 individual checks passed

## 9. Quality and Security

### Ruff

Command:
python -m ruff check src tests

Initial scan identified 9 issues.

After corrections, Ruff reported:
All checks passed!

### Bandit

Command:
python -m bandit -r src

Bandit reported:
No issues identified.

The scan reported zero high-, medium-, and
low-severity findings.

## 10. Defect Detection and Repair

### DEF-001: Invalid Title Type

Initial behavior:
Passing None as the title caused AttributeError.

Correction:
Added explicit string-type validation.

Verification:
The invalid-title edge-case test passed.

### DEF-002: Task ID Reuse

Initial behavior:
Deleting the highest-numbered task allowed
its ID to be reused.

Correction:
Introduced a persistent next_id counter.

Verification:
The task ID uniqueness test passed.

## 11. Requirement Traceability

US-01 Create Tasks:
src/todo.py -> tests/test_crud.py

US-02 View Tasks:
src/todo.py -> tests/test_crud.py

US-03 Update Tasks:
src/todo.py -> tests/test_crud.py

US-04 Delete Tasks:
src/todo.py -> tests/test_crud.py

US-05 Filter Tasks:
src/todo.py -> tests/test_crud.py

US-06 JSON Persistence:
src/todo.py -> tests/test_crud.py
and tests/test_edge_cases.py

Invalid Input Handling:
src/todo.py -> tests/test_validation.py

Task ID Uniqueness:
src/todo.py -> tests/test_edge_cases.py

Code Quality:
Ruff -> evidence/ruff_fixed.txt

Security:
Bandit -> evidence/bandit_results.txt

Harness Execution:
run_harness.py -> evidence/harness_report.txt

## 12. Known Limitations

- No graphical user interface.
- No user authentication.
- No concurrent file-write protection.
- No database integration.
- No automated CI/CD pipeline.
- No measured statement or branch coverage.
- JSON writes are not atomic.
- Legacy JSON files cannot recover IDs deleted
  before migration to the next_id format.

## 13. Documentation Provenance

The application and harness were implemented before
this formal implementation plan was generated.

The initial plan was generated using Groq and reviewed
for factual accuracy.

Incorrect generated implementation details were
removed during manual review.

This document is a retrospective engineering record,
not evidence that the Spec Kit planning command was
executed before implementation.