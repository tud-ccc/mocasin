# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov

import subprocess
import filecmp
import os
import pytest


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_tetris_schedule(datadir, expected_dir):
    testname = "3337-mix-3-running-deadline_4.csv"
    input_scn = os.path.join(
        datadir, "tetris", "job_table", "{}".format(testname)
    )
    out_name = "3337_medf_mapping.out"
    out_path = os.path.join(datadir, out_name)
    tetris_base = os.path.join(datadir, "tetris", "apps")
    cmd = (
        "mocasin "
        + "tetris_scheduler "
        + "tetris_apps_dir={} ".format(tetris_base)
        + "job_table={} ".format(input_scn)
        + "resource_manager=medf platform=exynos "
        + "output_schedule={} ".format(out_path)
    )
    subprocess.check_call(cmd.split(), cwd=datadir)

    assert filecmp.cmp(
        os.path.join(expected_dir, out_name), out_path, shallow=False
    )


_EPS = 0.001
_FOUND_SCHEDULING_STR = "Found schedule: "
_SCHEDULE_TIME = "Schedule time: "
_ENERGY_CONSUMPTION = "Energy consumption: "


def run_tetris_scheduler(
    datadir, scheduler, test_schedule_tuple, options="", check_result=True
):
    scenario = test_schedule_tuple[0]
    testname = os.path.splitext(scenario)[0]
    input_scn = os.path.join(
        datadir, "tetris", "job_table", "{}.csv".format(testname)
    )
    out_name = "{}_{}.out".format(scheduler, testname)
    out_path = os.path.join(datadir, out_name)
    tetris_base = os.path.join(datadir, "tetris", "apps")
    cmd = (
        "mocasin "
        + "tetris_scheduler "
        + "tetris_apps_dir={} ".format(tetris_base)
        + "job_table={} ".format(input_scn)
        + "resource_manager={} ".format(scheduler)
        + "platform=exynos "
        + options
        + " "
        + "output_schedule={} ".format(out_path)
    )

    print(cmd)
    res = subprocess.run(
        cmd.split(), cwd=datadir, check=True, stdout=subprocess.PIPE
    )

    if check_result:
        stdout = res.stdout.decode()
        for line in stdout.split("\n"):
            if line.startswith(_FOUND_SCHEDULING_STR):
                found_scheduling = line[len(_FOUND_SCHEDULING_STR) :]
                expected_found = test_schedule_tuple[1]
                assert found_scheduling == str(expected_found)
            if line.startswith(_SCHEDULE_TIME):
                schedule_time = float(line[len(_SCHEDULE_TIME) : -1])
                assert abs(schedule_time - test_schedule_tuple[2]) < _EPS
            if line.startswith(_ENERGY_CONSUMPTION):
                energy = float(line[len(_ENERGY_CONSUMPTION) : -1])
                assert abs(energy - test_schedule_tuple[3]) < _EPS


@pytest.fixture(
    params=[
        ("hog-1.csv", True, 12.663, 11.866),
        ("hog-1-2.csv", True, 12.353, 14.254),
        ("hog-big-5-d.csv", True, 84.931, 358.910),
        ("hog-big-8-d.csv", True, 125.766, 601.978),
        ("1041-sr_B-1-new-deadline_7.csv", True, 24.379, 31.006),
        ("1053-af_B-1-new-deadline_7.csv", True, 27.913, 125.326),
        ("2177-mix-2-new-deadline_2.csv", True, 41.922, 42.123),
        ("3319-af_B-3-running-deadline_4.csv", True, 78.598, 173.138),
        ("3337-mix-3-running-deadline_4.csv", True, 13.941, 41.408),
        ("3509-mix-3-running-deadline_5.csv", False, None, None),
        ("3569-mix-3-running-deadline_7.csv", False, None, None),
        ("4405-hog_B-4-new-deadline_6.csv", False, None, None),
    ]
)
def medf_expected_schedule(request):
    return request.param


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_tetris_medf(datadir, medf_expected_schedule):
    run_tetris_scheduler(datadir, "medf", medf_expected_schedule)


@pytest.fixture(
    params=[
        ("3319-af_B-3-running-deadline_4.csv", True, 78.598, 173.138),
        ("3337-mix-3-running-deadline_4.csv", True, 13.941, 41.408),
    ]
)
def medf_rot_expected_schedule(request):
    return request.param


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_tetris_medf_rotations(datadir, medf_rot_expected_schedule):
    run_tetris_scheduler(
        datadir,
        "medf",
        medf_rot_expected_schedule,
        "+resource_manager.rotations=True",
    )


