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

    try:
        execute_task(task)
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(-1)


if __name__ == "__main__":
    main(sys.argv)
