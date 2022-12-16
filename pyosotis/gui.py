import logging
import tkinter as tk
from collections import namedtuple
from tkinter import Listbox, StringVar, ttk

from .runner import Runner

TaskBlock = namedtuple(
    "TaskBlock", ["labelframe", "button", "listbox", "listbox_choices"]
)

logger = logging.getLogger(__name__)

close_requested = False


def close_window():
    global close_requested
    close_requested = True


class PyosotisGui:
    def __init__(self, tk_root, runner: Runner):
        self.tk_root = tk_root
        tk_root.protocol("WM_DELETE_WINDOW", close_window)
        self.runner = runner
        runner.update_tasks()

        tk_root.title("Pyosotis")

        self.mainframe = ttk.Frame(tk_root, padding="3 3 12 12")

        self.place_gui_components(tk_root)
        self.update_gui()

    def place_gui_components(self, tk_root):
        def _place_task_block(label_text, button_text=None, button_command=None):
            """Create a consecutive block of a text label, a listbox and the listbox choices
            and return a TaskBlock with references to the new items."""
            lf = ttk.LabelFrame(tk_root, text=label_text)

            btn = None
            if button_text and button_command:
                btn = ttk.Button(
                    lf,
                    text=label_text,
                    command=button_command,
                )
                btn.pack(side="top", fill="both", expand=True)

            lb_choices = StringVar()
            lb = Listbox(lf, listvariable=lb_choices, selectmode="single")
            lb.pack(side="top", fill="both", expand=True)
            lf.pack(side="top", fill="both", expand=True)

            return TaskBlock(
                labelframe=lf, button=btn, listbox=lb, listbox_choices=lb_choices
            )

        self.tb_due = _place_task_block(
            "Currently due manual tasks",
            "Mark selected task as done",
            self.btn_due_done,
        )
        self.tb_running = _place_task_block("Currently running automatic tasks")
        self.tb_waiting = _place_task_block("Waiting tasks")
        self.tb_finished = _place_task_block("Finished tasks")

        tk.Label(text="Info").pack()

        self.tx_messages = tk.Text(tk_root)
        self.tx_messages.pack(side="top", fill="both", expand=True)

    def update_gui(self) -> None:
        global close_requested
        if close_requested:
            self.tk_root.destroy()
            exit
        self.runner.update_tasks()
        self.tb_due.listbox_choices.set(self.runner.due_task_titles())
        self.tb_running.listbox_choices.set(self.runner.running_task_titles())
        self.tb_waiting.listbox_choices.set(self.runner.waiting_task_titles())
        self.tb_finished.listbox_choices.set(self.runner.finished_task_titles())
        self.tk_root.after(1000, self.update_gui)

    def btn_due_done(self, *args):
        for i in self.tb_due.listbox.curselection():
            self.runner.finish_due_task(due_task_index=i)
            self.tx_messages.insert(tk.END, f"finished task {i}\n")
        self.update_gui()
