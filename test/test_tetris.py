# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

import subprocess
import filecmp
import os
import pytest

module_path = os.path.dirname(__file__)
tetris_scn_dir = os.path.join(module_path, "..", "examples", "tetris",
                              "scenarios")
all_scheduler_tests = [
    f for f in os.listdir(os.path.join(tetris_scn_dir, "scheduler"))
    if (os.path.splitext(f)[-1].lower() == ".csv")
]


@pytest.fixture(params=all_scheduler_tests)
def tetris_scheduler_test(request):
    return request.param


def test_tetris_dac(datadir, expected_dir, tetris_scheduler_test):
    testname = os.path.splitext(tetris_scheduler_test)[0]
    input_scn = os.path.join(datadir, "tetris", "scenarios", "scheduler",
                             "{}.csv".format(testname))
    out_name = "{}_{}.out".format("dac", testname)
    out_path = os.path.join(datadir, out_name)
    tetris_base = os.path.join(datadir, "tetris")
    subprocess.check_call([
        "pykpn", "tetris", "tetris_base={}".format(tetris_base),
        "scenario={}".format(input_scn), "scheduler=DAC", "mode=single",
        "platform=exynos", "output={}".format(out_path)
    ], cwd=datadir)

    assert filecmp.cmp(os.path.join(expected_dir, out_name), out_path,
                       shallow=False)
