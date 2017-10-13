# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from .convert_2017_04 import convert as convert_2017_04
from .convert_2017_10 import convert as convert_2017_10
from .parse_2017_04 import parse as parse_2017_04
from .parse_2017_10 import parse as parse_2017_10
from pykpn.common import logging
from pykpn.common.mapping import Mapping


log = logging.getLogger(__name__)


class SlxMapping(Mapping):

    def __init__(self, kpn, platform, mapping_file, version='2017.10'):
        super().__init__(kpn, platform)
        log.info('Start parsing the SLX mapping ' + mapping_file)
        if (version == '2017.04'):
            xml_mapping = parse_2017_04(mapping_file, True)
            convert_2017_04(self, xml_mapping)
        elif (version == '2017.10'):
            xml_mapping = parse_2017_10(mapping_file, True)
            convert_2017_10(self, xml_mapping)
        else:
            raise RuntimeError('SLX version %s is not supported!' % version)
        log.info('Done parsing the SLX mapping')
