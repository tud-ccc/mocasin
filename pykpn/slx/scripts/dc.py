#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Gerald Hempel

import argparse
import timeit

import re
import sys
import json
import logging
import argparse

from pykpn.design_centering.design_centering import dc_oracle
from pykpn.design_centering.design_centering import dc_sample
from pykpn.design_centering.design_centering import dc_volume
from pykpn.design_centering.design_centering import designCentering
from pykpn.design_centering.design_centering import dc_settings as conf
from pykpn.design_centering.design_centering import perturbationManager as p
from pykpn.common import logging
from pykpn.util import plot # t-SNE plotting stuff
import numpy as np
import matplotlib.pyplot as plt
from pykpn.representations import representations as reps

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()

    logging.add_cli_args(parser)

    parser.add_argument('configFile', nargs=1,
                        help="input configuration file", type=str)
    
    args = parser.parse_args()
    logging.setup_from_args(args)

    argv = sys.argv
    
    log.info("==== Run Design Centering ====")
    #logging.basicConfig(filename="dc.log", filemode = 'w', level=logging.DEBUG)
    
    
    tp = designCentering.ThingPlotter()

    if (len(argv) > 1):
        # read cmd-line and settings
        try:
            center = [1,2,3,4,5,6,7,8]
            #json.loads(argv[1])
        except ValueError:
            log.warning(" {:s} is not a vector \n".format(argv[1]))
            sys.stderr.write("JSON decoding failed (in function main) \n")

        if (conf.shape == "cube"):
            v = dc_volume.Cube(center, len(center))

        # run DC algorithm
        config = args.configFile
        oracle = dc_oracle.Oracle(args.configFile)
        dc = designCentering.DesignCentering(v, conf.distr, oracle)
        center = dc.ds_explore()

        # plot explored design space (in 2D)
        #if True:
        #    tp.plot_samples(dc.samples)
        log.info("center: {} radius: {:f}".format(dc.vol.center, dc.vol.radius))
        log.info("==== Design Centering done ====")

        # run perturbation test
        if conf.run_perturbation:
            log.info("==== Run Perturbation Test ====")
            num_pert = conf.num_perturbations
            num_mappings = conf.num_mappings
            pm = p.PerturbationManager( config, num_mappings, num_pert)
            map_set = pm.create_randomMappings()

            pert_res = []
            pert_res.append(pm.run_perturbation(center.getMapping(0), pm.apply_singlePerturbation))

            for m in map_set:
                pert_res.append(pm.run_perturbation(m, pm.apply_singlePerturbation))

            tp.plot_perturbations(pert_res)
            log.info("==== Perturbation Test done ====")

    else:
        log.info("usage: python designCentering [x1,x2,...,xn]\n")

    return 0

if __name__ == "__main__":
    main()

# calls
#/slx_random_walk -V ~/misc_code/kpn-apps/audio_filter/parallella/config.ini /tmp -n5000
#./bin/dc_run ~/misc_code/kpn-apps-2/audio_filter/parallella/config.ini -w pykpn.design_centering
