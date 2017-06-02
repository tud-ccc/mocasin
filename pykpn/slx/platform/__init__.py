# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard

import logging

from .parse_2017_04 import parse as parse_2017_04
from .convert_2017_04 import convert as convert_2017_04

from ...common import Platform
from ...common import Processor


log = logging.getLogger(__name__)


class SlxPlatform(Platform):

    def __init__(self, xml_path, version='2017.04'):
        super().__init__()
        log.info('start parsing the platform description')
        if version == '2017.04':
            xml_platform = parse_2017_04(xml_path, True)
            convert_2017_04(self, xml_platform)
        else:
            raise RuntimeError('SLX version %s is not supported!' % version)
        log.info('done parsing the platform description')
