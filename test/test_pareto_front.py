# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens, Robert Khasanov

import filecmp
from pathlib import Path
import pytest
import subprocess
import sys


@pytest.fixture(
    params=['"exec_time;resources"', '"exec_time;resources;energy"']
)
def objectives(request):
    return request.param


def get_suffix(objective_string):
    suffix = ""
    for obj in sorted(objective_string.strip('"').split(";")):
        if obj == "energy":
            suffix += "e"
            continue
        if obj == "exec_time":
            suffix += "t"
            continue
        if obj == "resources":
            suffix += "r"
            continue
        raise RuntimeError(f"Unknonwn objective {obj}")
    return suffix


def test_pareto_front_tgff_exynos990(datadir, expected_dir):
    out_csv_file = Path(datadir).joinpath("mappings.csv")
    expected_filename = f"mappings_auto-indust-cords_exynos990_tr.csv"
    expected_csv = Path(expected_dir).joinpath(expected_filename)
    subprocess.check_call(
        [
            "mocasin",
            "pareto_front",
            "graph=tgff_reader",
            "platform=exynos990",
            "tgff.directory=tgff/e3s-0.9",
            "tgff.file=auto-indust-cords.tgff",
            f"mapping_table={out_csv_file}",
            f'mapper.objectives="exec_time;resources"',
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )

    # On Python 3.6 different mappings is generated. This might be due to
    # implementation in the library.
    if sys.version_info >= (3, 7):
        assert filecmp.cmp(out_csv_file, expected_csv, shallow=False)
    else:
        assert out_csv_file.is_file()


# This is a placeholder of the test, checking that depending on the different
# objective list we produce different mapping table. Once the branch
# "odroid_freq" is merged to master, the expected tables should be updated
# correspondingly
def test_pareto_front_tgff_odroid(datadir, objectives, expected_dir):
    out_csv_file = Path(datadir).joinpath("mappings.csv")
    expected_filename = (
        f"mappings_auto-indust-cords_odroid_{get_suffix(objectives)}.csv"
    )
    expected_csv = Path(expected_dir).joinpath(expected_filename)
    subprocess.check_call(
        [
            "mocasin",
            "pareto_front",
            "graph=tgff_reader",
            "platform=odroid",
            "tgff.directory=tgff/e3s-0.9",
            "tgff.file=auto-indust-cords.tgff",
            f"mapping_table={out_csv_file}",
            f"mapper.objectives={objectives}",
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )

    # On Python 3.6 different mappings is generated. This might be due to
    # implementation in the library.
    if sys.version_info >= (3, 7):
        assert filecmp.cmp(out_csv_file, expected_csv, shallow=False)
    else:
        assert out_csv_file.is_file()
