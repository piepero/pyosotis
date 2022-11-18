import logging

from .task import Task

logger = logging.getLogger(__name__)


class Runner:

    tasks = []
    due_tasks = []
    waiting_tasks = []
    finished_tasks = []

    def __init__(self, task_module):
        logger.debug("Runner(task_module.__name__):")
        self.task_module_name = task_module.__name__
        self.tasks = [
            Task(item, getattr(task_module, item))
            for item in dir(task_module)
            if item.startswith("task_")
        ]
        logger.debug(f"{len(self.tasks)} Tasks found.")

    def update_tasks(self):
        finished_task_names = [task.name for task in self.finished_tasks]

        self.due_tasks = [
            task for task in self.tasks if task.is_due(finished_task_names)
        ]
        self.waiting_tasks = [
            task for task in self.tasks if not task.is_due(finished_task_names)
        ]

    def __str__(self):
        return "\n".join(
            [
                f"Runner({self.task_module_name}):",
                f"  tasks: [{', '.join([task.name for task in self.tasks])}]",
                f"  due: [{', '.join([task.name for task in self.due_tasks])}]",
                f"  waiting: [{', '.join([task.name for task in self.waiting_tasks])}]",
                f"  finished: [{', '.join([task.name for task in self.finished_tasks])}]",
            ]
        )
