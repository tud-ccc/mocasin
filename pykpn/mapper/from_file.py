# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit

import hydra

class FromFileMapper:

    def __init__(self, kpn, platform, cfg):
        self.mapper = hydra.utils.instantiate(cfg['source'], kpn, platform, cfg)

    def generate_mapping(self):
        return self.mapper.generate_mapping()
