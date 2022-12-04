[![PYOSOTIS](./assets/pyosotis_banner.png)](https://github.com/piepero/pyosotis)
# PYOSOTIS

## About the project

_⚠ This is a (working) prototype and work in progress._  
_⚠ current status: usable for manual to do lists and automatic processes that need no arguments to run_

Pyosotis is (intended to be) a framework for building "interactive asynchronous to do lists" (or checklists) which can lead the user through complex processes requiring multiple sequential or parallel steps.
Those steps can be either performed automatically or by the user.

Parallel display and execution of due tasks will minimize the required time to finish all tasks, while the interactive GUI will ensure that no manual steps are forgotten or executed prematurely.

An example: A (simplified) manual software release process might contain the following tasks:
- T1: clone main project
- T2: clone helper projects
- T3: update readme in main project
- T4: build binaries
- T5: package and upload binaries
- T6: send notification e-mail

With the following dependencies:
- T3 can only be started after T1 is finished
- T4 requires T1 and T2 to be completed
- T5 requires the completion of T3 and T4
- T6 will be performed after T5 is done

Some tasks could be automated (T1, T2, T4, T5), while others may need to be performed manually (T3, T6).

Starting the pyosotis task runner should:
- start T1 and T2 automatically, and in parallel
- as soon as T1 is completed: prompt the user to update the readme (T3)
- as soon as both T1 and T2 are completed: start T4
- run T5 as soon as T3 and T4 are finished
- and finally prompt the user to perform T6 once T5 is done

## Example

```shell
> py ./sample_runner.py
```
## Example files

_```sample_runner.py```_ creates a task runner based on _```sample_tasks.py```_ and starts a simple _tkinter_ GUI leading the user through all the manual items on the task list.

_```sample_tasks.py```_ contains a bunch of (purely manual) sample tasks with various dependencies. Used by _```sample_runner.py```_.

_```sample_dummies.py```_ defines dummy procedures, emulating simple automatic tasks for use in _```sample_tasks.py```_.
