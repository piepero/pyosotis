import logging
import tkinter as tk
from tkinter import Listbox, StringVar, ttk

from .runner import Runner

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

        ttk.Button(
            tk_root, text="Mark selected task as done", command=self.btn_due_done
        ).pack()

        ttk.Label(tk_root, text="Currently due tasks").pack(
            side="top", fill="both", expand=True
        )

        self.lb_due_choices = StringVar(value=runner.due_task_messages())
        self.lb_due = Listbox(
            tk_root, listvariable=self.lb_due_choices, selectmode="multiple"
        )
        self.lb_due.pack(side="top", fill="both", expand=True)

        tk.Label(text="Waiting tasks").pack(side="top", fill="both", expand=True)

        self.lb_waiting_choices = StringVar(value=runner.waiting_task_messages())
        self.lb_waiting = Listbox(
            tk_root,
            listvariable=self.lb_waiting_choices,
            state=tk.DISABLED,
            takefocus=False,
        )
        self.lb_waiting.pack(side="top", fill="both", expand=True)

        tk.Label(text="Finished tasks").pack(side="top", fill="both", expand=True)

        self.lb_finished_choices = StringVar(value=runner.finished_task_messages())
        self.lb_finished = Listbox(
            tk_root,
            listvariable=self.lb_finished_choices,
            state=tk.DISABLED,
            takefocus=False,
        )
        self.lb_finished.pack(side="top", fill="both", expand=True)

        tk.Label(text="Info").pack()

        self.tx_messages = tk.Text(tk_root)
        self.tx_messages.pack(side="top", fill="both", expand=True)
        self.update_gui()

    def update_gui(self) -> None:
        global close_requested
        if close_requested:
            self.tk_root.destroy()
            exit
        self.runner.update_tasks()
        self.lb_due_choices.set(self.runner.due_task_messages())
        self.lb_waiting_choices.set(self.runner.waiting_task_messages())
        self.lb_finished_choices.set(self.runner.finished_task_messages())
        self.tk_root.after(1000, self.update_gui)

    def btn_due_done(self, *args):
        for i in self.lb_due.curselection():
            self.runner.finish_due_task(due_task_index=i)
            self.tx_messages.insert(tk.END, f"finished task {i}\n")
        self.update_gui()
