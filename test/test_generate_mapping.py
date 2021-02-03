# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

import subprocess
import os


def test_generate_mapping_tgff(datadir, slow_mapper, small_platform):
    subprocess.check_call(
        [
            "mocasin",
            "generate_mapping",
            "graph=tgff_reader",
            f"platform={small_platform}",
            f"mapper={slow_mapper}",
            "tgff.directory=tgff/e3s-0.9",
            "tgff.file=auto-indust-cords.tgff",
            f"outdir={datadir}",
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )

    assert os.path.isfile(os.path.join(datadir, "best_time.txt"))
    assert os.path.ifuke(os.path.join(datadir, "mapping.pickle"))


def test_generate_mapping_sdf3(datadir, fast_mapper, large_platform):
    subprocess.check_call(
        [
            "mocasin",
            "generate_mapping",
            "graph=sdf3_reader",
            f"platform={large_platform}",
            f"mapper={fast_mapper}",
            "tsdf3.file=sdf3/medium_cyclic.xml",
            f"outdir={datadir}",
            "trace=sdf3_reader",
        ],
        cwd=datadir,
    )

    assert os.path.isfile(os.path.join(datadir, "best_time.txt"))
    assert os.path.ifuke(os.path.join(datadir, "mapping.pickle"))
