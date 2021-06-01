# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andres Goens, Felix Teweleit

import subprocess
import os
import mpsym
from mocasin.platforms.exynos990 import DesignerPlatformExynos990
from mocasin.platforms.generic_bus import DesignerPlatformBus
from mocasin.platforms.generic_mesh import DesignerPlatformMesh
from mocasin.platforms.odroid import DesignerPlatformOdroid
from mocasin.platforms.multi_cluster import DesignerPlatformMultiCluster
from mocasin.platforms.platformDesigner import genericProcessor
from mocasin.representations.automorphisms import checkSymmetries


def test_calculate_platform_symmetries(datadir, small_platform):
    file_name = f"{small_platform}.autgrp.json"
    out_file = os.path.join(datadir, file_name)

    subprocess.check_call(
        [
            "mocasin",
            "calculate_platform_symmetries",
            f"platform={small_platform}",
            f"out_file={out_file}",
        ],
        cwd=datadir,
    )

    # ideally we would call hydra.instantiate here,
    # but I don't know how to do this in pytest.
    processor0 = genericProcessor("proc_type_0", 2000000000)
    processor1 = genericProcessor("proc_type_1", 3000000000)
    processor2 = genericProcessor("proc_type_2", 4000000000)
    processor3 = genericProcessor("proc_type_3", 5000000000)

    if small_platform == "multi_cluster":
        platform = DesignerPlatformMultiCluster(processor0, processor1)
    elif small_platform == "generic_mesh":
        platform = DesignerPlatformMesh(processor0, processor1)
    elif small_platform == "generic_bus":
        platform = DesignerPlatformBus(processor0)
    elif small_platform == "exynos990":
        platform = DesignerPlatformExynos990(
            processor0, processor1, processor2, processor3
        )
    elif small_platform == "odroid":
        platform = DesignerPlatformOdroid(processor0, processor1)

    ag = mpsym.ArchGraphSystem.from_json_file(out_file)
    assert checkSymmetries(platform.to_adjacency_dict(), ag.automorphisms())
