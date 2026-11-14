# Smart Todo & Task Manager

## Objective

Develop a deterministic task management application
using Python and Spec-Driven Development.

## Functional Requirements

FR-01: Users can create tasks.

FR-02: Users can view all tasks.

FR-03: Users can update existing tasks.

FR-04: Users can delete tasks.

FR-05: Users can assign priorities:
High, Medium, Low.

FR-06: Users can assign task statuses:
Pending, In Progress, Completed.

FR-07: Users can filter tasks by priority,
status, and tags.

FR-08: Tasks must be stored persistently
in a JSON file.

## Non-Functional Requirements

NFR-01: The application must be deterministic.

NFR-02: Invalid inputs must be handled safely.

NFR-03: The application must support automated tests.

NFR-04: The application must use Python.

## Acceptance Criteria

AC-01: Creating a task generates a unique ID.

AC-02: Created tasks appear in the task list.

AC-03: Updating a task changes the correct record.

AC-04: Deleting a task removes the correct record.

AC-05: Filtering returns only matching tasks.

AC-06: Tasks persist after restarting the application.

AC-07: Invalid priority and status values are rejected.

AC-08: Automated tests validate the requirements.