# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Robert Khasanov

import subprocess
import filecmp
import os
import pytest


def test_tetris_mapping(datadir, expected_dir):
    testname = "3337-mix-3-running-deadline_4.csv"
    input_scn = os.path.join(datadir, "tetris", "job_table",
                             "{}".format(testname))
    out_name = "3337_dac_mapping.out"
    out_path = os.path.join(datadir, out_name)
    tetris_base = os.path.join(datadir, "tetris", "apps")
    cmd = ("pykpn " + "tetris_scheduler " +
           "tetris_apps_dir={} ".format(tetris_base) +
           "job_table={} ".format(input_scn) +
           "resource_manager=dac platform=exynos " +
           "output_schedule={} ".format(out_path))
    subprocess.check_call(cmd.split(), cwd=datadir)

    assert filecmp.cmp(os.path.join(expected_dir, out_name), out_path,
                       shallow=False)


_EPS = 0.001
_FOUND_SCHEDULING_STR = "Found schedule: "
_SCHEDULE_TIME = "Schedule time: "
_ENERGY_CONSUMPTION = "Energy consumption: "


def run_tetris_scheduler(datadir, scheduler, test_schedule_tuple, options="",
                         check_result=True):
    scenario = test_schedule_tuple[0]
    testname = os.path.splitext(scenario)[0]
    input_scn = os.path.join(datadir, "tetris", "job_table",
                             "{}.csv".format(testname))
    out_name = "{}_{}.out".format(scheduler, testname)
    out_path = os.path.join(datadir, out_name)
    tetris_base = os.path.join(datadir, "tetris", "apps")
    cmd = ("pykpn " + "tetris_scheduler " +
           "tetris_apps_dir={} ".format(tetris_base) +
           "job_table={} ".format(input_scn) +
           "resource_manager={} ".format(scheduler) + "platform=exynos " +
           options + " " + "output_schedule={} ".format(out_path))

    print(cmd)
    res = subprocess.run(cmd.split(), cwd=datadir, check=True,
                         stdout=subprocess.PIPE)

    if check_result:
        stdout = res.stdout.decode()
        for line in stdout.split('\n'):
            if line.startswith(_FOUND_SCHEDULING_STR):
                found_scheduling = line[len(_FOUND_SCHEDULING_STR):]
                expected_found = test_schedule_tuple[1]
                assert found_scheduling == str(expected_found)
            if line.startswith(_SCHEDULE_TIME):
                schedule_time = float(line[len(_SCHEDULE_TIME):-1])
                assert abs(schedule_time - test_schedule_tuple[2]) < _EPS
            if line.startswith(_ENERGY_CONSUMPTION):
                energy = float(line[len(_ENERGY_CONSUMPTION):-1])
                assert abs(energy - test_schedule_tuple[3]) < _EPS


@pytest.fixture(params=[
    ("hog-1.csv", True, 12.663, 11.866),
    ("hog-1-2.csv", True, 12.353, 14.254),
    ("hog-big-5-d.csv", True, 84.931, 358.91),
    ("hog-big-8-d.csv", True, 125.766, 601.98),
    ("1041-sr_B-1-new-deadline_7.csv", True, 24.379, 31.006),
    ("1053-af_B-1-new-deadline_7.csv", True, 27.913, 125.33),
    ("2177-mix-2-new-deadline_2.csv", True, 41.922, 42.123),
    ("3319-af_B-3-running-deadline_4.csv", True, 78.598, 173.14),
    ("3337-mix-3-running-deadline_4.csv", True, 13.941, 41.408),
    ("3509-mix-3-running-deadline_5.csv", False, None, None),
    ("3569-mix-3-running-deadline_7.csv", False, None, None),
    ("4405-hog_B-4-new-deadline_6.csv", False, None, None),
])
def dac_expected_schedule(request):
    return request.param


def test_tetris_dac(datadir, dac_expected_schedule):
    run_tetris_scheduler(datadir, "dac", dac_expected_schedule)


@pytest.fixture(params=[
    ("hog-1.csv", True, 12.663, 11.866),
    ("hog-big-8-d.csv", True, 125.766, 601.98),
    ("3337-mix-3-running-deadline_4.csv", True, 11.041, 46.493),
    ("4405-hog_B-4-new-deadline_6.csv", False, None, None),
])
def dac2_expected_schedule(request):
    return request.param


