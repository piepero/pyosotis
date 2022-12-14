import logging

logger = logging.getLogger(__name__)


class Task:
    def __init__(self, task_name, task_proc):
        self.name = task_name
        self.proc = task_proc
        self.data = task_proc()
        logger.debug(f"Task({task_name}) created.")

    def __str__(self):
        return f"Task name: {self.name}"

    def is_due(self, finished_task_names):
        if not "requires" in self.data:
            return True
        for req in self.data["requires"]:
            if not req.__name__ in finished_task_names:
                return False
        return True

    @property
    def title(self):
        return self.data["title"]

    @property
    def description(self):
        return self.data["description"]
