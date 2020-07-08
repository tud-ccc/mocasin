#!/usr/bin/env python3

# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens, Christian Menard

import logging
import sys
import traceback

from pykpn.tasks import execute_task
log = logging.getLogger(__name__)


def main():
    """
    This script is the universal pykpn launcher, which replaces
    individual scripts for different tasks.

    The idea is for this script to manage different tasks that are
    available to do with the pykpn framework, using the different
    configuration capabilities allowed by the hydra framework.

    See :module:`pykpn.tasks` for a description of how new tasks can be added.
    """

    # We treat the first argument as the task to be executed
    # and remove it from argv. All other command line arguments are processed
    # later by hydra.

    task = None
    if len(sys.argv) > 1:
        task = sys.argv[1]
        del sys.argv[1]

    # Normally we want pykpn to fail and exit with an error code when an
    # exception occurs. However, in the case of hydra multirun, we usually want
    # to continue running other jobs even if a single one of them
    # fails. Therefore, calling exit() is prevented in the case of multirun
    fail_on_exception = True
    if ('-m' in sys.argv or '--multirun' in sys.argv):
        fail_on_exception = False

    try:
        execute_task(task)
    except Exception:
        log.error(traceback.format_exc())
        if fail_on_exception:
            sys.exit(1)


if __name__ == "__main__":
    main()
