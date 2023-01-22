from pyosotis.task_tools import TASK_PROC_PREFIX, has_task_prefix, remove_task_prefix


def test_has_task_prefix() -> None:
    assert not has_task_prefix("")
    assert not has_task_prefix("some text")
    assert not has_task_prefix(f"_{TASK_PROC_PREFIX}")
    assert has_task_prefix(TASK_PROC_PREFIX)
    assert has_task_prefix(f"{TASK_PROC_PREFIX}do_something")


def test_remove_task_prefix() -> None:
    assert remove_task_prefix("") == ""
    assert remove_task_prefix("some text") == "some text"
    assert remove_task_prefix(f"_{TASK_PROC_PREFIX}") == f"_{TASK_PROC_PREFIX}"
    assert remove_task_prefix(TASK_PROC_PREFIX) == ""
    assert remove_task_prefix(f"{TASK_PROC_PREFIX}do_something") == "do_something"
