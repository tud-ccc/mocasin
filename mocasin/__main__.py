#!/usr/bin/env python3

# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andres Goens, Christian Menard

import argparse
import cProfile
import logging
import os
import shlex
import sys
import inspect
import traceback
import typing

from dataclasses import dataclass
from glob import glob

import mocasin.tasks

log = logging.getLogger(__name__)


@dataclass
class Task:
    name: str = None
    function: typing.Callable = None
    docstring: str = None


def get_all_tasks():
    """Find all tasks defined by mocasin

    This extracts all tasks defined in tasks/__init__.py

    Yields:
        Task: an object describing a task
    """
    tasks = inspect.getmembers(mocasin.tasks, predicate=inspect.isfunction)
    for name, func in tasks:
        yield Task(name=name, function=func, docstring=inspect.getdoc(func))


def main():
    """
    This script is the universal mocasin launcher, which replaces
    individual scripts for different tasks.

    The idea for this script is to manage the execution of tasks that are
    provided by the mocasin framework in combination with the configuration
    capabilities provided by the hydra framework.

    When running mocasin, it expects the task name to be the first command line
    argument and calls the appropriate task. Any further arguments are
    processed by hydra and then handed to the task.

    See :module:`mocasin.tasks` for a description of how new tasks can be added.
    """

    # create an epilog for our help message to list all avilable tasks
    epilog = "mocasin tasks:\n"
    for task in sorted(get_all_tasks(), key=lambda x: x.name):
        if len(task.name) < 22:
            epilog += "  {:<21} {}\n".format(
                task.name, task.docstring.replace("\n", "").replace("\r", "")
            )

    parser = argparse.ArgumentParser(
        description=(
            "mocasin is a framework for modeling dataflow applications and "
            "their execution on heterogeneous MPSoC platforms."
        ),
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="mocasin [mocasin option] TASK [hydra overrides]",
    )
    parser.add_argument(
        "task",
        metavar="TASK",
        help="The mocasin task to run. See below for a list of available tasks",
    )
    parser.add_argument(
        "--no-fail-on-exception",
        help=(
            "Prevent mocasin from exiting with an error code in case of an "
            "internal exception. This is useful in combination with hydra "
            "mutlirun if execution should continue even when one job failed."
        ),
        action="store_true",
    )
    parser.add_argument(
        "--profile",
        help=(
            "Execute the mocasin task while running a profiler (cProfile). The "
            "profiling stats are dumped to file mocasin_profile."
        ),
        action="store_true",
    )

    # parse all arguments directly known by mocasin. All unparsed arguments
    # will be passed to hydra
    args, unparsed = parser.parse_known_args()

    # we can pass arguments to hydra only via sys.argv, thus we manipulate it
    # here
    sys.argv = ["mocasin"] + unparsed

    # start the profiler if needed
    if args.profile:
        profiler = cProfile.Profile()
        profiler.enable()

    # we use a hidden "autocomplete" task for bash auto completion
    if args.task == "autocomplete":
        autocomplete()
        return

    # lookup the given task
    task = next((t for t in get_all_tasks() if t.name == args.task), None)

    if task is None:
        log.error(f"ERROR: The task '{args.task}' is not known to mocasin\n")
        parser.print_help()
        sys.exit(-1)

    # run the actual task
    exception = False
    try:
        task.function()
    except Exception:
        log.error(traceback.format_exc())
        exception = True

    # dump the profiler stats
    if args.profile:
        profiler.dump_stats("mocasin_profile")

    # Normally we want mocasin to fail and exit with an error code when an
    # exception occurs. However, in the case of hydra multirun, we might want
    # to continue running other jobs even if a single one of them
    # fails. Therefore, calling exit() is prevented if the
    # '--no-fail-on-exception' flag is given.
    if exception and not args.no_fail_on_exception:
        sys.exit(1)


def autocomplete():
    # the command we are completing
    cmd = shlex.split(os.environ["COMP_LINE"])
    # index of the word we are completing
    word_idx = int(os.environ["COMP_CWORD"])
    # the word we are completing
    try:
        word = cmd[word_idx]
    except IndexError:
        word = None

    # complete the command with the mocasin options
    args = ["-h", "--help", "--profile", "--no-fail-on-exception"]
    for arg in args:
        if word is None or arg.startswith(word):
            print(arg)

    # check if there is a task specified in cmd
    task = None
    for t in get_all_tasks():
        if t.name in cmd:
            task = t
            break

    if task is None:
        # if no tasks was found, we complete the task
        for t in get_all_tasks():
            if word is None or t.name.startswith(word):
                print(t.name)
    else:
        # if a task is given, we call hydra to do its completion
        # First remove the task from the command, because it confuses hydra
        cmd.remove(task.name)
        os.environ["COMP_LINE"] = " ".join(cmd)
        os.environ["COMP_POINT"] = str(
            int(os.environ["COMP_POINT"]) - len(task.name)
        )

        # we also need to manipulate sys.argv to trick hydra into completion
        # mode
        sys.argv = ["mocasin", "-sc", "query=bash"]

        # finally we manipulate stdout to intercept any completions hydra finds
        class Out(object):
            def write(self, s):
                self.s += s

            def flush(self):
                pass

            def __init__(self):
                self.s = ""

        hydra_out = Out()
        sys.stdout = hydra_out

        # call the task to get completion options
        task.function()

        # revert to default stdout
        sys.stdout = sys.__stdout__
        # and print all the completion options found by hydra
        for line in hydra_out.s.split("\n"):
            print(line)

        hydra_options = hydra_out.s.strip()

        # do we complete a word in style "lhs=rhs"?
        if word is not None and "=" in word:
            # did hydra not find any completion options?
            if hydra_options == "" or hydra_options==word:
                # if hydra did not find anything, we assume rhs is a file path
                # and attempt to complete it
                lhs, rhs = word.split("=")
                for f in glob("*") + glob(f"{rhs}*") + glob(f"{rhs}/*"):
                    if os.path.isdir(f):
                        print(f"{lhs}={f}/")
                    else:
                        print(f"{lhs}={f}")


if __name__ == "__main__":
    main()
