# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard, Andres Goens, Felix Teweleit

import os
import subprocess


def test_enumerate_equivalent_tgff(datadir):
    out_file = os.path.join(datadir, "mappings.txt")

    subprocess.check_call(
        [
            "mocasin",
            "enumerate_equivalent",
            "graph=tgff_reader",
            "platform=exynos990",
            "tgff.directory=tgff/e3s-0.9",
            "tgff.file=auto-indust-cords.tgff",
            "mapper=default",
            f"output_file={out_file}",
        ],
        cwd=datadir,
    )

    # Todo: compare with expected result after merge with gbm_mapper branch
    assert os.stat(out_file).st_size > 0
