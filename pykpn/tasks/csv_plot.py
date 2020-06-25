# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

import hydra

from pykpn.util import plot
from pykpn.util.csv_reader import DataReader


@hydra.main(config_path='conf/csv_plot.yaml')
def csv_plot(cfg):
    platform = hydra.utils.instantiate(cfg['platform'])
    kpn = hydra.utils.instantiate(cfg['kpn'])
    data_reader = DataReader(platform,
                             cfg['csv_file'],
                             kpn,
                             cfg['property'],
                             cfg['prefix'],
                             cfg['suffix'])

    mappings = data_reader.formMappings()

    compare_property = []
    mapping_list = []

    for key in mappings:
        mapping_list.append(mappings[key][0])
        compare_property.append(float(mappings[key][1]))

    plot.visualize_mapping_space(mapping_list, compare_property)
