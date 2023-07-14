import queue
import tkinter as tk
from collections import namedtuple
from logging import Handler
from queue import Queue
from tkinter import Listbox, StringVar, ttk
from tkinter.scrolledtext import ScrolledText

from loguru import logger

from .runner import Runner

TaskBlock = namedtuple(
    "TaskBlock", ["labelframe", "button", "listbox", "listbox_choices"]
)

close_requested = False


def close_window():
    global close_requested
    close_requested = True


class QueueHandler(Handler):
    def __init__(self, queue):
        Handler.__init__(self)
        self.queue = queue

    def emit(self, record):
        self.queue.put(record)


class PyosotisGui:
    def __init__(self, tk_root, runner: Runner):
        self.tk_root = tk_root
        tk_root.protocol("WM_DELETE_WINDOW", close_window)
        self.runner = runner
        runner.update_tasks()

        tk_root.title("Pyosotis")

        self.mainframe = ttk.Frame(tk_root, padding="3 3 12 12")
        self.mainframe.grid(row=0, column=0, sticky="nsew")

        tk_root.rowconfigure(0, weight=1)
        tk_root.columnconfigure(0, weight=1)

        self.place_gui_components(self.mainframe)

        self.log_queue: Queue = Queue()
        self.log_queue_handler = QueueHandler(self.log_queue)
        logger.add(self.log_queue_handler)

        self.update_gui()

    def place_gui_components(self, tk_root):
        def _place_task_block(label_text, button_text=None, button_command=None):
            """Create a consecutive block of a text label, a listbox and the listbox
            choices and return a TaskBlock with references to the new items."""
            lf = ttk.LabelFrame(tk_root, text=label_text)

            btn = None
            if button_text and button_command:
                btn = ttk.Button(
                    lf,
                    text=button_text,
                    command=button_command,
                )
                btn.pack(side="top", fill="both", expand=True)

            lb_choices = StringVar()
            lb = Listbox(lf, listvariable=lb_choices, selectmode="single")
            lb.pack(side="top", fill="both", expand=True)

            return TaskBlock(
                labelframe=lf, button=btn, listbox=lb, listbox_choices=lb_choices
            )

        self.tb_due = _place_task_block(
            "Currently due manual tasks",
            "Mark selected task as done",
            self.btn_due_done,
        )

        self.tb_due.listbox.bind("<<ListboxSelect>>", self.due_task_selected)
        self.tb_running = _place_task_block("Currently running automatic tasks")
        self.tb_waiting = _place_task_block("Waiting tasks")
        self.tb_finished = _place_task_block("Finished tasks")

        self.tb_due.labelframe.grid(row=0, column=0, stick="nsew")
        self.tb_running.labelframe.grid(row=0, column=1, stick="nsew")
        self.tb_waiting.labelframe.grid(row=1, column=0, stick="nsew")
        self.tb_finished.labelframe.grid(row=1, column=1, stick="nsew")

        lf = ttk.LabelFrame(tk_root, text="Task Description")
        self.tx_description = ScrolledText(lf, wrap=tk.WORD)
        self.tx_description.pack(side="top", fill="both")
        lf.grid(row=2, column=0, columnspan=2, stick="nsew")

        lf = ttk.LabelFrame(tk_root, text="Log")
        self.tx_messages = ScrolledText(lf, wrap=tk.NONE)
        self.tx_messages.pack(side="top", fill="both")
        lf.grid(row=3, column=0, columnspan=2, stick="nsew")

        self.tx_messages.tag_config("INFO", foreground="black")
        self.tx_messages.tag_config("DEBUG", foreground="gray")
        self.tx_messages.tag_config("WARNING", foreground="orange")
        self.tx_messages.tag_config("ERROR", foreground="red")
        self.tx_messages.tag_config("CRITICAL", foreground="red", underline=True)

        (cols, rows) = tk_root.grid_size()
        for r in range(rows):
            tk_root.rowconfigure(r, weight=1)
        for c in range(cols):
            tk_root.columnconfigure(c, weight=1)

    def update_gui(self) -> None:
        """Update the GUI."""

        # if requested by the global flag, close the program
        global close_requested
        if close_requested:
            self.tk_root.destroy()
            return

        # show log messages from queue
        while True:
            try:
                rec = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.tx_messages.insert(
                    tk.END, self.log_queue_handler.format(rec) + "\n", rec.levelname
                )
                self.tx_messages.yview(tk.END)

        # update the status of all tasks
        self.runner.update_tasks()

        # write the task titles to the appropriate listboxes
        self.tb_due.listbox_choices.set(self.runner.due_tasks.titles)
        self.tb_running.listbox_choices.set(self.runner.running_tasks.titles)
        self.tb_waiting.listbox_choices.set(self.runner.waiting_tasks.titles)
        self.tb_finished.listbox_choices.set(self.runner.finished_tasks.titles)

        # schedule next GUI update
        self.tk_root.after(500, self.update_gui)

    def btn_due_done(self, *args):
        for i in self.tb_due.listbox.curselection():
            task_id = self.runner.due_tasks.tasks[i].id
            self.runner.finish_due_task(i)
            logger.info(f"task '{task_id}' manually marked as done")
        self.tx_description.delete("1.0", tk.END)
        self.update_gui()

    def due_task_selected(self, event):
        selection = event.widget.curselection()
        if not selection:
            return
        task = self.runner.due_tasks.tasks[selection[0]]
        self.tx_description.delete("1.0", tk.END)
        self.tx_description.insert(tk.END, task.description)
