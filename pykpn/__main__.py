#!/usr/bin/env python3

# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens, Christian Menard

import logging
import sys
import traceback

from pykpn.tasks import execute_task
from pykpn.tgff.tgffSimulation import TgffReferenceError

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
    # if the first argument is not an assignment, we treat it as a task
    if len(sys.argv) > 1 and '=' not in sys.argv[1]:
        sys.argv[1] = "task=%s" % sys.argv[1]

    # execute the task
    try:
        execute_task()
    except TgffReferenceError:
        log.warning("Referenced non existing tgff component!")
        sys.exit(0)
    except Exception:
        log.error(traceback.format_exc())
        sys.exit(-1)


if __name__ == "__main__":
    main()
