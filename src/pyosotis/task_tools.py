# all task data generating procedures share a common prefix
TASK_PROC_PREFIX = "task_"


def has_task_prefix(proc_name: str) -> bool:
    return proc_name.startswith(TASK_PROC_PREFIX)


def remove_task_prefix(proc_name: str) -> str:
    return proc_name.removeprefix(TASK_PROC_PREFIX)
