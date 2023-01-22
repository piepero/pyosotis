[![PYOSOTIS](./assets/pyosotis_banner.png)](https://github.com/piepero/pyosotis)
# PYOSOTIS

## About the project

_⚠ This project is work in progress. Expect changes to names, keys and functionality._  
_⚠ Current status: fully usable, though somewhat lacking in features._

Pyosotis is a framework for building "interactive asynchronous to do lists" (or checklists) which guide the user through complex processes requiring multiple sequential or parallel steps.
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

_```sample_tasks.py```_ contains a bunch of sample tasks with various dependencies. Used by _```sample_runner.py```_.

_```sample_dummies.py```_ defines dummy procedures, emulating simple automatic tasks for use in _```sample_tasks.py```_.


## Documentation (quite rudimentary)

### Creating tasks

For working examples, see _```sample_tasks.py```_.

A fully featured task could look something like this:
```python
def task_do_something():
    return Task(
        title="This is the title of the task",
        description="This is a longer description of the task.\nIt can contain mutltiple lines.",
        requires_func=[task_one, task_two],
        run=some_python_function,
    }
```

Tasks are defined as functions.  
The function name doubles as unique task ID. If other tasks refer to the task (for example by referencing it in ```"requires_func"```), they have to use the full function name __task_do_something__.

The function returns a Task item.

```"title"``` is the only required argument. This is the titel by which the task is represented in the GUI. The title should describe in one line what the task does.

```"description"``` is optional. Use this argument to store a longer description of the task. For manual tasks, the description could provide info on the necessary steps to complete the task. The description can contain line breaks.

```"requires_func"``` is optional. This is the most important parameter for Pyosotis' functionality. If a task has a list of other required tasks, it will only become due, when all tasks in "requires_func" have been previously completed. In this example, __task_do_something__ will not be considered _due_, unless __task_one__ and __task_two__ have been completed.

```"run"``` is optional, as well. It marks an automatic task. The value of run has to be a callable function. For details, see "using functions" below. The pyosotis task runner will automatically start this function in a thread. See "Using functions" below for more details.

### Using functions

For working examples, see _```sample_dummies.py```_.

```python
def create_file_in_workdir(SharedDict: dict):
    """Creates a tempory file in the workdir."""
    workdir = SharedDict['workdir']

    temp_path = os.path.join(workdir, 'my_file.txt')
    with open(temp_path, 'w') as fout:
        fout.write('This is a file in workdir.')
    
    SharedDict['my_filename'] = temp_path
```

The functions called by the task's "run" parameter are simple Python functions with a single parameter, which is a dictionary passed to each function by the task runner.

The functions use this dictionary to access and also to return data. Since the task functions run in threads, race conditions and similar inconveniences may occur! However, this is not expected to be much of a problem in practice, since Pyosotis is mainly intended for fairly linear processes in which later tasks mostly only read data provided by earlier tasks and add their own keys to the dictionary.
## Future enhancements
### Planned enhancements

- [ ] show a message when all tasks are complete
- [ ] GUI: render task desription as markdown (see [[markdown]](https://pypi.org/project/Markdown/)[[css]](https://markdowncss.github.io/))
- [ ] Use a nice tkinter theme [[Reddit]](https://www.reddit.com/r/Python/comments/lps11c/how_to_make_tkinter_look_modern_how_to_use_themes/)

### Considered enhancements

Ideas for optional improvements.

- [ ] automatically store return value of automated tasks in a defined location and make it accessible by other tasks. See [stackoverflow](https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread) for inspiration.
- [ ] change value of "run" to be a list/tuple/set of multiple functions instead of just one.
- [ ] allow tasks to pass arguments to the function (or functions) called in "run".
- [ ] provide a locking mechanism for SharedDict. Currently, only atomic operations are thread safe. Possibly the ThreadSafeDict from [this stackoverflow thread](https://stackoverflow.com/questions/1312331/using-a-global-dictionary-with-threads-in-python).
- [ ] visualize the task structure