# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from .convert_2017_04 import convert as convert_2017_04
from .parse_2017_04 import parse as parse_2017_04
from pykpn.common import logging
from pykpn.common.platform import Platform


log = logging.getLogger(__name__)


class SlxPlatform(Platform):

    def __init__(self, name, xml_path, version):
        super().__init__(name)
        log.info('start parsing the platform description')
        if (version == '2017.04' or version == '2017.10'):
            xml_platform = parse_2017_04(xml_path, True)
            convert_2017_04(self, xml_platform)
        else:
            raise RuntimeError('SLX version %s is not supported!' % version)
        log.info('done parsing the platform description')
