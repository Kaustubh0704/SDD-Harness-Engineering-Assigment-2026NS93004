from src.todo import TaskManager

manager = TaskManager()

task = manager.create_task(
    title="Complete SDD Assignment",
    description="Finish Part 1A implementation",
    priority="High",
    status="Pending",
    tags=["college", "assignment"]
)

print("Task created successfully!")
print(task)