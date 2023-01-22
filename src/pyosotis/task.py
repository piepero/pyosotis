from dataclasses import dataclass, field
from typing import Callable, Optional

import pydot
from loguru import logger

from .task_tools import remove_task_prefix


@dataclass
class Task:
    title: str
    description: str = ""
    run: Optional[Callable] = None
    requires: list["Task"] = field(default_factory=list)
    requires_func: list[Callable] = field(default_factory=list)
    id: str = "will be automatically set"

    def __hash__(self):
        return hash(self.id)

    @property
    def pydot_node(self) -> pydot.Node:
        kw_args = {"name": self.id, "title": self.title, "shape": "box"}
        if self.run:
            kw_args["shape"] = "parallelogram"
        return pydot.Node(**kw_args)
