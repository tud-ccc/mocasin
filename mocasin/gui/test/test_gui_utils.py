# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from mocasin.gui.utils import listOperations as lo
from mocasin.gui.utils import platformOperations as po
import pytest


class TestListOperations(object):
    def test_convertToMatrix_1(self):
        testList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert lo.convertToMatrix(testList) == result

    def test_convertToMatrix_2(self):
        testList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        result = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        assert lo.convertToMatrix(testList) == result

    def test_convertToMatrix_3(self):
        testList = [1, 2, 3, 4, 5, 6, 7]
        result = [[1, 2, 3], [4, 5, 6], [7]]
        assert lo.convertToMatrix(testList) == result

    def test_convertToMatrix_4(self):
        testList = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
        ]
        result = [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            [11, 12, 13, 14, 15],
            [16, 17, 18, 19],
        ]
        assert lo.convertToMatrix(testList) == result

    def test_getDimension_1(self):
        testMatrix = [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            [11, 12, 13, 14, 15],
            [16, 17, 18, 19],
        ]
        assert lo.getDimension(testMatrix) == 5

    def test_getDimension_2(self):
        testMatrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
        ]
        assert lo.getDimension(testMatrix) == 4

    def test_getDimension_3(self):
        testMatrix = [1]
        assert lo.getDimension(testMatrix) == 1

    def test_getDimension_4(self):
        testMatrix = 1
        assert lo.getDimension(testMatrix) == 1

    def test_containsItem_1(self):
        testList = [1, 2, 3, 4, 5]
        assert lo.containsItem(testList, 5)

    def test_containsItem_2(self):
        testList = (1, 2)
        assert lo.containsItem(testList, 2)

    def test_containsItem_3(self):
        testList = [[1, 2, [2, 3, 4]], [9], [23], (1, [9])]
        assert lo.containsItem(testList, 3)

    def test_containsItem_4(self):
        testList = [[1, 2, [2, 3, 4]], [9], [23], (1, [9])]
        assert lo.containsItem(testList, 9)

    def test_containsItem_5(self):
        testList = [[1, 2, [2, 3, 4]], [9], [23], (1, [9])]
        assert not lo.containsItem(testList, 34)


