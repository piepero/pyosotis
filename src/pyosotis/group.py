"""Task Store."""
from collections.abc import Iterable
from types import ModuleType
from typing import Callable

from pydot import Dot, Edge

from .task import Task
from .task_tools import has_task_prefix, remove_task_prefix


class Group:
    tasks: list[Task]

    def __init__(self) -> None:
        self.tasks = list()

    def add_tasks_from_module(self, task_module: ModuleType) -> None:
        """Add tasks from a module."""

        # collect all procedure names starting with TASK_PROC_PREFIX
        task_proc_names = [
            item
            for item in dir(task_module)
            if has_task_prefix(item) and callable(getattr(task_module, item))
        ]

        proc_to_task_lookup: dict[Callable, Task] = dict()
        for proc_name in task_proc_names:
            # get the task generator procedure
            task_proc = getattr(task_module, proc_name)
            # call the procedure to get the returned Task object
            new_task = task_proc()
            # inject the shortened procedure name (w/o prefix) as task id
            new_task.id = remove_task_prefix(proc_name)

            proc_to_task_lookup[task_proc] = new_task

            self.add_task(new_task)

        # now that we know all task_procedures and tasks,
        # fill task.requires from task.requires_func
        for t in proc_to_task_lookup.values():
            t.requires = [proc_to_task_lookup[p] for p in t.requires_func]

    def __iter__(self):
        """Make Group iterable over self.tasks."""
        return iter(self.tasks)

    def add_task(self, task: Task) -> None:
        """Add a single Task object."""
        self.tasks.append(task)

    def add_tasks(self, tasks: Iterable[Task]) -> None:
        """Add multiple tasks."""
        self.tasks.extend(tasks)

    def remove_task(self, task: Task) -> None:
        """Remove the task from the group."""
        self.tasks.remove(task)

    def remove_tasks(self, tasks: Iterable[Task]) -> None:
        """Remove the task from the group."""
        self.tasks = [t for t in self.tasks if t not in tasks]

    def has_task(self, task_id: str) -> bool:
        """Test if the Group contains a task with the specified id."""
        return task_id in [x.id for x in self.tasks]

    @property
    def ids(self) -> list[str]:
        return [t.id for t in self.tasks]

    @property
    def titles(self) -> list[str]:
        return [t.title for t in self.tasks]

    @property
    def dot(self) -> Dot:
        """Generate a pydot Dot graph of the tasks and their dependencies."""

        dot = Dot()

        # first add all tasks as nodes
        for task in self.tasks:
            dot.add_node(task.pydot_node)

        # then add all dependencies as edges
        for task in self.tasks:
            if task.requires:
                for t in task.requires:
                    dot.add_edge(Edge(t.id, task.id))

        return dot
