#!/usr/bin/env python3

# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andres Goens, Christian Menard

import argparse
import logging
import sys
import traceback
import cProfile

from mocasin.tasks import execute_task, get_all_tasks

log = logging.getLogger(__name__)


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

    epilog = "mocasin tasks:\n"
    for task in get_all_tasks():
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
    )
    parser.add_argument(
        "task",
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

    # run the actual task
    exception = False
    try:
        execute_task(args.task)
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


if __name__ == "__main__":
    main()
