# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

import subprocess
import filecmp
import os

def test_tetris():
    """Run the command.

    Run ``make test`` in ``test/tetris`` directory for testing.
    """
    subprocess.check_call(["make", "test"],
                          cwd="test/tetris")


