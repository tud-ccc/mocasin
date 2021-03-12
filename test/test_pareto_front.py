# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

from pathlib import Path
import pytest
import subprocess


@pytest.fixture(
    params=['"exec_time;resources"', '"exec_time;resources;energy"']
)
def objectives(request):
    return request.param


def test_pareto_front_tgff(datadir, objectives):
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
            f"mapper.objectives={objectives}",
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )
    assert out_csv_file.is_file()
