from concurrent.futures import Future, ThreadPoolExecutor
from threading import Thread
from types import ModuleType
from typing import Optional

from loguru import logger

from .group import Group
from .task import Task


class Runner:
    waiting_tasks: Group
    due_tasks: Group
    running_tasks: Group
    finished_tasks: Group

    pool: ThreadPoolExecutor

    SharedDict: Optional[dict] = dict()

    task_futures: dict[Task, Future] = dict()

    def __init__(self, task_module: ModuleType, shared_dict: Optional[dict] = None):
        logger.debug("Runner(task_module.__name__):")
        self.task_module_name = task_module.__name__

        self.waiting_tasks = Group()
        self.due_tasks = Group()
        self.running_tasks = Group()
        self.finished_tasks = Group()

        self.pool = ThreadPoolExecutor(5)

        self.waiting_tasks.add_tasks_from_module(task_module)
        if shared_dict:
            self.SharedDict = shared_dict
            self.SharedDict["results"] = dict()  # a dict to collect results

    def update_tasks(self):
        """Update the status of all tasks."""

        # check the threads of running_tasks for completions
        remove_from_task_futures = list()
        for task in self.task_futures:
            if self.task_futures[task].done():
                logger.debug(f"Thread of task '{task.id}' has finished.")
                self.finished_tasks.add_task(task)
                self.running_tasks.remove_task(task)
                if self.SharedDict:
                    self.SharedDict["results"][task.id] = self.task_futures[
                        task
                    ].result()
                remove_from_task_futures.append(task)

        for task in remove_from_task_futures:
            self.task_futures.pop(task)

        # move tasks from waiting to due, if their requirements are met
        newly_due_tasks = [
            wt
            for wt in self.waiting_tasks
            if set(wt.requires).issubset(set(self.finished_tasks))
        ]
        self.waiting_tasks.remove_tasks(tasks=newly_due_tasks)
        self.due_tasks.add_tasks(newly_due_tasks)

        # start threads for all due_tasks with a run command
        # and move the tasks to running_tasks
        for task in [task for task in self.due_tasks if task.run]:
            logger.debug(f"Starting thread for task '{task.id}'.")
            assert task.run  # to satisfy the type checker for the next line
            self.task_futures[task] = self.pool.submit(task.run, task, self.SharedDict)
            self.running_tasks.add_task(task)
            self.due_tasks.remove_task(task)

    def finish_due_task(self, task_index: int) -> None:
        task = self.due_tasks.tasks[task_index]
        self.finished_tasks.add_task(task)
        self.due_tasks.remove_task(task)
