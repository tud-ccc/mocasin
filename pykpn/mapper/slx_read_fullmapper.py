# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

from pykpn.slx.mapping import SlxMapping

class slx_read_mapper:
    """
    Reads a SLX default mapping from a file. Mapping is returned by generate_mapping method to maintain the
    common mapper interface.
    """
    def __init__(self, kpn, platform, cfg):
        self.mapping = SlxMapping(kpn, platform, cfg['mapping_xml'], cfg['slx_version'])

    def generate_mapping(self):
        return self.mapping
