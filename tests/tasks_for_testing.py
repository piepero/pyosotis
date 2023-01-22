from pyosotis import Task


def task_eins():
    return Task(
        title="Title: eins",
        description="Description: eins",
    )


def task_zwei():
    return Task(
        title="Title: zwei",
        description="Description: zwei",
        run=lambda x: 42,
        requires_func=[task_eins],
    )
