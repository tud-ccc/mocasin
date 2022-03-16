# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Julian Robledo

import pytest
from mocasin.platforms.platformDesigner import (
    PlatformDesigner,
    genericProcessor,
)
from mocasin.common.platform import Platform
from mocasin.platforms.odroid import DesignerPlatformOdroid
from mocasin.platforms.haec import DesignerPlatformHAEC
from mocasin.platforms.exynos990 import DesignerPlatformExynos990
from mocasin.platforms.generic_mesh import DesignerPlatformMesh
from mocasin.platforms.mppa_coolidge import DesignerPlatformCoolidge
from mocasin.platforms.multi_cluster import DesignerPlatformMultiCluster
from mocasin.platforms.generic_bus import DesignerPlatformBus
from mocasin.platforms.generic_bus import GenericBusPlatform


@pytest.fixture(
    params=[
        "exynos990",
        "odroid",
        "generic_bus",
        "flat_bus",
        "generic_mesh",
        "multi_cluster",
        "haec",
        "coolidge",
    ]
)
def platform(request):
    processor0 = genericProcessor("proc_type_0")
    processor1 = genericProcessor("proc_type_1")
    processor2 = genericProcessor("proc_type_2")
    processor3 = genericProcessor("proc_type_3")

    if request.param == "exynos990":
        return DesignerPlatformExynos990(
            processor0, processor1, processor2, processor3
        )
    elif request.param == "odroid":
        return DesignerPlatformOdroid(processor0, processor1)
    elif request.param == "generic_bus":
        return DesignerPlatformBus(processor0)
    elif request.param == "flat_bus":
        return GenericBusPlatform("bus", 4)
    elif request.param == "generic_mesh":
        return DesignerPlatformMesh(processor0, processor1)
    elif request.param == "multi_cluster":
        return DesignerPlatformMultiCluster(processor0, processor1)
    elif request.param == "haec":
        return DesignerPlatformHAEC(processor0)
    elif request.param == "coolidge":
        return DesignerPlatformCoolidge(processor0, processor1)
    else:
        assert False, "wrong parameter"


@pytest.fixture
def DAG():
    return {
        0: [1, 2],
        1: [3, 4],
        2: [5, 6],
        3: [7],
        4: [9],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [8],
    }


@pytest.fixture
def cyclicGraph():
    return {
        0: [1, 4, 7],
        1: [0, 2, 4],
        2: [1, 3, 7],
        3: [2, 6, 8],
        4: [0, 1, 5, 7],
        5: [4, 6, 8],
        6: [3, 5],
        7: [0, 2, 4, 8],
        8: [3, 5, 7, 9],
        9: [8],
    }


@pytest.fixture
def designer():
    platformObject = Platform("test")
    designer = PlatformDesigner(platformObject)
    designer.setSchedulingPolicy("TestPolicy", 1000)
    return designer


@pytest.fixture
def peListShort():
    return ["PE00", "PE01", "PE02", "PE03"]


@pytest.fixture
def peList():
    return [
        "PE00",
        "PE01",
        "PE02",
        "PE03",
        "PE04",
        "PE05",
        "PE06",
        "PE07",
        "PE08",
        "PE09",
    ]


@pytest.fixture
def peListNineElems():
    return [
        "PE00",
        "PE01",
        "PE02",
        "PE03",
        "PE04",
        "PE05",
        "PE06",
        "PE07",
        "PE08",
    ]


@pytest.fixture
def peListLong():
    return [
        "PE00",
        "PE01",
        "PE02",
        "PE03",
        "PE04",
        "PE05",
        "PE06",
        "PE07",
        "PE08",
        "PE09",
        "PE10",
        "PE11",
        "PE12",
        "PE13",
        "PE14",
        "PE15",
        "PE16",
        "PE17",
        "PE18",
        "PE19",
    ]


@pytest.fixture
def peListTorus():
    return [
        "PE00",
        "PE01",
        "PE02",
        "PE03",
        "PE04",
        "PE05",
        "PE06",
        "PE07",
        "PE08",
        "PE09",
        "PE10",
        "PE11",
        "PE12",
        "PE13",
        "PE14",
        "PE15",
    ]
