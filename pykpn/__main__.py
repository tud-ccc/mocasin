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

    # If there is an positional argument that is not an assignment, we treat it
    # as a task.
    for i in range(1, len(sys.argv)):
        if '=' not in sys.argv[i] and sys.argv[i][0] != '-':
            sys.argv[i] = "task=%s" % sys.argv[i]
            break

    # execute the task
    try:
        execute_task()
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(-1)


if __name__ == "__main__":
    main()

