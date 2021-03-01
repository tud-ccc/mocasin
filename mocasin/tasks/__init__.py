# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


"""This subpackage manages the executable tasks that are available within
mocasin

To add a new task, add an entrypoint to the `entrypoints` module.
"""

import inspect
import logging
import sys
import textwrap
import typing
import os

from dataclasses import dataclass

from mocasin.tasks import entrypoints

log = logging.getLogger(__name__)


@dataclass
class Task:
    name: str = None
    function: typing.Callable = None
    docstring: str = None


def get_all_tasks():
    tasks = inspect.getmembers(entrypoints, predicate=inspect.isfunction)
    for name, func in tasks:
        yield Task(name=name, function=func, docstring=inspect.getdoc(func))


def print_help():
    print("mocasin is a framework for modeling dataflow applications and their")
    print("execution on MPSoC platforms.")
    print("")
    print("Usage: mocasin TASK [MOCASIN OPTIONS] [HYDRA OPTIONS]")
    print("")
    print("mocasin can perform one of several tasks. It expects the first ")
    print("argument to specify the task to be executed.")
    print("")
    print("Available mocasin tasks:")
    for task in get_all_tasks():
        desc = task.docstring
        desc_lines = textwrap.wrap(desc, width=41)
        task_name = f"  {task.name}: "
        print("%s%s" % ("{:<24}".format(task_name), desc_lines[0]))
        for line in desc_lines[1:]:
            print("%s%s" % ("{:<24}".format(""), line))
    print("")
    print("mocasin options:")
    print(" --no-fail-on-exception If this flag is set, mocasin does not exit")
    print("                        with an error code in case of an internal")
    print("                        exception. This is useful in combination")
    print("                        with hydra mutlirun if execution should")
    print("                        continue even when one job failed.")
    print(" --profile              If this flag is set, the specified task")
    print("                        is executed with a profiler (cProfile). The")
    print("                        profiling stats are dumped to file")
    print("                        mocasin_profile.")


def execute_task(task_name):
    """Execute a mocasin task.

    Args:
        task (str): name of the task to be executed
    """

    if task_name is None:
        log.error("ERROR: You need to specify a task!\n")
        print_help()
        sys.exit(-1)

    # collect all defined tasks
    tasks = {t.name: t.function for t in get_all_tasks()}

    if task_name not in tasks:
        log.error(
            f"ERROR: Tried to run a task unknown to mocasin ({task_name})\n"
        )
        print_help()
        sys.exit(-1)

    # execute the task
    tasks[task_name]()


def task_autocomplete():
    line = os.environ["COMP_LINE"]
    words = line.split(" ")
    if len(words) < 2:
        return [""]
    else:
        result = []
        start = words[-1]
        for task in _tasks:
            if task.startswith(start):
                result.append(task)
        return result
