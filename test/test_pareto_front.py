# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

import subprocess
import os
import pytest


@pytest.mark.xfail(reason="Required files are not in the repository anymore")
def test_pareto_front_maps(datadir, maps_kpn, representation):
    subprocess.check_call(
        [
            "mocasin",
            "pareto_front",
            "kpn=%s" % maps_kpn,
            "platform=exynos",
            "platform.embedding_json=None",
            "representation=%s" % representation,
            "outdir=../../../",
            "trace=maps_default",
        ],
        cwd=datadir,
    )

    try:
        file_path = os.path.join(datadir, "mapping0.pickle")
        file = open(file_path, "r")
        file.close()
    except FileNotFoundError:
        assert False


def test_pareto_front_tgff(datadir, tgff):
    tgff_dir = os.path.join(datadir, "tgff/e3s-0.9")
    subprocess.check_call(
        [
            "mocasin",
            "pareto_front",
            "kpn=tgff_reader",
            "platform=exynos990",
            "tgff.directory=%s" % tgff_dir,
            "tgff.file=%s.tgff" % tgff,
            "outdir=../../../",
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )
    try:
        file_path = os.path.join(datadir, "results0.txt")
        file = open(file_path, "r")
        file.close()
    except FileNotFoundError:
        assert False
