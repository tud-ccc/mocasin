# Copyright (C) 2017 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard

import logging

from hydra.utils import to_absolute_path

from .convert import convert
from .parse import parse
from mocasin.common.platform import Platform


log = logging.getLogger(__name__)


class MapsPlatform(Platform):
    def __init__(self, name, xml_file, **kwargs):
        super().__init__(
            name,
            symmetries_json=kwargs.get("symmetries_json", None),
            embedding_json=kwargs.get("embedding_json", None),
        )
        log.info("start parsing the platform description")
        xml_platform = parse(to_absolute_path(xml_file), True)
        convert(
            self,
            xml_platform,
            scheduler_cycles=kwargs.get("scheduler_cycles", None),
            fd_frequencies=kwargs.get("fd_frequencies", None),
            ppm_power=kwargs.get("ppm_power", None),
        )
        log.info("done parsing the platform description")
