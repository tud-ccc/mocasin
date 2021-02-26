#!/usr/bin/env python3

# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andres Goens, Christian Menard

import logging
import sys
import traceback
import cProfile

from mocasin.tasks import execute_task, task_autocomplete

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

    # We treat the first argument as the task to be executed
    # and remove it from argv. All other command line arguments are processed
    # later by hydra.

    task = None
    if len(sys.argv) > 1:
        task = sys.argv[1]
        del sys.argv[1]

    # This code is for bash/zsh autocompletion for the available mocasin tasks
    # and there is no reason this would otherwise be called.
    if task == "-sc" and len(sys.argv) == 2 and sys.argv[1] == "query=bash":
        print(" ".join(task_autocomplete()))
        return

    # Normally we want mocasin to fail and exit with an error code when an
    # exception occurs. However, in the case of hydra multirun, we might want
    # to continue running other jobs even if a single one of them
    # fails. Therefore, calling exit() is prevented if the
    # '--no-fail-on-exception' flag is given.
    fail_on_exception = True
    if "--no-fail-on-exception" in sys.argv:
        sys.argv.remove("--no-fail-on-exception")
        fail_on_exception = False

    profiler = None
    if "--profile" in sys.argv:
        sys.argv.remove("--profile")
        profiler = cProfile.Profile()
        profiler.enable()

    exception = False
    try:
        execute_task(task)
    except Exception:
        log.error(traceback.format_exc())
        exception = True

    if profiler is not None:
        profiler.dump_stats("mocasin_profile")
    if exception and fail_on_exception:
        sys.exit(1)


def profile():
    """
    This script is a wrapper around the mocasin launcher, which replaces
    starts a profiling run.
    """
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.dump_stats("profile_dump")
    profiler.print_stats()


if __name__ == "__main__":
    main()
