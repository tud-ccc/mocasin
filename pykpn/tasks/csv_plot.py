# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

import hydra

from pykpn.util import plot
from pykpn.util.csv_reader import DataReader

def csv_plot(cfg):
    platform = hydra.utils.instantiate(cfg['platform'])
    kpn = hydra.utils.instantiate(cfg['kpn'])
    dataReader = DataReader(platform,
                            cfg['filePath'],
                            kpn,
                            cfg['property'],
                            cfg['prefix'],
                            cfg['suffix'])

    mappings = dataReader.formMappings()

    compareProperty = []
    mappingList = []

    for key in mappings:
        mappingList.append(mappings[key][0])
        compareProperty.append(float(mappings[key][1]))

    plot.visualize_mapping_space(mappingList, compareProperty)
