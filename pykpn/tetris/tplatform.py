# This file describes the class Platform
#
# Author: Robert Khasanov
from pykpn.common.platform import Platform as KpnPlatform
from pykpn.tetris.extra import NamedDimensionalNumber

class Platform:
    """This class wraps the class pykpn.slx.platform.Platform class.

    Args:
        name (str): Platform name
        platform (pykpn.common.Platform): A platform to be wrapped
    """
    def __init__(self, name: str, platform: KpnPlatform):
        self.name = name
        self.__platform = platform
        self.__core_types = {}
        for p in platform.processors():
            if p.type not in self.__core_types:
                self.__core_types[p.type] = 1
            else:
                self.__core_types[p.type] += 1
        pass

    def core_types(self, only_types = False):
        """Count PEs in the platform and classify on their types.

        Args:
            only_types (bool): A returned object contains only types of PEs without their number

        Returns:
            A NamedDimensionalNumber object with core types as dimensions.
            If only_types is False, each dimension contains a number of PE of corresponding type, otherwise the number is 0.
        """
        return NamedDimensionalNumber(self.__core_types.items(), init_only_names = only_types)

    def find_processor(self, name):
        """Find processor by its name.

        Args:
            name (str): Name of the processor

        Returns:
            Processor
        """
        return self.__platform.find_processor(name)

    def kpn_platform(self):
        return self.__platform

