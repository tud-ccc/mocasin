# Copyright (C) 2019 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andres Goens

import hydra
import os

from pykpn.util import plot
from pykpn.util.csv_reader import DataReader

@hydra.main(config_path='conf/csv_plot.yaml')
def csv_plot(cfg):
    platform = hydra.utils.instantiate(cfg['platform'])
    kpn = hydra.utils.instantiate(cfg['kpn'])
    out_file = cfg['output_file']
    only_log = bool(cfg['log_to_file'])
    data_reader = DataReader(platform, kpn, cfg)

    mappings = data_reader.formMappings()

    compare_property = []
    mapping_list = []

    for key in mappings:
        mapping_list.append(mappings[key][0])
        compare_property.append(float(mappings[key][1]))

    if not only_log and not os.environ.get('DISPLAY', '') == '':
        plot.visualize_mapping_space(mapping_list, compare_property)

    else:
        if not len(mapping_list) == len(compare_property) and not out_file == 'None':
            raise RuntimeError("List of mappings and properties have different length")
        file = open(out_file, 'a')
        for i in range(0, len(mapping_list)):
            file.write(str(mapping_list[i].to_list()) + " : " + str(compare_property[i]) + "\n")

        file.close()

    plot.visualize_mapping_space(mapping_list, compare_property,cfg)
