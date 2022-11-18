import logging

import sample_tasks
from pyosotis.runner import Runner

logging.basicConfig(filename=__name__ + ".log", level=logging.DEBUG)

my_runner = Runner(sample_tasks)
my_runner.update_tasks()
print(my_runner)
