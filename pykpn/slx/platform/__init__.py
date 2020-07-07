# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard


from .convert import convert
from .parse import parse
from pykpn.util import logging
from pykpn.common.platform import Platform


log = logging.getLogger(__name__)


class SlxPlatform(Platform):

    def __init__(self, name, platform_xml):
        super().__init__(name)
        log.info('start parsing the platform description')
        xml_platform = parse(platform_xml, True)
        convert(self, xml_platform)
        log.info('done parsing the platform description')
