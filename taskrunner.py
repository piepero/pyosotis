import sample_tasks


class Task:
    def __init__(self, task_name, task_proc):
        self.name = task_name
        self.proc = task_proc
        self.data = task_proc()

    def __str__(self):
        return f"Task name: {self.name}"

    def is_due(self, finished_task_names):
        if not "requires" in self.data:
            return True
        for req in self.data["requires"]:
            if not req.__name__ in finished_task_names:
                return False
        return True


all_tasks = [
    Task(item, getattr(sample_tasks, item))
    for item in dir(sample_tasks)
    if item.startswith("task_")
]
finished_tasks = []  # [task for task in all_tasks if task.name == "task_clone_main"]
finished_task_names = [task.name for task in finished_tasks]

due_tasks = [task for task in all_tasks if task.is_due(finished_task_names)]
waiting_tasks = [task for task in all_tasks if not task.is_due(finished_task_names)]

print("All:")
for task in all_tasks:
    print(task)

print("Finished:")
for task in finished_tasks:
    print(task)

print("Due:")
for task in due_tasks:
    print(task)
print("Waiting:")
for task in waiting_tasks:
    print(task)
