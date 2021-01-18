# Copyright (C) 2016 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andrés Goens

import functools
import time
from itertools import product
from mocasin.util.logging import getLogger

log = getLogger(__name__)

total_time = 0


def timeit(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        global total_time
        start_time = time.time()
        ret = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        total_time += elapsed_time
        return ret

    return newfunc


# important! permutations start with 0
class Permutation(list):
    def __init__(self, ls, n=-1, action=0, *args):
        assert type(ls) == list
        m = max([max(l) for l in ls])
        if n == -1:
            self.n = m + 1
        else:
            if not (n >= m):
                log.error(
                    "Trying to initialize "
                    + str(ls)
                    + "( max "
                    + str(m)
                    + ") with n = "
                    + str(n)
                )
                return None
            self.n = n
        if not (action == 0 or action == 1):
            log.error("Unrecognized action: " + str(action))
            return None
        self.action = action
        list.__init__(self, range(0, self.n), *args)
        for l in ls:
            if len(l) >= 2:
                first = l.pop(0)
                prev = first
                while l:
                    cur = l.pop(0)
                    self[prev] = cur
                    prev = cur
                self[prev] = first

    def act(self, obj):
        if self.action == 0:
            if not (isinstance(obj, list) or isinstance(obj, tuple)):
                log.debug(
                    str(obj)
                    + " not of list/tuple type ("
                    + str(type(obj))
                    + ")"
                )
                return None
            for elem in obj:
                if not (elem < self.n):
                    log.error(
                        "Permutation "
                        + str(self)
                        + ": trying to act on invalid point "
                        + str(elem)
                        + " in object: "
                        + str(obj)
                    )
                    return None
            return self.act_point(obj)
        elif self.action == 1:
            if not (len(obj) == self.n):
                log.error(
                    "Permutation "
                    + str(self)
                    + ": trying to act on invalid point "
                    + str(obj)
                )
                return None
            return self.act_tuple(obj)
        else:
            return None

    def act_point(self, l):
        if not (type(l) == list or type(l) == tuple):
            log.error((str(l) + " not of list/tuple type"))
            return None
        res = list()
        for i in l:
            res.append(self[i])
        return res

    def act_tuple(self, tup):
        assert type(tup) == list
        assert self.n == len(tup)
        newtup = list(tup)  # is this very inefficient?
        for i, elem in enumerate(tup):
            newtup[self[i]] = elem
        return newtup

    def get_cycles(self):
        ls = []
        moved = [x for x in self if self[x] != x]
        l = []
        while moved:
            x = moved.pop()
            l = [x]
            while self[x] not in l:
                x = self[x]
                moved.remove(x)
                l.append(x)
            ls.append(l)

        return ls


class PermutationGroup(list):
    def __init__(self, perms, n=-1, action=0, *args):
        assert type(perms) == list
        assert action == 0 or action == 1
        assert len(perms) > 0 or n > -1
        if len(perms) > 0:
            if not (type(perms[0]) == Permutation):
                log.error(
                    str(perms[0])
                    + " is not a permutation ("
                    + str(type(perms[0]))
                )
                return None
            n = perms[0].n
        for g in perms:
            assert type(g) == Permutation
            # assert(g.action == action)
            # assert(g.n == n)
        m = max([g.n for g in perms] + [-1])
        self.action = action
        if n == -1:
            self.n = m
        else:
            # assert(n >= m)
            self.n = n

        list.__init__(self, perms, *args)

    def generators(self):
        return [gen.get_cycles() for gen in self]

    def orbit(self, function, point):
        stack = [point]
        orbit = [point]
        while stack:
            p = stack.pop()
            for perm in self:
                im = function(perm, p)
                if im not in orbit:
                    stack.append(im)
                    orbit.append(im)

        return orbit

    def point_orbit(self, point):
        return frozenset(self.orbit((lambda perm, p: perm[p]), point))

    def tuple_orbit(self, tup):
        return frozenset(
            [tuple(e) for e in self.orbit((lambda perm, p: perm.act(p)), tup)]
        )

    def point_orbit_hash(self, point):
        return hash(self.point_orbit(point))

    def tuple_orbit_hash(self, tup):
        return hash(self.tuple_orbit(tup))

    def point_normalize(self, point):
        return min(self.point_orbit(point))

    def enumerate_orbits(self):
        orbs = []
        points = set(range(self.n))
        while points:
            p = points.pop()
            orb = self.point_orbit(p)
            points = points.difference(set(orb))
            orbs.append(orb)
        return orbs

    def enumerate_tuple_orbits(self, d=1):
        orbs = []
        points = set(product(range(self.n), repeat=d))
        while points:
            p = points.pop()
            orb = self.tuple_orbit(p)
            points = points.difference(set(orb))
            orbs.append(orb)
        return orbs

    @timeit
    def tuple_normalize(self, tup, verbose=False, quick=True):
        if verbose:
            log.debug(("normalizing: " + str(tup)))
        S_x0lt = []  # { g.act(tup) for g in self if g.act(tup) < tup}
        for g in self:
            im = g.act(tup)
            if im not in S_x0lt and im < tup:
                S_x0lt.append(im)
        if quick and S_x0lt != []:
            S_x0lt = [min(S_x0lt)]

        Snext_x0lt = S_x0lt
        Scur_x0lt = [tup]
        iterator = 2
        while Snext_x0lt:
            Scur_x0lt = Snext_x0lt
            Snext_x0lt = (
                []
            )  # [ g.act(t) for t in Scur_x0lt for g in self if g.act(t) < t ]
            for t in Scur_x0lt:
                for g in self:
                    im = g.act(t)
                    if im not in Snext_x0lt and im < t:
                        Snext_x0lt.append(im)
            if verbose and Snext_x0lt:
                log.debug(
                    "|(S^{"
                    + str(iterator)
                    + "}x_0)_<| = "
                    + str(len(Snext_x0lt))
                    + ", min: "
                    + str(min(Snext_x0lt))
                )
                iterator = iterator + 1
            if quick == True and Snext_x0lt:
                Snext_x0lt = [min(Snext_x0lt)]
        minimal = Scur_x0lt[0]
        if verbose:
            log.debug("finished normalizing: " + str(minimal))
            global total_time
            log.debug("total time elapsed normalizing: " + str(total_time))
        return minimal


class TrivialGroup(PermutationGroup):
    def __init__(self, n, action=0, *args):
        assert type(n) == int
        assert n > 0
        assert action == 0 or action == 1
        self.action = action
        PermutationGroup.__init__(self, [], n, action=action, *args)


class SymmetricGroupTranspositions(PermutationGroup):
    def __init__(self, n, action=0, *args):
        assert type(n) == int
        assert n > 0
        generators = []
        for i in range(0, n):
            for j in range(i + 1, n):
                generators.append(Permutation([[i, j]], n, action))
        PermutationGroup.__init__(self, generators, n, action=action, *args)


class DuplicateGroup(PermutationGroup):
    def __init__(self, g, times=2, trivials=[], *args):
        assert isinstance(g, PermutationGroup)
        # print("generators: " + str(g.generators()))
        action = g.action
        clist_old = [l.get_cycles() for l in g]
        generators_clist = []
        for l in clist_old:
            new_l = []
            start_bound = 0
            for _ in range(0, times):
                for t in sorted(trivials):
                    if start_bound == t:
                        start_bound += 1
                new_l += list(
                    map(
                        lambda cycles: list(
                            map(lambda x: x + start_bound, cycles)
                        ),
                        l,
                    )
                )
                # print("start bound: " + str(start_bound))
                start_bound += g.n
            generators_clist.append(new_l)

        generators = list(
            map(
                lambda cycles: Permutation(
                    cycles, times * g.n + len(trivials), action=action
                ),
                generators_clist,
            )
        )

        PermutationGroup.__init__(
            self, generators, 2 * g.n, action=action, *args
        )


class ProductGroup(PermutationGroup):
    def __init__(self, gs, *args):
        assert type(gs) == list
        assert len(gs) > 0
        action = gs[0].action
        for g in gs:
            assert isinstance(g, PermutationGroup)
            assert action == g.action
        current_n = 0
        generators = []
        sum_n = sum([g.n for g in gs])
        for g in gs:
            extra_n = g.n
            for gen in g:
                new_gen = []
                for cycle in gen.get_cycles():
                    new_gen.append(list(map(lambda x: x + current_n, cycle)))
                # print("gen: " + str(new_gen) + " (" + str(sum_n) +")")
                generators.append(
                    Permutation(new_gen, sum_n, action=gen.action)
                )
            current_n += extra_n

        PermutationGroup.__init__(
            self, generators, current_n, action=action, *args
        )


class PermutationGroupFromGens(PermutationGroup):
    def __init__(self, gs, *args):
        assert type(gs) == list
        assert len(gs) > 0
        for g in gs:
            assert isinstance(g, Permutation)
        point_g_ns = [g.n for g in gs if g.action == 0]
        if point_g_ns:
            n = max(point_g_ns)
        else:
            n = max([g.n for g in gs if g.action == 1])
        PermutationGroup.__init__(self, gs, n, *args)


class PartialPermutation(dict):
    def __init__(self, l, *args):
        assert type(l) == list
        dict.__init__(self, *args)

        # TODO: implement partial permutation data type in python


# Test code:
if __name__ == "__main__":
    separator = "------------------------------"
    l = Permutation([[0, 1, 2], [4, 5]])
    print("Cycles of Permutation([[0,1,2],[4,5]]): " + str(l.get_cycles()))
    print(separator)
    g = PermutationGroup([l])
    print("Point orbit of 5: " + str(g.point_orbit(5)))
    print("Orbits of generated group: " + str(g.enumerate_orbits()))
    print("Tuple orbit of [0,5]: " + str(g.tuple_orbit([0, 5])))
    print(separator)
    s4xs8 = ProductGroup(
        [SymmetricGroupTranspositions(8), SymmetricGroupTranspositions(4)]
    )
    s4xs8_double = DuplicateGroup(s4xs8)
    print("Generators of double s4xs8: " + str(s4xs8_double.generators()))
    print(separator)
    arch_group = ProductGroup([s4xs8_double, TrivialGroup(3)])
    print("arch group: " + str(arch_group))
    print(
        "Tuple orbit size of [1, 10, 1, 9, 7, 1, 1, 1, 22, 25, 24] under arch_group "
        + str(
            len(arch_group.tuple_orbit([1, 10, 1, 9, 7, 1, 1, 1, 22, 25, 24]))
        )
    )
    print(
        "Tuple [1, 10, 1, 9, 7, 1, 1, 1, 22, 25, 24] normalized under arch_group "
        + str(arch_group.tuple_normalize([1, 10, 1, 9, 7, 1, 1, 1, 22, 25, 24]))
    )
    print(
        "Tuple [0, 8, 0, 0, 0, 0, 0, 0, 0, 25, 25, 24, 25, 24, 25, 0, 0, 24, 0, 0] normalized under arch_group (already minimal): "
        + str(
            arch_group.tuple_normalize(
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
            )
        )
    )
    print(separator)
    app_group = DuplicateGroup(
        ProductGroup(
            [
                TrivialGroup(1, action=1),
                SymmetricGroupTranspositions(4, action=1),
            ]
        ),
        times=4,
    )
    print("app group: " + str(app_group))
    print(
        "Tuple [0, 8, 0, 0, 0, 0, 0, 0, 0, 25, 25, 24, 25, 24, 25, 0, 0, 24, 0, 0] normalized under app_group "
        + str(
            app_group.tuple_normalize(
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
            )
        )
    )

    full_group = PermutationGroupFromGens(list(app_group) + list(arch_group))
    print(
        "Tuple [2, ,2 , 8,  2, 2, 2, 2, 2, 2, 25, 25, 24, 25, 24, 25, 2, 2, 24, 2, 2] normalized under full_group "
        + str(
            full_group.tuple_normalize(
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
            )
        )
    )

    print(separator)
    mandelbrot_group = DuplicateGroup(
        SymmetricGroupTranspositions(16, action=1), times=3, trivials=[16, 17]
    )
    mandelbrot_full_group = PermutationGroupFromGens(
        list(arch_group) + list(mandelbrot_group)
    )
    # print(str(mandelbrot_full_group))
    print(
        "Tuple [6, 6, 1, 2, 7, 6, 9, 10, 6, 11, 9, 0, 1, 0, 4, 3, 5, 0, 18, 24, 25, 14, 24, 24, 25, 24, 24, 24, 25, 12, 13, 25, 25, 15, 25, 24, 25, 25, 24, 12, 25, 25, 25, 24, 12, 0, 24, 0, 24, 12] normalized under mandelbrot_full_group "
        + str(
            mandelbrot_full_group.tuple_normalize(
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
            )
        )
    )

    print(separator)
    # arch_group = PermutationGroup([ Permutation([range(0,12),range(12,24)],27), Permutation([[0,1],[12,13]],27)])
    # print("normalization of[1, 10, 1, 9, 7, 1, 1, 1, 1, 24, 24, 25, 13, 24, 24, 1, 1, 22, 25, 24]: " + arch_group.tuple_normalize([1, 10, 1, 9, 7, 1, 1, 1, 1, 24, 24, 25, 13, 24, 24, 1, 1, 22, 25, 24]))
    mjpeg_gens_func = lambda l: [(i, j) for i in l for j in l[l.index(i) :]]
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
                lambda trans: Permutation([list(trans)], action=1, n=27),
                (mjpeg_chans_gens + mjpeg_procs_gens),
            )
        )
    )
    mjpeg_full_group = PermutationGroupFromGens(
        list(arch_group) + list(mjpeg_group)
    )
    print(
        "Tuple [11, 6, 10, 7, 10, 10, 5, 8, 10, 8, 11, 2, 24, 24, 18, 24, 10, 22, 24, 22, 22, 24, 20, 10, 20, 24, 24] normalized under mjpeg_full_group "
        + str(
            mjpeg_full_group.tuple_normalize(
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
            )
        )
    )
    print(
        "Tuple [11, 6, 10, 7, 10, 10, 5, 8, 10, 8, 11, 2, 24, 24, 18, 24, 10, 22, 24, 22, 22, 24, 20, 10, 20, 24, 24] normalized under arch_group "
        + str(
            arch_group.tuple_normalize(
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
            )
        )
    )
    print(
        "Tuple [8, 0, 9, 1, 9, 9, 2, 10, 9, 10, 8, 3, 24, 24, 12, 24, 9, 21, 24, 21, 21, 24, 22, 9, 22, 24, 24]  normalized under mjpeg_group "
        + str(
            mjpeg_group.tuple_normalize(
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
            )
        )
    )

    print(separator)
    print(
        str(
            DuplicateGroup(
                SymmetricGroupTranspositions(2, action=1),
                times=7,
                trivials=[6, 7],
            )
        )
    )
    print("elapsed time normalizing " + str(total_time))

    # print("Hash of this tuple orbit: " + str(arch_group.tuple_orbit_hash([1, 10, 1, 9, 7, 1, 1, 1, 1, 24, 24, 25, 13, 24, 24, 1, 1, 22, 25, 24])))
    # TODO: fix Permutation([[3,4],[4,5]]) == [0, 1, 2, 4, 5, 4]
