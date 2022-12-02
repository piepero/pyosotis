import logging
import threading
import time

from .task import Task

logger = logging.getLogger(__name__)


class Runner:

    tasks = []
    due_tasks = []
    running_tasks = []
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
            task
            for task in self.tasks
            if task.is_due(finished_task_names) and not task in self.finished_tasks
        ]
        self.waiting_tasks = [
            task
            for task in self.tasks
            if not task.is_due(finished_task_names) and not task in self.finished_tasks
        ]

    def task_names(self):
        return [task.name for task in self.tasks]

    def due_task_names(self):
        return [task.name for task in self.due_tasks]

    def due_task_messages(self):
        return [task.message for task in self.due_tasks]

    def waiting_task_messages(self):
        return [task.message for task in self.waiting_tasks]

    def finished_task_messages(self):
        return [task.message for task in self.finished_tasks]

    def finish_due_task(self, due_task_index: int) -> None:
        self.set_finished(self.due_tasks[due_task_index])

    def set_finished(self, task: Task) -> None:
        if not task in self.finished_tasks:
            self.finished_tasks.append(task)

    def __str__(self):
        return "\n".join(
            [
                f"Runner({self.task_module_name}):",
                f"  tasks: [{', '.join(self.task_names())}]",
                f"  due: [{', '.join(self.due_task_names)}]",
                f"  waiting: [{', '.join([task.name for task in self.waiting_tasks])}]",
                f"  finished: [{', '.join([task.name for task in self.finished_tasks])}]",
            ]
        )
