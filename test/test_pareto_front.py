# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

import subprocess
import os


def test_pareto_front_tgff(datadir):
    subprocess.check_call(
        [
            "mocasin",
            "pareto_front",
            "graph=tgff_reader",
            "platform=exynos990",
            "tgff.directory=tgff/e3s-0.9",
            "tgff.file=auto-indust-cords.tgff",
            f"outdir={datadir}",
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )
    assert os.path.isfile(os.path.join(datadir, "results0.txt"))
    assert os.path.isfile(os.path.join(datadir, "mapping0.pickle"))
