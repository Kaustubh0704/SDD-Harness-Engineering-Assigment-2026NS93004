# Smart Todo Manager

## Overview

A deterministic Python task management application developed
for the Spec-Driven Development and Harness Engineering assignment.

## Features

- Create tasks
- View tasks
- Update tasks
- Delete tasks
- Filter tasks by priority, status, and tags
- JSON data persistence
- Unique task IDs
- Input validation

## Technology Stack

- Python 3.12
- JSON
- Ruff
- Bandit
- GitHub Spec Kit
- Custom Python testing harness

## Project Structure

- `src/todo.py` - Application implementation
- `tests/test_crud.py` - CRUD tests
- `tests/test_validation.py` - Validation tests
- `tests/test_edge_cases.py` - Edge-case tests
- `run_harness.py` - Automated test runner
- `specs/` - Requirements and design documents
- `.specify/` - Spec Kit infrastructure
- `evidence/` - Actual test and scan results

## Running the Application

The application currently provides a Python TaskManager API.

Example:

```python
from src.todo import TaskManager

manager = TaskManager()

task = manager.create_task(
    title="Complete assignment",
    priority="High",
    tags=["college"]
)

print(task)
print(manager.get_all_tasks())
```

## Running the Automated Harness

From the Part1A_SmartTodo directory:

```powershell
python run_harness.py
```

## Code Quality

```powershell
python -m ruff check src tests
```

## Security Scan

```powershell
python -m bandit -r src
```

## Verified Results

- CRUD tests: 6 passed
- Validation tests: 6 passed
- Edge-case tests: 4 passed
- Automated harness: 3 suites passed
- Ruff: All checks passed
- Bandit: No issues identified

## Defect Detection and Repair

### DEF-001: Invalid Title Type

Originally, passing None as a task title caused AttributeError.

Fixed by adding explicit string-type validation.

### DEF-002: Task ID Reuse

Previously issued task IDs could be reused after deletion.

Fixed by implementing a persistent next_id counter.

## Spec Kit Documentation

The project contains:

- Constitution
- Feature specification
- Retrospective implementation plan
- Retrospective task breakdown

Spec Kit was initialized after the initial application
implementation.

The plan and task breakdown were prepared retrospectively
with AI assistance and manual review.

## Known Limitations

- No graphical user interface
- No user authentication
- No concurrent file-write protection
- No database integration
- No automated CI/CD pipeline
- No measured code coverage
- JSON writes are not atomic