import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.todo import TaskManager

with tempfile.TemporaryDirectory() as temp_dir:

    file_path = Path(temp_dir) / "tasks.json"
    manager = TaskManager(file_path)

    # Test 1: Create
    task = manager.create_task(
        title="Complete Assignment",
        priority="High",
        tags=["college"]
    )

    assert task["id"] == 1
    print("PASS: Create Task")

    # Test 2: View
    tasks = manager.get_all_tasks()

    assert len(tasks) == 1
    print("PASS: View Tasks")

    # Test 3: Update
    updated = manager.update_task(
        1,
        status="Completed"
    )

    assert updated["status"] == "Completed"
    print("PASS: Update Task")

    # Test 4: Filter
    filtered = manager.filter_tasks(
        status="Completed"
    )

    assert len(filtered) == 1
    print("PASS: Filter Tasks")

    # Test 5: Persistence
    reloaded_manager = TaskManager(file_path)

    assert len(reloaded_manager.get_all_tasks()) == 1
    print("PASS: JSON Persistence")

    # Test 6: Delete
    manager.delete_task(1)

    assert len(manager.get_all_tasks()) == 0
    print("PASS: Delete Task")

print("\nAll basic CRUD tests passed!")