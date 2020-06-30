# This file defines extra usefull classes
#
# Author: Robert Khasanov

from collections.abc import Iterable

class NamedDimensionalNumber:
    """This class defines multi-dimensional number (similar to vector), all dimensions have unique names.
    
    The operations between instances of the class NamedDimensionalNumber are valid iff. they have the same dimensions.

    Args:
        v: an iterable object
        init_only_names (bool): if True, all dimenstions assigned to zero
    """
    def __init__(self, v, init_only_names = False):
        assert isinstance(v, Iterable)

        if isinstance(v, (type({}.items()), NamedDimensionalNumber) ):
            self.__dict = dict(v)
            if init_only_names:
                for k in self.__dict.keys():
                    self.__dict[k] = 0
        else:
            self.__dict = { k:0 for k in v}

    def __len__(self):
        return len(self.__dict)

    def __getitem__(self, key):
        assert key in self.__dict
        return self.__dict[key]

    def __setitem__(self, key, value):
        assert key in self.__dict
        self.__dict[key] = value

    def __str__(self):
        return str(self.__dict)

    def __iter__(self):
        yield from self.__dict.items()

    def __check_object_same_type(self, other):
        assert isinstance(other, NamedDimensionalNumber)
        if set(self.__dict.keys()) != set(other.__dict.keys()):
            print("Error: trying to use a binary operator on NamedDimensionalNumbers with different dimensions")
            print(self.__dict.keys())
            print(other.__dict.keys())
            return False
        return True

    def __eq__(self, other):
        assert self.__check_object_same_type(other)
        for k in self.__dict.keys():
            if self[k] != other[k]:
                return False
        return True

    def __le__(self, other):
        assert self.__check_object_same_type(other)
        for k in self.__dict.keys():
            if self[k] > other[k]:
                return False
        return True

    def __add__(self, other):
        assert self.__check_object_same_type(other)
        r = NamedDimensionalNumber(self, init_only_names = True)
        for k in self.__dict.keys():
            r[k] = self[k] + other[k]
        return r

    def __sub__(self, other):
        assert self.__check_object_same_type(other)
        r = NamedDimensionalNumber(self, init_only_names = True)
        for k in self.__dict.keys():
            r[k] = self[k] - other[k]
        return r

    def __mul__(self, other: float):
        if isinstance(other, (float, int)):
            single_value = True
        else:
            single_value = False
            assert isinstance(other, NamedDimensionalNumber)
            assert self.__check_object_same_type(other)

        r = NamedDimensionalNumber(self, init_only_names = True)
        for k in self.__dict.keys():
            if single_value:
                r[k] = self[k] * other
            else:
                r[k] = self[k] * other[k]
        return r

    def reduce(self, f, start_value = None):
        if start_value is None:
            assert len(self) > 0

        res = start_value
        for v in self.__dict.values():
            if res is None:
                res = v
            else:
                res = f(res, v)
        return res

    @classmethod
    def max_per_dim(cls, v1, v2):
        """Returns the new number with maximum value between v1 and v2 at each dimenstion."""
        assert isinstance(v1, NamedDimensionalNumber)
        if isinstance(v2, (float, int)):
            single_value = True
        else:
            single_value = False
            assert isinstance(v2, NamedDimensionalNumber)
            assert self.__check_object_same_type(other)

        r = cls(v1, init_only_names= True)
        for k in v1.__dict.keys():
            if single_value:
                r[k] = max(v1[k], v2)
            else:
                r[k] = max(v1[k], v2[k])
        return r



