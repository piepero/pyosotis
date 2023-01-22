import tasks_for_testing

from pyosotis import Group, Task


def test_has_task():
    my_group = Group()

    assert not my_group.has_task("say_hello")
    assert not my_group.has_task("do_something")

    my_group.add_task(Task(id="delete_everything", title="Delete Everything"))

    assert not my_group.has_task("say_hello")
    assert not my_group.has_task("do_something")

    my_group.add_task(Task(id="do_something", title="Do something"))

    assert not my_group.has_task("say_hello")
    assert my_group.has_task("do_something")

    my_group.add_task(Task(id="say_hello", title="Hello World!"))

    assert my_group.has_task("say_hello")
    assert my_group.has_task("do_something")
