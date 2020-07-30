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


@pytest.fixture(params=["hog-1.csv"])
def tetris_wwt15_opt_test(request):
    return request.param


@pytest.fixture(params=[
    "hog-1-1.csv",
    "hog-1-2.csv",
    "hog-1-3.csv",
    "hog-1-4.csv",
    "hog-1-5.csv",
    "hog-1.csv",
    "hog-big-1.csv",
    "hog-big-1-d.csv",
    "hog-2.csv",
    "hog-big-2.csv",
    "hog-big-2-d.csv",
    "hogA-2tasks-not_fisible.csv",
    "hog-big-3.csv",
    "hog-big-3-d.csv",
    "hog-mixed-3-d.csv",
    "hog-mixed-3-d-man.csv",
])
def tetris_bf_test(request):
    return request.param


@pytest.fixture(params=["wwt15_lr=['R','D','RDP']"])
def tetris_wwt15_option(request):
    return request.param


def run_tetris(datadir, expected_dir, scheduler, scenario, mode, options="",
               file_suffix=""):
    testname = os.path.splitext(scenario)[0]
    sched_l = scheduler.lower()
    input_scn = os.path.join(datadir, "tetris", "scenarios", "scheduler",
                             "{}.csv".format(testname))
    out_name = "{}_{}{}.out".format(sched_l, testname, file_suffix)
    out_path = os.path.join(datadir, out_name)
    tetris_base = os.path.join(datadir, "tetris")
    cmd = ("pykpn " + "tetris " + "tetris_base={} ".format(tetris_base) +
           "scenario={} ".format(input_scn) +
           "scheduler={} ".format(scheduler) + "mode={} ".format(mode) +
           "platform=exynos " + options + " " + "output={} ".format(out_path))
    subprocess.check_call(cmd.split(), cwd=datadir)

    assert filecmp.cmp(os.path.join(expected_dir, out_name), out_path,
                       shallow=False)


def test_tetris_dac(datadir, expected_dir, tetris_scheduler_test):
    run_tetris(datadir, expected_dir, "DAC", tetris_scheduler_test, 'single')


def test_tetris_dac_2(datadir, expected_dir, tetris_scheduler_test):
    run_tetris(datadir, expected_dir, "DAC-2", tetris_scheduler_test, 'single')


def test_tetris_fast(datadir, expected_dir, tetris_scheduler_test):
    run_tetris(datadir, expected_dir, "FAST", tetris_scheduler_test, 'single')


def test_tetris_wwt15(datadir, expected_dir, tetris_scheduler_test):
    run_tetris(datadir, expected_dir, "WWT15", tetris_scheduler_test, 'single')


def test_tetris_wwt15_rdp(datadir, expected_dir, tetris_wwt15_opt_test):
    run_tetris(datadir, expected_dir, "WWT15", tetris_wwt15_opt_test, 'single',
               options="wwt15_lr=['R','D','RDP']", file_suffix="_rdp")


def test_tetris_bf(datadir, expected_dir, tetris_bf_test):
    run_tetris(datadir, expected_dir, "BF", tetris_bf_test, 'single')


def test_tetris_bf_mem(datadir, expected_dir, tetris_bf_test):
    run_tetris(datadir, expected_dir, "BF-MEM", tetris_bf_test, 'single')
