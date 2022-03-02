# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Robert Khasanov, Felix Teweleit, Andres Goens

import csv
import numpy as np
from pathlib import Path
import pytest
import subprocess

from mocasin.mapper.pareto import _is_pareto_efficient


def check_pareto_optimality(path):
    """Check whether the generated pareto set is Pareto-optimal."""
    with open(path, "r") as file:
        csv_reader = csv.DictReader(file)
        fieldnames = csv_reader.fieldnames
        processes = [x for x in fieldnames if x.startswith("t_")]

        # collect all processors
        processors = set()
        for row in csv_reader:
            for p in processes:
                processors.add(row[p])
        proc_dict = {}
        for i, proc in enumerate(processors):
            proc_dict[proc] = i

        # start reading from the beginning
        file.seek(0)
        next(csv_reader)

        # initialize costs array
        costs = np.empty((0, len(processors) + 2), float)
        no_energy = False

        # collect costs
        for row in csv_reader:
            lm = [0] * len(processors)
            # mark used processors
            for p in processes:
                lm[proc_dict[row[p]]] = 1
            # execution time
            assert row["executionTime"] != ""
            lm.append(float(row["executionTime"]))
            # energy
            if row["dynamicEnergy"] == "":
                no_energy = True
                lm.append(0)
            else:
                lm.append(float(row["dynamicEnergy"]))
            costs = np.append(costs, [lm], axis=0)

        # assert that all mappings either have or not have energy data
        if no_energy:
            assert np.all(costs[:, len(processors) + 1] == 0)

        # calculate pareto front
        flags = _is_pareto_efficient(costs)
        return np.all(flags)


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


def test_pareto_front_tgff_exynos990(datadir):
    out_csv_file = Path(datadir).joinpath("mappings.csv")
    subprocess.check_call(
        [
            "mocasin",
            "pareto_front",
            "graph=tgff_reader",
            "platform=exynos990",
            "tgff.directory=tgff/e3s-0.9",
            "tgff.file=auto-indust-cords.tgff",
            f"mapping_table={out_csv_file}",
            "mapper.objectives=[exec_time,resources]",
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )

    assert check_pareto_optimality(out_csv_file)


@pytest.mark.parametrize(
    "objectives", ["[exec_time,resources]", "[exec_time,resources,energy]"]
)
def test_pareto_front_tgff_odroid(datadir, objectives):
    out_csv_file = Path(datadir).joinpath("mappings.csv")
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

    assert check_pareto_optimality(out_csv_file)


@pytest.mark.parametrize(
    "evaluate_metadata,suffix",
    [
        ("True", "eval"),
        ("False", "noeval"),
    ],
)
def test_pareto_front_tgff_odroid_fair(
    datadir, evaluate_metadata, suffix, expected_dir
):
    out_csv_file = Path(datadir).joinpath("mappings.csv")
    expected_filename = f"mappings_auto-indust-cords_odroid_fair_{suffix}.csv"
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
            f"evaluate_metadata={evaluate_metadata}",
        ],
        cwd=datadir,
    )

    if evaluate_metadata == "True":
        assert check_pareto_optimality(out_csv_file)
    assert compare_mapping_tables(out_csv_file, expected_csv)
