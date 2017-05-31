# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

from .xml.platform_2017_04 import parse as parse_2017_04

from ..common import Platform


class SlxPlatform(Platform):

    def __init__(self, xml_path, version='2017.04'):
        super().__init__()
        if version == '2017.04':
            self.init_from_2017_04(xml_path)
        else:
            raise RuntimeError('SLX version %s is not supported!' % version)

    def init_from_2017_04(self, xml_path):
        xml_platform = parse_2017_04(xml_path, True)

        # TODO implement me
