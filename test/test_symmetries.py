# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

import subprocess
import pytest
import filecmp
import os


@pytest.mark.skip(reason="Test just takes too long.")
def test_symmetries_tgff_large(datadir, large_platform):
    subprocess.check_call(
        [
            "mocasin",
            "generate_mapping",
            "graph=tgff_reader",
            "tgff.directory=tgff/e3s-0.9",
            "tgff.file=auto-indust-cords.tgff",
            f"platform={large_platform}",
            "representation=Symmetries",
            "mapper=genetic",
            f"outdir={datadir}/mpsym/",
            f"platform.symmetries_json=platform/symmetries/{large_platform}.json",
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )

    subprocess.check_call(
        [
            "mocasin",
            "generate_mapping",
            "graph=tgff_reader",
            "tgff.directory=tgff/e3s-0.9",
            "tgff.file=auto-indust-cords.tgff",
            f"platform={large_platform}",
            "representation=Symmetries",
            "representation.disable_mpsym=true",
            "mapper=genetic",
            f"outdir={datadir}/python/",
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )

    assert filecmp.cmp(
        os.path.join(datadir, "mpsym/best_time.txt"),
        os.path.join(datadir, "python/best_time.txt"),
        shallow=False,
    )


def test_symmetries_tgff_small(datadir, small_platform):
    subprocess.check_call(
        [
            "mocasin",
            "generate_mapping",
            "graph=tgff_reader",
            "tgff.directory=tgff/e3s-0.9",
            "tgff.file=auto-indust-cords.tgff",
            f"platform={small_platform}",
            "representation=Symmetries",
            "mapper=genetic",
            "mapper.random_seed=42",
            f"outdir={datadir}/mpsym/",
            f"platform.symmetries_json=platform/symmetries/{small_platform}.json",
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )

    subprocess.check_call(
        [
            "mocasin",
            "generate_mapping",
            "graph=tgff_reader",
            "tgff.directory=tgff/e3s-0.9",
            "tgff.file=auto-indust-cords.tgff",
            f"platform={small_platform}",
            "representation=Symmetries",
            "representation.disable_mpsym=true",
            "mapper=genetic",
            "mapper.random_seed=42",
            f"outdir={datadir}/python/",
            "trace=tgff_reader",
        ],
        cwd=datadir,
    )

    assert filecmp.cmp(
        os.path.join(datadir, "mpsym/best_time.txt"),
        os.path.join(datadir, "python/best_time.txt"),
        shallow=False,
    )