@pytest.fixture(
    params=[
        ("hog-1.csv", True, 12.663, 11.866),
        ("hog-1-2.csv", True, 12.353, 14.254),
        ("hog-big-5-d.csv", False, None, None),
        ("1041-sr_B-1-new-deadline_7.csv", True, 24.379, 31.006),
        ("2177-mix-2-new-deadline_2.csv", True, 41.922, 42.123),
        ("3319-af_B-3-running-deadline_4.csv", True, 62.667, 158.809),
        ("3337-mix-3-running-deadline_4.csv", True, 11.015, 43.016),
        ("3569-mix-3-running-deadline_7.csv", False, None, None),
        ("4405-hog_B-4-new-deadline_6.csv", False, None, None),
    ]
)
def segmedf_expected_schedule(request):
    return request.param


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_tetris_segmedf(datadir, segmedf_expected_schedule):
    run_tetris_scheduler(datadir, "seg_medf", segmedf_expected_schedule)


@pytest.fixture(
    params=[
        ("hog-1-2.csv", True, 12.353, 14.254),
        ("hog-big-5-d.csv", True, 85.747, 357.768),
        ("hog-big-8-d.csv", True, 114.298, 626.054),
        ("2057-sr_B-2-running-deadline_2.csv", True, 39.027, 44.970),
        ("2177-mix-2-new-deadline_2.csv", True, 41.922, 42.123),
        ("3319-af_B-3-running-deadline_4.csv", True, 67.103, 147.956),
        ("3337-mix-3-running-deadline_4.csv", True, 12.676, 40.076),
        ("3509-mix-3-running-deadline_5.csv", True, 37.127, 105.081),
        ("4405-hog_B-4-new-deadline_6.csv", False, None, None),
    ]
)
def seglr_expected_schedule(request):
    return request.param


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_tetris_seglr(datadir, seglr_expected_schedule):
    run_tetris_scheduler(datadir, "seg_lr", seglr_expected_schedule)


@pytest.fixture(
    params=[
        ("hog-1-2.csv",),
        ("2177-mix-2-new-deadline_2.csv",),
    ]
)
def seglr_rdp_expected_schedule(request):
    return request.param


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_tetris_seglr_rdp(datadir, seglr_rdp_expected_schedule):
    run_tetris_scheduler(
        datadir,
        "seg_lr",
        seglr_rdp_expected_schedule,
        options="resource_manager.seg_lr_constraints=['R','D','RDP']",
        check_result=False,
    )


@pytest.fixture(
    params=[
        ("hog-1.csv", True, 12.663, 11.866),
        ("1053-af_B-1-new-deadline_7.csv", True, 27.913, 125.326),
        ("2177-mix-2-new-deadline_2.csv", True, 41.922, 42.123),
        ("3569-mix-3-running-deadline_7.csv", False, None, None),
        ("3658-mix-3-running-deadline_6.csv", True, 10.692, 46.171),
        ("4412-hog_B-4-running-deadline_6.csv", True, 80.760, 238.836),
    ]
)
def bf_expected_schedule(request):
    return request.param


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_tetris_bf(datadir, bf_expected_schedule):
    run_tetris_scheduler(datadir, "bf", bf_expected_schedule)


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_tetris_bf_mem(datadir, bf_expected_schedule):
    run_tetris_scheduler(datadir, "bf-mem", bf_expected_schedule)


@pytest.fixture(
    params=[
        ("3337-mix-3-running-deadline_4.csv", True, 14.803, 36.681),
    ]
)
def bf_nomig_expected_schedule(request):
    return request.param


@pytest.fixture(
    params=[
        ("2177-mix-2-new-deadline_2.csv", True, 41.922, 42.123),
    ]
)
def bf_rot_nomig_expected_schedule(request):
    return request.param


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_tetris_bf_nomig(datadir, bf_nomig_expected_schedule):
    run_tetris_scheduler(
        datadir,
        "bf",
        bf_nomig_expected_schedule,
        options="+resource_manager.migrations=False",
    )


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_tetris_bf_rot_nomig(datadir, bf_rot_nomig_expected_schedule):
    run_tetris_scheduler(
        datadir,
        "bf",
        bf_rot_nomig_expected_schedule,
        options="+resource_manager.migrations=False +resource_manager.rotations=True",
    )


@pytest.fixture(
    params=[
        "hog-big-8-d-online.csv",
    ]
)
def tetris_manager_test(request):
    return request.param


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_tetris_manager(datadir, expected_dir, tetris_manager_test):
    testname = os.path.splitext(tetris_manager_test)[0]
    input_scn = os.path.join(
        datadir, "tetris", "request_trace", "{}.csv".format(testname)
    )
    out_name = "{}_{}.out".format("manager", testname)
    out_path = os.path.join(datadir, out_name)
    tetris_base = os.path.join(datadir, "tetris", "apps")
    cmd = (
        "mocasin "
        + "tetris_manager "
        + "tetris_apps_dir={} ".format(tetris_base)
        + "input_jobs={} ".format(input_scn)
        + "resource_manager={} ".format("medf")
        + "platform=exynos "
        + "log_level=INFO "
        + "output_trace={} ".format(out_path)
    )
    subprocess.check_call(cmd.split(), cwd=datadir)

    # TODO: Add output
