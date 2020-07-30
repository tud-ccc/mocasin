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


def run_tetris(datadir, expected_dir, scheduler, scenario, mode):
    testname = os.path.splitext(scenario)[0]
    sched_l = scheduler.lower()
    input_scn = os.path.join(datadir, "tetris", "scenarios", "scheduler",
                             "{}.csv".format(testname))
    out_name = "{}_{}.out".format(sched_l, testname)
    out_path = os.path.join(datadir, out_name)
    tetris_base = os.path.join(datadir, "tetris")
    subprocess.check_call([
        "pykpn", "tetris", "tetris_base={}".format(tetris_base),
        "scenario={}".format(input_scn), "scheduler={}".format(scheduler),
        "mode={}".format(mode), "platform=exynos", "output={}".format(out_path)
    ], cwd=datadir)

    assert filecmp.cmp(os.path.join(expected_dir, out_name), out_path,
                       shallow=False)


def test_tetris_dac(datadir, expected_dir, tetris_scheduler_test):
    run_tetris(datadir, expected_dir, "DAC", tetris_scheduler_test, 'single')

def test_tetris_dac_2(datadir, expected_dir, tetris_scheduler_test):
    run_tetris(datadir, expected_dir, "DAC-2", tetris_scheduler_test, 'single')
