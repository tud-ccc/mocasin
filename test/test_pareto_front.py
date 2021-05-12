# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens, Robert Khasanov

import csv
from pathlib import Path
import pytest
import subprocess
import sys


def compare_mapping_tables(path1, path2):
    """Compare two mapping tables."""
    with open(path1, "r") as file1:
        with open(path2, "r") as file2:
            csv1 = csv.DictReader(file1)
            csv2 = csv.DictReader(file2)
            if csv1.fieldnames != csv2.fieldnames:
                return False
            fieldnames = csv1.fieldnames
            for row1, row2 in zip(csv1, csv2):
                for field in fieldnames:
                    if field in ["executionTime", "dynamicEnergy"]:
                        if bool(row1[field]) ^ bool(row2[field]):
                            return False
                        if row1[field] == row2[field] == "":
                            continue
                        if abs(float(row1[field]) - float(row2[field])) > 1e-6:
                            return False
                        continue
                    if row1[field] != row2[field]:
                        return False
            if len(list(csv1)) or len(list(csv2)):
                return False
            return True


# This test relies on hard-coded results that depend on  multiple
# parameters. Thus, a failing test here does not mean incorrect
# behavior. Instead, this test should check for an invariant of
# the actual function. In the case of the pareto front, for example,
# a better test might check that indeed no point dominates any other
# point, which means it is a pareto front, and is invariant of the
# parameters in the algorithms
@pytest.mark.xfail
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
            f"mapper.objectives=[exec_time,resources]",
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )

    # On Python 3.6 different mappings are generated. This might be due to
    # implementation in the library.
    if sys.version_info >= (3, 7):
        assert compare_mapping_tables(out_csv_file, expected_csv)
    else:
        assert out_csv_file.is_file()


@pytest.mark.parametrize(
    "objectives,suffix",
    [
        ("[exec_time,resources]", "tr"),
        ("[exec_time,resources,energy]", "etr"),
    ],
)
@pytest.mark.xfail
def test_pareto_front_tgff_odroid(datadir, objectives, suffix, expected_dir):
    out_csv_file = Path(datadir).joinpath("mappings.csv")
    expected_filename = f"mappings_auto-indust-cords_odroid_{suffix}.csv"
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

    # On Python 3.6 different mappings are generated. This might be due to
    # implementation in the library.
    if sys.version_info >= (3, 7):
        assert compare_mapping_tables(out_csv_file, expected_csv)
    else:
        assert out_csv_file.is_file()


def test_pareto_front_tgff_odroid_fair(datadir, expected_dir):
    out_csv_file = Path(datadir).joinpath("mappings.csv")
    expected_filename = f"mappings_auto-indust-cords_odroid_fair.csv"
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
            "mapper=static_cfs",
            "trace=tgff_reader",
            "evaluate_metadata=True",
        ],
        cwd=datadir,
    )

    assert filecmp.cmp(out_csv_file, expected_csv, shallow=False)
