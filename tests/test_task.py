from pyosotis import Task


def test_requires_ids() -> None:
    task_one = Task(title="Task One")
    task_two = Task(title="Task Two", requires=[task_one])
    task_three = Task(title="Task Three", requires=[task_one, task_two])

    assert not task_one.requires

    assert task_one in task_two.requires
    assert not task_two in task_two.requires
    assert not task_three in task_two.requires

    assert task_one in task_three.requires
    assert task_two in task_three.requires
    assert not task_three in task_three.requires
