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

    SharedDict = dict()

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
        """Update the status of all tasks."""

        # check running_tasks for completions
        for task in self.running_tasks:
            if not task.thread.is_alive():
                logger.debug(f"thread of task {task.name} has finished")
                self.finished_tasks.append(task)
                self.running_tasks.remove(task)

        finished_task_names = [task.name for task in self.finished_tasks]

        # all due tasks which are manual (i.e. without run command)
        self.due_tasks = [
            task
            for task in self.tasks
            if task.is_due(finished_task_names)
            and not task.data.get("run", None)
            and not task in self.finished_tasks
            and not task in self.running_tasks
        ]

        # all waiting tasks (i.e. unfinished and not yet due)
        self.waiting_tasks = [
            task
            for task in self.tasks
            if not task.is_due(finished_task_names) and not task in self.finished_tasks
        ]

        # start threads for all due tasks with run command and append to running_tasks
        for task in [
            task
            for task in self.tasks
            if task.is_due(finished_task_names)
            and task.data.get("run", None)
            and not task in self.finished_tasks
            and not task in self.running_tasks
        ]:
            logger.debug(f"Starting thread for {task.name}")
            task.thread = threading.Thread(
                target=task.data["run"], args=(self.SharedDict,)
            )
            task.thread.start()
            self.running_tasks.append(task)

    def task_names(self):
        return [task.name for task in self.tasks]

    def due_task_names(self):
        return [task.name for task in self.due_tasks]

    def due_task_descriptions(self):
        return [task.description for task in self.due_tasks]

    def due_task_titles(self):
        return [task.title for task in self.due_tasks]

    def waiting_task_descriptions(self):
        return [task.description for task in self.waiting_tasks]

    def waiting_task_titles(self):
        return [task.title for task in self.waiting_tasks]

    def running_task_titles(self):
        return [task.title for task in self.running_tasks]

    def finished_task_descriptions(self):
        return [task.description for task in self.finished_tasks]

    def finished_task_titles(self):
        return [task.title for task in self.finished_tasks]

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
