import logging
import tkinter as tk

import sample_tasks
from pyosotis.gui import PyosotisGui
from pyosotis.runner import Runner

logging.basicConfig(filename=__name__ + ".log", level=logging.DEBUG)

if __name__ == "__main__":
    my_runner = Runner(sample_tasks)

    tk_root = tk.Tk()
    app = PyosotisGui(tk_root=tk_root, runner=my_runner)
    tk_root.mainloop()
