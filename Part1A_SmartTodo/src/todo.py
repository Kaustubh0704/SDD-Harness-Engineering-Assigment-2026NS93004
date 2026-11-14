import json
from pathlib import Path


class TaskManager:

    VALID_PRIORITIES = ("High", "Medium", "Low")

    VALID_STATUSES = ("Pending", "In Progress", "Completed")

    def __init__(self, file_path="data/tasks.json"):

        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.tasks = self.load_tasks()

    def load_tasks(self):

        if not self.file_path.exists():
            self.next_id = 1
            return []

        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            # Backward compatibility with existing JSON files
            tasks = data
            self.next_id = max(
                (task["id"] for task in tasks),
                default=0
            ) + 1
            return tasks

        self.next_id = data["next_id"]

        return data["tasks"]

    def save_tasks(self):

        data = {
            "next_id": self.next_id,
            "tasks": self.tasks
        }

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def create_task(
        self,
        title,
        description="",
        priority="Medium",
        status="Pending",
        tags=None
    ):

        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title must be a non-empty string")

        if priority not in self.VALID_PRIORITIES:
            raise ValueError("Invalid priority")

        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid status")

        if tags is None:
            tags = []

        task_id = self.next_id
        self.next_id += 1

        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": status,
            "tags": tags
        }

        self.tasks.append(task)

        self.save_tasks()

        return task

    def get_all_tasks(self):
        return [task.copy() for task in self.tasks]

    def update_task(self, task_id, **updates):

        allowed_fields = {
            "title", "description", "priority",
            "status", "tags"
        }

        if not updates:
            raise ValueError("No updates provided")

        if not set(updates).issubset(allowed_fields):
            raise ValueError("Invalid update field")

        if "title" in updates:
            title = updates["title"]

            if not isinstance(title, str) or not title.strip():
                raise ValueError("Task title cannot be empty")

        if "priority" in updates and updates["priority"] not in self.VALID_PRIORITIES:
                  raise ValueError("Invalid priority")

        if "status" in updates and updates["status"] not in self.VALID_STATUSES:
                  raise ValueError("Invalid status")

        if "description" in updates and not isinstance(updates["description"], str):
                  raise ValueError("Description must be a string")

        if "tags" in updates:
            tags = updates["tags"]

            if not isinstance(tags, list) or not all(
                isinstance(tag, str) for tag in tags
            ):
                raise ValueError("Tags must be a list of strings")

        for task in self.tasks:
            if task["id"] == task_id:
                task.update(updates)
                self.save_tasks()
                return task.copy()

        raise KeyError("Task not found")

    def delete_task(self, task_id):

        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                return True

        raise KeyError("Task not found")

    def filter_tasks(self, priority=None, status=None, tag=None):

        if priority is not None and priority not in self.VALID_PRIORITIES:
            raise ValueError("Invalid priority")

        if status is not None and status not in self.VALID_STATUSES:
            raise ValueError("Invalid status")

        results = self.tasks

        if priority is not None:
            results = [
                task for task in results
                if task["priority"] == priority
            ]

        if status is not None:
            results = [
                task for task in results
                if task["status"] == status
            ]

        if tag is not None:
            results = [
                task for task in results
                if tag in task["tags"]
            ]

        return [task.copy() for task in results]