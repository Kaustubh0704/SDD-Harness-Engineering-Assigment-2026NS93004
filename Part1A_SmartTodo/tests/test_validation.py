import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.todo import TaskManager


def expect_error(action, expected_error, test_name):
    try:
        action()
    except expected_error:
        print(f"PASS: {test_name}")
    except Exception as error:
        raise AssertionError(
            f"{test_name}: Unexpected error {type(error).__name__}"
        ) from error
    else:
        raise AssertionError(
            f"{test_name}: Expected {expected_error.__name__}"
        )


with tempfile.TemporaryDirectory() as temp_dir:

    manager = TaskManager(Path(temp_dir) / "tasks.json")

    # Test 1: Empty title
    expect_error(
        lambda: manager.create_task(title=""),
        ValueError,
        "Empty Title Validation"
    )

    # Test 2: Invalid priority
    expect_error(
        lambda: manager.create_task(
            title="Test Task",
            priority="Urgent"
        ),
        ValueError,
        "Invalid Priority Validation"
    )

    # Test 3: Invalid status
    expect_error(
        lambda: manager.create_task(
            title="Test Task",
            status="Unknown"
        ),
        ValueError,
        "Invalid Status Validation"
    )

    # Test 4: Update nonexistent task
    expect_error(
        lambda: manager.update_task(
            999,
            status="Completed"
        ),
        KeyError,
        "Update Nonexistent Task"
    )

    # Test 5: Delete nonexistent task
    expect_error(
        lambda: manager.delete_task(999),
        KeyError,
        "Delete Nonexistent Task"
    )

    # Test 6: Invalid filter
    expect_error(
        lambda: manager.filter_tasks(priority="Urgent"),
        ValueError,
        "Invalid Filter Validation"
    )

print("\nAll validation tests passed!")