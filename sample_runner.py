import tkinter as tk

from loguru import logger

import sample_tasks
from pyosotis.gui import PyosotisGui
from pyosotis.runner import Runner

logger.add(".sample_runner.log")

if __name__ == "__main__":
    # provide custom shared dictionary that is passed on to the automatic functions
    MySharedDict = {"username": "Ada Lovelace"}

    # create the task runner object
    my_runner = Runner(task_module=sample_tasks, shared_dict=MySharedDict)

    tk_root = tk.Tk()
    app = PyosotisGui(tk_root=tk_root, runner=my_runner)
    tk_root.mainloop()

    logger.info(MySharedDict)
