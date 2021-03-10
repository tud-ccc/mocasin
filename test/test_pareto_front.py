# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

from pathlib import Path
import subprocess


def test_pareto_front_tgff(datadir):
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
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )
    assert out_csv_file.is_file()