class TestPlatformOperations(object):
    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_peToString_1(self, exynos):
        result = po.peToString(exynos.processors())
        assert result == [
            "ARM00",
            "ARM01",
            "ARM02",
            "ARM03",
            "ARM04",
            "ARM05",
            "ARM06",
            "ARM07",
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_peToString_2(self, parallella):
        result = po.peToString(parallella.processors())
        assert result == [
            "ARM0",
            "ARM1",
            "E00",
            "E01",
            "E02",
            "E03",
            "E04",
            "E05",
            "E06",
            "E07",
            "E08",
            "E09",
            "E10",
            "E11",
            "E12",
            "E13",
            "E14",
            "E15",
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_peToString_3(self, multiDSP):
        result = po.peToString(multiDSP.processors())
        assert result == ["dsp0", "dsp1", "dsp2", "dsp3", "dsp4"]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_getSortedProcessorScheme_1(self, exynos):
        result = po.peToString(exynos.processors())
        result = po.getSortedProcessorScheme(result)
        assert result == [
            "ARM00",
            "ARM01",
            "ARM02",
            "ARM03",
            "ARM04",
            "ARM05",
            "ARM06",
            "ARM07",
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_getSortedProcessorScheme_2(self, parallella):
        result = po.peToString(parallella.processors())
        result = po.getSortedProcessorScheme(result)
        assert result == [
            "ARM0",
            "E00",
            "ARM1",
            "E01",
            "E02",
            "E03",
            "E04",
            "E05",
            "E06",
            "E07",
            "E08",
            "E09",
            "E10",
            "E11",
            "E12",
            "E13",
            "E14",
            "E15",
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_getSortedProcessorScheme_3(self, multiDSP):
        result = po.peToString(multiDSP.processors())
        result = po.getSortedProcessorScheme(result)
        assert result == ["dsp0", "dsp1", "dsp2", "dsp3", "dsp4"]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_getMembersOfPrimitive_1(self, exynos):
        primitive = exynos.find_primitive("comm_DRAM")
        result = po.getMembersOfPrimitive(primitive)
        assert result == [
            "ARM00",
            "ARM01",
            "ARM02",
            "ARM03",
            "ARM04",
            "ARM05",
            "ARM06",
            "ARM07",
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_getMembersOfPrimitive_2(self, parallella):
        primitive = parallella.find_primitive("EMEM")
        result = po.getMembersOfPrimitive(primitive)
        assert result == [
            "ARM0",
            "ARM1",
            "E00",
            "E01",
            "E02",
            "E03",
            "E04",
            "E05",
            "E06",
            "E07",
            "E08",
            "E09",
            "E10",
            "E11",
            "E12",
            "E13",
            "E14",
            "E15",
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_getMembersOfPrimitive_3(self, multiDSP):
        primitive = multiDSP.find_primitive("comm_cp_shared_shared_memory")
        result = po.getMembersOfPrimitive(primitive)
        assert result == ["dsp0", "dsp1", "dsp2", "dsp3", "dsp4"]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_getPlatformDescription_1(self, exynos):
        processors = exynos.processors()
        primitives = exynos.primitives()
        result = po.getPlatformDescription(processors, primitives)
        assert result == [
            (
                "comm_DRAM",
                [
                    (
                        "comm_DRAM",
                        [
                            (
                                "comm_L2_A7",
                                [
                                    (
                                        "comm_L2_A7",
                                        [
                                            (
                                                "comm_L1_ARM00",
                                                [("comm_L1_ARM00", ["ARM00"])],
                                            ),
                                            (
                                                "comm_L1_ARM01",
                                                [("comm_L1_ARM01", ["ARM01"])],
                                            ),
                                            (
                                                "comm_L1_ARM02",
                                                [("comm_L1_ARM02", ["ARM02"])],
                                            ),
                                            (
                                                "comm_L1_ARM03",
                                                [("comm_L1_ARM03", ["ARM03"])],
                                            ),
                                        ],
                                    )
                                ],
                            ),
                            (
                                "comm_L2_A15",
                                [
                                    (
                                        "comm_L2_A15",
                                        [
                                            (
                                                "comm_L1_ARM04",
                                                [("comm_L1_ARM04", ["ARM04"])],
                                            ),
                                            (
                                                "comm_L1_ARM05",
                                                [("comm_L1_ARM05", ["ARM05"])],
                                            ),
                                            (
                                                "comm_L1_ARM06",
                                                [("comm_L1_ARM06", ["ARM06"])],
                                            ),
                                            (
                                                "comm_L1_ARM07",
                                                [("comm_L1_ARM07", ["ARM07"])],
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            )
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_getPlatformDescription_2(self, parallella):
        processors = parallella.processors()
        primitives = parallella.primitives()
        result = po.getPlatformDescription(processors, primitives)
        assert result == [
            (
                "EMEM",
                [
                    ("hostToHostCached", ["ARM0", "ARM1"]),
                    (
                        "meshDirect_E15",
                        [
                            (
                                "meshDirect_E14",
                                [
                                    (
                                        "meshDirect_E13",
                                        [
                                            (
                                                "meshDirect_E12",
                                                [
                                                    (
                                                        "meshDirect_E11",
                                                        [
                                                            (
                                                                "meshDirect_E10",
                                                                [
                                                                    (
                                                                        "meshDirect_E09",
                                                                        [
                                                                            (
                                                                                "meshDirect_E08",
                                                                                [
                                                                                    (
                                                                                        "meshDirect_E07",
                                                                                        [
                                                                                            (
                                                                                                "meshDirect_E06",
                                                                                                [
                                                                                                    (
                                                                                                        "meshDirect_E05",
                                                                                                        [
                                                                                                            (
                                                                                                                "meshDirect_E04",
                                                                                                                [
                                                                                                                    (
                                                                                                                        "meshDirect_E03",
                                                                                                                        [
                                                                                                                            (
                                                                                                                                "meshDirect_E02",
                                                                                                                                [
                                                                                                                                    (
                                                                                                                                        "meshDirect_E01",
                                                                                                                                        [
                                                                                                                                            (
                                                                                                                                                "meshDirect_E00",
                                                                                                                                                [
                                                                                                                                                    "E00",
                                                                                                                                                    "E01",
                                                                                                                                                    "E02",
                                                                                                                                                    "E03",
                                                                                                                                                    "E04",
                                                                                                                                                    "E05",
                                                                                                                                                    "E06",
                                                                                                                                                    "E07",
                                                                                                                                                    "E08",
                                                                                                                                                    "E09",
                                                                                                                                                    "E10",
                                                                                                                                                    "E11",
                                                                                                                                                    "E12",
                                                                                                                                                    "E13",
                                                                                                                                                    "E14",
                                                                                                                                                    "E15",
                                                                                                                                                ],
                                                                                                                                            )
                                                                                                                                        ],
                                                                                                                                    )
                                                                                                                                ],
                                                                                                                            )
                                                                                                                        ],
                                                                                                                    )
                                                                                                                ],
                                                                                                            )
                                                                                                        ],
                                                                                                    )
                                                                                                ],
                                                                                            )
                                                                                        ],
                                                                                    )
                                                                                ],
                                                                            )
                                                                        ],
                                                                    )
                                                                ],
                                                            )
                                                        ],
                                                    )
                                                ],
                                            )
                                        ],
                                    )
                                ],
                            )
                        ],
                    ),
                ],
            )
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_getPlatformDescription_3(self, multiDSP):
        processors = multiDSP.processors()
        primitives = multiDSP.primitives()
        result = po.getPlatformDescription(processors, primitives)
        assert result == [
            (
                "comm_cp_shared_shared_memory",
                ["dsp0", "dsp1", "dsp2", "dsp3", "dsp4"],
            )
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_findEqualPrimitives_1(self, exynos):
        result = po.findEqualPrimitives(exynos)
        assert result == [
            ["comm_L1_ARM00", "comm_L1_ARM00_putget"],
            ["comm_L1_ARM01", "comm_L1_ARM01_putget"],
            ["comm_L1_ARM02", "comm_L1_ARM02_putget"],
            ["comm_L1_ARM03", "comm_L1_ARM03_putget"],
            ["comm_L1_ARM04", "comm_L1_ARM04_putget"],
            ["comm_L1_ARM05", "comm_L1_ARM05_putget"],
            ["comm_L1_ARM06", "comm_L1_ARM06_putget"],
            ["comm_L1_ARM07", "comm_L1_ARM07_putget"],
            ["comm_L2_A7", "comm_L2_A7_putget"],
            ["comm_L2_A15", "comm_L2_A15_putget"],
            ["comm_DRAM", "comm_DRAM_putget"],
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_findEqualPrimitives_2(self, parallella):
        result = po.findEqualPrimitives(parallella)
        assert result == [
            ["EMEM"],
            ["hostToHostCached"],
            [
                "meshDirect_E00",
                "meshDirect_E01",
                "meshDirect_E02",
                "meshDirect_E03",
                "meshDirect_E04",
                "meshDirect_E05",
                "meshDirect_E06",
                "meshDirect_E07",
                "meshDirect_E08",
                "meshDirect_E09",
                "meshDirect_E10",
                "meshDirect_E11",
                "meshDirect_E12",
                "meshDirect_E13",
                "meshDirect_E14",
                "meshDirect_E15",
            ],
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_findEqualPrimitives_3(self, multiDSP):
        result = po.findEqualPrimitives(multiDSP)
        assert result == [["comm_cp_shared_shared_memory"]]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_mergeEqualPrimitives_1(self, exynos):
        processors = exynos.processors()
        primitives = exynos.primitives()
        platformDescription = po.getPlatformDescription(processors, primitives)
        equalList = po.findEqualPrimitives(exynos)
        result = po.mergeEqualPrimitives(platformDescription, equalList)
        assert result == [
            (
                "comm_DRAM",
                [
                    (
                        "comm_L2_A7",
                        [
                            ("network_on_chip", ["ARM00"]),
                            ("network_on_chip", ["ARM01"]),
                            ("network_on_chip", ["ARM02"]),
                            ("network_on_chip", ["ARM03"]),
                        ],
                    ),
                    (
                        "comm_L2_A15",
                        [
                            ("network_on_chip", ["ARM04"]),
                            ("network_on_chip", ["ARM05"]),
                            ("network_on_chip", ["ARM06"]),
                            ("network_on_chip", ["ARM07"]),
                        ],
                    ),
                ],
            )
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_mergeEqualPrimitives_2(self, parallella):
        processors = parallella.processors()
        primitives = parallella.primitives()
        platformDescription = po.getPlatformDescription(processors, primitives)
        equalList = po.findEqualPrimitives(parallella)
        result = po.mergeEqualPrimitives(platformDescription, equalList)
        assert result == [
            (
                "EMEM",
                [
                    ("hostToHostCached", ["ARM0", "ARM1"]),
                    (
                        "network_on_chip",
                        [
                            (
                                "network_on_chip",
                                [
                                    "E00",
                                    "E01",
                                    "E02",
                                    "E03",
                                    "E04",
                                    "E05",
                                    "E06",
                                    "E07",
                                    "E08",
                                    "E09",
                                    "E10",
                                    "E11",
                                    "E12",
                                    "E13",
                                    "E14",
                                    "E15",
                                ],
                            )
                        ],
                    ),
                ],
            )
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_mergeEqualPrimitives_3(self, multiDSP):
        processors = multiDSP.processors()
        primitives = multiDSP.primitives()
        platformDescription = po.getPlatformDescription(processors, primitives)
        equalList = po.findEqualPrimitives(multiDSP)
        result = po.mergeEqualPrimitives(platformDescription, equalList)
        assert result == [
            (
                "comm_cp_shared_shared_memory",
                ["dsp0", "dsp1", "dsp2", "dsp3", "dsp4"],
            )
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_createNOCMatrix(self, parallella):
        processors = parallella.processors()
        primitives = parallella.primitives()
        platformDescription = po.getPlatformDescription(processors, primitives)
        equalList = po.findEqualPrimitives(parallella)
        platformDescription = po.mergeEqualPrimitives(
            platformDescription, equalList
        )
        result = po.createNocMatrix(platformDescription, parallella)
        assert result == [
            (
                "EMEM",
                [
                    ("hostToHostCached", ["ARM0", "ARM1"]),
                    (
                        "network_on_chip",
                        [
                            "E00",
                            "E01",
                            "E02",
                            "E03",
                            "E04",
                            "E05",
                            "E06",
                            "E07",
                            "E08",
                            "E09",
                            "E10",
                            "E11",
                            "E12",
                            "E13",
                            "E14",
                            "E15",
                        ],
                    ),
                ],
            )
        ]

    @pytest.mark.xfail(
        reason="Required files are not in the repository anymore"
    )
    def test_organizePEs(self, parallella):
        peList = [
            (
                "network_on_chip",
                [
                    "E00",
                    "E01",
                    "E02",
                    "E03",
                    "E04",
                    "E05",
                    "E06",
                    "E07",
                    "E08",
                    "E09",
                    "E10",
                    "E11",
                    "E12",
                    "E13",
                    "E14",
                    "E15",
                ],
            )
        ]
        adjacencyDict = parallella.to_adjacency_dict()
        result = po.organizePEs(peList, adjacencyDict)
        assert result == [
            "E00",
            "E01",
            "E02",
            "E03",
            "E04",
            "E05",
            "E06",
            "E07",
            "E08",
            "E09",
            "E10",
            "E11",
            "E12",
            "E13",
            "E14",
            "E15",
        ]