def test_tetris_dac2(datadir, dac2_expected_schedule):
    run_tetris_scheduler(datadir, "dac-2", dac2_expected_schedule)


@pytest.fixture(params=[
    ("hog-1.csv", True, 12.663, 11.866),
    ("hog-1-2.csv", True, 12.353, 14.254),
    ("hog-big-5-d.csv", False, None, None),
    ("1041-sr_B-1-new-deadline_7.csv", True, 24.379, 31.006),
    ("2177-mix-2-new-deadline_2.csv", True, 41.922, 42.123),
    ("3319-af_B-3-running-deadline_4.csv", True, 62.667, 158.81),
    ("3337-mix-3-running-deadline_4.csv", True, 11.015, 43.016),
    ("4405-hog_B-4-new-deadline_6.csv", False, None, None),
])
def fast_expected_schedule(request):
    return request.param


def test_tetris_fast(datadir, fast_expected_schedule):
    run_tetris_scheduler(datadir, "fast", fast_expected_schedule)


@pytest.fixture(params=[
    ("hog-1-2.csv", True, 12.353, 14.254),
    ("hog-big-5-d.csv", True, 79.872, 366.01),
    ("hog-big-8-d.csv", True, 114.298, 626.05),
    ("2177-mix-2-new-deadline_2.csv", True, 41.922, 42.123),
    ("3319-af_B-3-running-deadline_4.csv", True, 67.103, 147.96),
    ("3337-mix-3-running-deadline_4.csv", True, 12.131, 40.719),
    ("3509-mix-3-running-deadline_5.csv", True, 37.127, 105.08),
    ("4405-hog_B-4-new-deadline_6.csv", False, None, None),
])
def wwt15_expected_schedule(request):
    return request.param


def test_tetris_wwt15(datadir, wwt15_expected_schedule):
    run_tetris_scheduler(datadir, "wwt15", wwt15_expected_schedule)


@pytest.fixture(params=[
    ("hog-1-2.csv", ),
    ("2177-mix-2-new-deadline_2.csv", ),
])
def wwt15_rdp_expected_schedule(request):
    return request.param


def test_tetris_wwt15_rdp(datadir, wwt15_rdp_expected_schedule):
    run_tetris_scheduler(datadir, "wwt15", wwt15_rdp_expected_schedule,
                         options="resource_manager.wwt15_lr=['R','D','RDP']",
                         check_result=False)


@pytest.fixture(params=[
    ("hog-1.csv", True, 12.663, 11.866),
    ("hog-1-2.csv", True, 12.353, 14.254),
    ("1041-sr_B-1-new-deadline_7.csv", True, 24.379, 31.006),
    ("1053-af_B-1-new-deadline_7.csv", True, 27.913, 125.33),
    ("2177-mix-2-new-deadline_2.csv", True, 41.922, 42.123),
    #     ("3337-mix-3-running-deadline_4.csv", True, 15.144, 32.513), # FIXME: This test is too long, need to find a substitution
    ("3569-mix-3-running-deadline_7.csv", False, None, None),
])
def bf_expected_schedule(request):
    return request.param

def test_tetris_bf(datadir, bf_expected_schedule):
    run_tetris_scheduler(datadir, "bf", bf_expected_schedule)


def test_tetris_bf_mem(datadir, bf_expected_schedule):
    run_tetris_scheduler(datadir, "bf-mem", bf_expected_schedule)


@pytest.fixture(params=[
    "hog-big-8-d-online.csv",
])
def tetris_manager_test(request):
    return request.param


def test_tetris_manager(datadir, expected_dir, tetris_manager_test):
    testname = os.path.splitext(tetris_manager_test)[0]
    input_scn = os.path.join(datadir, "tetris", "request_trace",
                             "{}.csv".format(testname))
    out_name = "{}_{}.out".format("manager", testname)
    out_path = os.path.join(datadir, out_name)
    tetris_base = os.path.join(datadir, "tetris", "apps")
    cmd = ("pykpn " + "tetris_manager " +
           "tetris_apps_dir={} ".format(tetris_base) +
           "input_jobs={} ".format(input_scn) +
           "resource_manager={} ".format("dac") + "platform=exynos " +
           "log_level=INFO " + "output_trace={} ".format(out_path))
    subprocess.check_call(cmd.split(), cwd=datadir)

    # TODO: Add output
