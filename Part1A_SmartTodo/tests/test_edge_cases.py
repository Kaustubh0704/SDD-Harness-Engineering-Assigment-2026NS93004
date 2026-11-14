import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.todo import TaskManager


def run_test(name, action):
    try:
        action()
        print(f"PASS: {name}")
    except Exception as error:
        print(f"FAIL: {name} - {type(error).__name__}: {error}")
        raise


def test_invalid_title():
    with tempfile.TemporaryDirectory() as directory:
        manager = TaskManager(Path(directory) / "tasks.json")

        try:
            manager.create_task(title=None)
        except ValueError:
            return

        raise AssertionError("Expected ValueError for None title")


def test_unique_ids():
    with tempfile.TemporaryDirectory() as directory:
        manager = TaskManager(Path(directory) / "tasks.json")

        manager.create_task("Task 1")
        second = manager.create_task("Task 2")

        manager.delete_task(second["id"])

        third = manager.create_task("Task 3")

        assert third["id"] > second["id"], (
            "Previously issued task ID was reused"
        )


def test_update_persistence():
    with tempfile.TemporaryDirectory() as directory:
        file_path = Path(directory) / "tasks.json"

        manager = TaskManager(file_path)

        task = manager.create_task("Task 1")

        manager.update_task(
            task["id"],
            status="Completed"
        )

        reloaded = TaskManager(file_path)

        assert reloaded.get_all_tasks()[0]["status"] == "Completed"


def test_delete_persistence():
    with tempfile.TemporaryDirectory() as directory:
        file_path = Path(directory) / "tasks.json"

        manager = TaskManager(file_path)

        task = manager.create_task("Task 1")

        manager.delete_task(task["id"])

        reloaded = TaskManager(file_path)

        assert len(reloaded.get_all_tasks()) == 0


run_test("Invalid Title Type", test_invalid_title)
run_test("Unique Task IDs", test_unique_ids)
run_test("Update Persistence", test_update_persistence)
run_test("Delete Persistence", test_delete_persistence)