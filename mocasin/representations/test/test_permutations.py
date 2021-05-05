# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens, Felix Teweleit

from mocasin.representations.permutations import (
    Permutation,
    PermutationGroup,
    ProductGroup,
    SymmetricGroupTranspositions,
    DuplicateGroup,
    TrivialGroup,
    PermutationGroupFromGens,
)


class TestPermutation(object):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_cycles(self):
        permutation = Permutation([[0, 1, 2], [4, 5]])
        assert permutation.get_cycles() == [[4, 5], [0, 1, 2]]

    def test_point_orbit(self):
        permutation = Permutation([[0, 1, 2], [4, 5]])
        permutation_group = PermutationGroup([permutation])
        assert frozenset(permutation_group.point_orbit(5)) == frozenset({4, 5})

    def test_enumerate_orbits(self):
        permutation = Permutation([[0, 1, 2], [4, 5]])
        permutation_group = PermutationGroup([permutation])
        assert permutation_group.enumerate_orbits() == [
            frozenset({0, 1, 2}),
            frozenset({3}),
            frozenset({4, 5}),
        ]

    def test_tuple_orbit(self):
        permutation = Permutation([[0, 1, 2], [4, 5]])
        permutation_group = PermutationGroup([permutation])
        expected = {(1, 4), (1, 5), (0, 5), (0, 4), (2, 5), (2, 4)}
        for perm in permutation_group.tuple_orbit([0, 5]):
            assert perm in expected
            expected.remove(perm)
        assert len(expected) == 0

    def test_generators(self):
        s4xs8 = ProductGroup(
            [SymmetricGroupTranspositions(8), SymmetricGroupTranspositions(4)]
        )
        s4xs8_double = DuplicateGroup(s4xs8)
        assert s4xs8_double.generators() == [
            [[12, 13], [0, 1]],
            [[12, 14], [0, 2]],
            [[12, 15], [0, 3]],
            [[12, 16], [0, 4]],
            [[12, 17], [0, 5]],
            [[12, 18], [0, 6]],
            [[12, 19], [0, 7]],
            [[13, 14], [1, 2]],
            [[13, 15], [1, 3]],
            [[13, 16], [1, 4]],
            [[13, 17], [1, 5]],
            [[13, 18], [1, 6]],
            [[13, 19], [1, 7]],
            [[14, 15], [2, 3]],
            [[14, 16], [2, 4]],
            [[14, 17], [2, 5]],
            [[14, 18], [2, 6]],
            [[14, 19], [2, 7]],
            [[15, 16], [3, 4]],
            [[15, 17], [3, 5]],
            [[15, 18], [3, 6]],
            [[15, 19], [3, 7]],
            [[16, 17], [4, 5]],
            [[16, 18], [4, 6]],
            [[16, 19], [4, 7]],
            [[17, 18], [5, 6]],
            [[17, 19], [5, 7]],
            [[18, 19], [6, 7]],
            [[20, 21], [8, 9]],
            [[20, 22], [8, 10]],
            [[20, 23], [8, 11]],
            [[21, 22], [9, 10]],
            [[21, 23], [9, 11]],
            [[22, 23], [10, 11]],
        ]

    def test_ProductGroup(self):
        s4xs8 = ProductGroup(
            [SymmetricGroupTranspositions(8), SymmetricGroupTranspositions(4)]
        )
        s4xs8_double = DuplicateGroup(s4xs8)
        arch_group = ProductGroup([s4xs8_double, TrivialGroup(3)])
        # fmt: off
        assert(arch_group == [
            [1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [2, 1, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 13, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [3, 1, 2, 0, 4, 5, 6, 7, 8, 9, 10, 11, 15, 13, 14, 12, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [4, 1, 2, 3, 0, 5, 6, 7, 8, 9, 10, 11, 16, 13, 14, 15, 12, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [5, 1, 2, 3, 4, 0, 6, 7, 8, 9, 10, 11, 17, 13, 14, 15, 16, 12, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [6, 1, 2, 3, 4, 5, 0, 7, 8, 9, 10, 11, 18, 13, 14, 15, 16, 17, 12, 19, 20, 21, 22, 23, 24, 25, 26],
            [7, 1, 2, 3, 4, 5, 6, 0, 8, 9, 10, 11, 19, 13, 14, 15, 16, 17, 18, 12, 20, 21, 22, 23, 24, 25, 26],
            [0, 2, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 3, 2, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 14, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 4, 2, 3, 1, 5, 6, 7, 8, 9, 10, 11, 12, 16, 14, 15, 13, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 5, 2, 3, 4, 1, 6, 7, 8, 9, 10, 11, 12, 17, 14, 15, 16, 13, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 6, 2, 3, 4, 5, 1, 7, 8, 9, 10, 11, 12, 18, 14, 15, 16, 17, 13, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 7, 2, 3, 4, 5, 6, 1, 8, 9, 10, 11, 12, 19, 14, 15, 16, 17, 18, 13, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 3, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 4, 3, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 15, 14, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 5, 3, 4, 2, 6, 7, 8, 9, 10, 11, 12, 13, 17, 15, 16, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 6, 3, 4, 5, 2, 7, 8, 9, 10, 11, 12, 13, 18, 15, 16, 17, 14, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 7, 3, 4, 5, 6, 2, 8, 9, 10, 11, 12, 13, 19, 15, 16, 17, 18, 14, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 2, 4, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 2, 5, 4, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 16, 15, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 2, 6, 4, 5, 3, 7, 8, 9, 10, 11, 12, 13, 14, 18, 16, 17, 15, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 2, 7, 4, 5, 6, 3, 8, 9, 10, 11, 12, 13, 14, 19, 16, 17, 18, 15, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 2, 3, 5, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 2, 3, 6, 5, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 17, 16, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 2, 3, 7, 5, 6, 4, 8, 9, 10, 11, 12, 13, 14, 15, 19, 17, 18, 16, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 2, 3, 4, 6, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 17, 19, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 2, 3, 4, 7, 6, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 18, 17, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 2, 3, 4, 5, 7, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 18, 20, 21, 22, 23, 24, 25, 26],
            [0, 1, 2, 3, 4, 5, 6, 7, 9, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 20, 22, 23, 24, 25, 26],
            [0, 1, 2, 3, 4, 5, 6, 7, 10, 9, 8, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 21, 20, 23, 24, 25, 26],
            [0, 1, 2, 3, 4, 5, 6, 7, 11, 9, 10, 8, 12, 13, 14, 15, 16, 17, 18, 19, 23, 21, 22, 20, 24, 25, 26],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 21, 23, 24, 25, 26],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 10, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 22, 21, 24, 25, 26],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 22, 24, 25, 26]])
        # fmt: on

    def test_tuple_orbit_2(self):
        s4xs8 = ProductGroup(
            [SymmetricGroupTranspositions(8), SymmetricGroupTranspositions(4)]
        )
        s4xs8_double = DuplicateGroup(s4xs8)
        arch_group = ProductGroup([s4xs8_double, TrivialGroup(3)])

        assert (
            len(
                list(
                    arch_group.tuple_orbit(
                        [1, 10, 1, 9, 7, 1, 1, 1, 22, 25, 24]
                    )
                )
            )
            == 672
        )

    def test_tuple_normalize(self):
        s4xs8 = ProductGroup(
            [SymmetricGroupTranspositions(8), SymmetricGroupTranspositions(4)]
        )
        s4xs8_double = DuplicateGroup(s4xs8)
        arch_group = ProductGroup([s4xs8_double, TrivialGroup(3)])

        assert arch_group.tuple_normalize(
            [1, 10, 1, 9, 7, 1, 1, 1, 22, 25, 24]
        ) == [0, 8, 0, 9, 1, 0, 0, 0, 20, 25, 24]

    def test_tuple_normalize_2(self):
        s4xs8 = ProductGroup(
            [SymmetricGroupTranspositions(8), SymmetricGroupTranspositions(4)]
        )
        s4xs8_double = DuplicateGroup(s4xs8)
        arch_group = ProductGroup([s4xs8_double, TrivialGroup(3)])

        assert arch_group.tuple_normalize(
            [
                0,
                8,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                25,
                25,
                24,
                25,
                24,
                25,
                0,
                0,
                24,
                0,
                0,
            ],
            verbose=True,
        ) == [
            0,
            8,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            25,
            25,
            24,
            25,
            24,
            25,
            0,
            0,
            24,
            0,
            0,
        ]

    def test_duplicate_group(self):
        app_group = DuplicateGroup(
            ProductGroup(
                [
                    TrivialGroup(1, action=1),
                    SymmetricGroupTranspositions(4, action=1),
                ]
            ),
            times=4,
        )

        # fmt: off
        assert(app_group == [
            [0, 2, 1, 3, 4, 5, 7, 6, 8, 9, 10, 12, 11, 13, 14, 15, 17, 16, 18, 19],
            [0, 3, 2, 1, 4, 5, 8, 7, 6, 9, 10, 13, 12, 11, 14, 15, 18, 17, 16, 19],
            [0, 4, 2, 3, 1, 5, 9, 7, 8, 6, 10, 14, 12, 13, 11, 15, 19, 17, 18, 16],
            [0, 1, 3, 2, 4, 5, 6, 8, 7, 9, 10, 11, 13, 12, 14, 15, 16, 18, 17, 19],
            [0, 1, 4, 3, 2, 5, 6, 9, 8, 7, 10, 11, 14, 13, 12, 15, 16, 19, 18, 17],
            [0, 1, 2, 4, 3, 5, 6, 7, 9, 8, 10, 11, 12, 14, 13, 15, 16, 17, 19, 18]
        ])
        # fmt: on

        def test_tuple_normalize_3(self):
            app_group = DuplicateGroup(
                ProductGroup(
                    [
                        TrivialGroup(1, action=1),
                        SymmetricGroupTranspositions(4, action=1),
                    ]
                ),
                times=4,
            )
            assert app_group.tuple_normalize(
                [
                    0,
                    8,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    25,
                    25,
                    24,
                    25,
                    24,
                    25,
                    0,
                    0,
                    24,
                    0,
                    0,
                ]
            ) == [
                0,
                0,
                0,
                0,
                8,
                0,
                0,
                0,
                25,
                0,
                25,
                24,
                25,
                25,
                24,
                0,
                0,
                24,
                0,
                0,
            ]

        def test_tuple_normalize_4(self):
            s4xs8 = ProductGroup(
                [
                    SymmetricGroupTranspositions(8),
                    SymmetricGroupTranspositions(4),
                ]
            )
            s4xs8_double = DuplicateGroup(s4xs8)
            arch_group = ProductGroup([s4xs8_double, TrivialGroup(3)])
            app_group = DuplicateGroup(
                ProductGroup(
                    [
                        TrivialGroup(1, action=1),
                        SymmetricGroupTranspositions(4, action=1),
                    ]
                ),
                times=4,
            )
            full_group = PermutationGroupFromGens(
                list(app_group) + list(arch_group)
            )
            assert full_group.tuple_normalize(
                [
                    2,
                    2,
                    8,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    25,
                    25,
                    24,
                    25,
                    24,
                    25,
                    2,
                    2,
                    24,
                    2,
                    2,
                ]
            ) == [
                0,
                0,
                0,
                0,
                8,
                0,
                0,
                0,
                25,
                0,
                25,
                24,
                24,
                25,
                25,
                0,
                0,
                0,
                0,
                24,
            ]

        def test_tuple_normalize_5(self):
            s4xs8 = ProductGroup(
                [
                    SymmetricGroupTranspositions(8),
                    SymmetricGroupTranspositions(4),
                ]
            )
            s4xs8_double = DuplicateGroup(s4xs8)
            arch_group = ProductGroup([s4xs8_double, TrivialGroup(3)])
            mandelbrot_group = DuplicateGroup(
                SymmetricGroupTranspositions(16, action=1),
                times=3,
                trivials=[16, 17],
            )
            mandelbrot_full_group = PermutationGroupFromGens(
                list(arch_group) + list(mandelbrot_group)
            )

            assert mandelbrot_full_group.tuple_normalize(
                [
                    6,
                    6,
                    1,
                    2,
                    7,
                    6,
                    9,
                    10,
                    6,
                    11,
                    9,
                    0,
                    1,
                    0,
                    4,
                    3,
                    5,
                    0,
                    18,
                    24,
                    25,
                    14,
                    24,
                    24,
                    25,
                    24,
                    24,
                    24,
                    25,
                    12,
                    13,
                    25,
                    25,
                    15,
                    25,
                    24,
                    25,
                    25,
                    24,
                    12,
                    25,
                    25,
                    25,
                    24,
                    12,
                    0,
                    24,
                    0,
                    24,
                    12,
                ]
            ) == [
                0,
                0,
                0,
                0,
                1,
                1,
                2,
                3,
                4,
                5,
                5,
                6,
                8,
                8,
                9,
                10,
                7,
                5,
                12,
                24,
                24,
                24,
                13,
                25,
                14,
                15,
                25,
                17,
                25,
                24,
                25,
                25,
                24,
                24,
                25,
                17,
                24,
                25,
                24,
                25,
                25,
                17,
                24,
                5,
                5,
                24,
                17,
                25,
                24,
                25,
            ]

        def test_tuple_normalize_6(self):
            s4xs8 = ProductGroup(
                [
                    SymmetricGroupTranspositions(8),
                    SymmetricGroupTranspositions(4),
                ]
            )
            s4xs8_double = DuplicateGroup(s4xs8)
            arch_group = ProductGroup([s4xs8_double, TrivialGroup(3)])
            mjpeg_gens_func = lambda l: [
                (i, j) for i in l for j in l[l.index(i) :]
            ]
            mjpeg_procs_gens = mjpeg_gens_func([6, 8, 10, 1]) + mjpeg_gens_func(
                [5, 7, 9, 11]
            )
            mjpeg_chans_gens = (
                mjpeg_gens_func([16, 17, 18, 19])
                + mjpeg_gens_func([20, 22, 24, 26])
                + mjpeg_gens_func([21, 23, 25, 14])
            )
            mjpeg_group = PermutationGroupFromGens(
                list(
                    map(
                        lambda trans: Permutation(
                            [list(trans)], action=1, n=27
                        ),
                        (mjpeg_chans_gens + mjpeg_procs_gens),
                    )
                )
            )
            mjpeg_full_group = PermutationGroupFromGens(
                list(arch_group) + list(mjpeg_group)
            )

            assert mjpeg_full_group.tuple_normalize(
                [
                    11,
                    6,
                    10,
                    7,
                    10,
                    10,
                    5,
                    8,
                    10,
                    8,
                    11,
                    2,
                    24,
                    24,
                    18,
                    24,
                    10,
                    22,
                    24,
                    22,
                    22,
                    24,
                    20,
                    10,
                    20,
                    24,
                    24,
                ],
                verbose=True,
            ) == [
                8,
                0,
                9,
                1,
                9,
                2,
                3,
                9,
                8,
                10,
                9,
                10,
                24,
                24,
                9,
                24,
                9,
                21,
                21,
                24,
                21,
                12,
                22,
                24,
                22,
                24,
                24,
            ]

        def test_tuple_normalize_7(self):
            s4xs8 = ProductGroup(
                [
                    SymmetricGroupTranspositions(8),
                    SymmetricGroupTranspositions(4),
                ]
            )
            s4xs8_double = DuplicateGroup(s4xs8)
            arch_group = ProductGroup([s4xs8_double, TrivialGroup(3)])

            assert arch_group.tuple_normalize(
                [
                    11,
                    6,
                    10,
                    7,
                    10,
                    10,
                    5,
                    8,
                    10,
                    8,
                    11,
                    2,
                    24,
                    24,
                    18,
                    24,
                    10,
                    22,
                    24,
                    22,
                    22,
                    24,
                    20,
                    10,
                    20,
                    24,
                    24,
                ],
                verbose=True,
            ) == [
                8,
                0,
                9,
                1,
                9,
                9,
                2,
                10,
                9,
                10,
                8,
                3,
                24,
                24,
                12,
                24,
                9,
                21,
                24,
                21,
                21,
                24,
                22,
                9,
                22,
                24,
                24,
            ]

        def test_tuple_normalize_8(self):
            mjpeg_gens_func = lambda l: [
                (i, j) for i in l for j in l[l.index(i) :]
            ]
            mjpeg_procs_gens = mjpeg_gens_func([6, 8, 10, 1]) + mjpeg_gens_func(
                [5, 7, 9, 11]
            )
            mjpeg_chans_gens = (
                mjpeg_gens_func([16, 17, 18, 19])
                + mjpeg_gens_func([20, 22, 24, 26])
                + mjpeg_gens_func([21, 23, 25, 14])
            )
            mjpeg_group = PermutationGroupFromGens(
                list(
                    map(
                        lambda trans: Permutation(
                            [list(trans)], action=1, n=27
                        ),
                        (mjpeg_chans_gens + mjpeg_procs_gens),
                    )
                )
            )
            assert mjpeg_group.tuple_normalize(
                [
                    8,
                    0,
                    9,
                    1,
                    9,
                    9,
                    2,
                    10,
                    9,
                    10,
                    8,
                    3,
                    24,
                    24,
                    12,
                    24,
                    9,
                    21,
                    24,
                    21,
                    21,
                    24,
                    22,
                    9,
                    22,
                    24,
                    24,
                ],
                verbose=True,
            ) == [
                8,
                0,
                9,
                1,
                9,
                3,
                2,
                9,
                8,
                10,
                9,
                10,
                24,
                24,
                9,
                24,
                9,
                21,
                21,
                24,
                21,
                12,
                22,
                24,
                22,
                24,
                24,
            ]

            assert mjpeg_group.tuple_normalize(
                [
                    8,
                    0,
                    9,
                    1,
                    9,
                    9,
                    2,
                    10,
                    9,
                    10,
                    8,
                    3,
                    24,
                    24,
                    12,
                    24,
                    9,
                    21,
                    24,
                    21,
                    21,
                    24,
                    22,
                    9,
                    22,
                    24,
                    24,
                ],
                verbose=True,
            ) == [
                8,
                0,
                9,
                1,
                9,
                3,
                2,
                9,
                8,
                10,
                9,
                10,
                24,
                24,
                9,
                24,
                9,
                21,
                21,
                24,
                21,
                12,
                22,
                24,
                22,
                24,
                24,
            ]

        def test_DuplicateGroup(self):
            assert (
                DuplicateGroup(
                    SymmetricGroupTranspositions(2, action=1),
                    times=7,
                    trivials=[6, 7],
                )
                == [[1, 0, 3, 2, 5, 4, 6, 7, 9, 8, 11, 10, 13, 12, 15, 14]]
            )
