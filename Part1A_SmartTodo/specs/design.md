# Smart Todo Manager - Technical Design

## 1. Architecture

The application will use a simple layered architecture:

1. User Interface
2. Task Management Logic
3. JSON Persistence Layer

The application will be implemented using Python.

## 2. Task Data Model

Each task will contain:

- id: Unique integer
- title: String
- description: String
- priority: High, Medium, or Low
- status: Pending, In Progress, or Completed
- tags: List of strings

Example:

{
  "id": 1,
  "title": "Complete Assignment",
  "description": "Finish SDD assignment",
  "priority": "High",
  "status": "Pending",
  "tags": ["college", "assignment"]
}

## 3. Core Components

### TaskManager

Responsible for managing tasks.

Methods:

- create_task()
- get_all_tasks()
- update_task()
- delete_task()
- filter_tasks()

### JSONStorage

Responsible for storing and retrieving tasks.

Methods:

- load_tasks()
- save_tasks()

## 4. Validation Rules

- Task title cannot be empty.
- Priority must be High, Medium, or Low.
- Status must be Pending, In Progress, or Completed.
- Task IDs must be unique.
- Updating a nonexistent task must return an error.
- Deleting a nonexistent task must return an error.

## 5. Persistence

Tasks will be stored in:

data/tasks.json

The application must load existing tasks when started.

Changes must be saved after successful operations.

## 6. Testing Strategy

The testing harness will verify:

- Task creation
- Task retrieval
- Task updates
- Task deletion
- Priority validation
- Status validation
- Filtering
- JSON persistence
- Invalid input handling

## 7. Deterministic Behavior

Given the same input and initial application state,
the application must produce the same result.

Task IDs will be generated sequentially.

## 8. Error Handling

The application will use explicit exceptions
for invalid operations.

Examples:

- ValueError for invalid input.
- KeyError for nonexistent task IDs.
- Storage errors for invalid or inaccessible JSON files.