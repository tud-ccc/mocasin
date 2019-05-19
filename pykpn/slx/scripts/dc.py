#!/usr/bin/env python3

# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Gerald Hempel, Andres Goens

import argparse
import timeit

import re
import sys
import os
import json
import logging
import argparse

from pykpn.design_centering.design_centering import dc_settings as conf
import random
random.seed(conf.random_seed)

from ..config import SlxSimulationConfig
from ..kpn import SlxKpnGraph
from ..mapping import export_slx_mapping
from ..platform import SlxPlatform
from ..trace import SlxTraceReader

from pykpn.design_centering.design_centering import dc_oracle
from pykpn.design_centering.design_centering import dc_sample
from pykpn.design_centering.design_centering import dc_volume
from pykpn.design_centering.design_centering import designCentering
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
    
    parser.add_argument(
        '-R',
        '--representation',
        type=str,
        help='Select the representation type for the mapping space.\nAvailable:'
        + ", ".join(dir(reps.RepresentationType)),
        dest='rep_type_str',
        default='GeomDummy')
    
    args = parser.parse_args()
    logging.setup_from_args(args)

    argv = sys.argv
    
    log.info("==== Run Design Centering ====")
    #logging.basicConfig(filename="dc.log", filemode = 'w', level=logging.DEBUG)
    
    log.info(f" Initialized random number generator. Seed: {conf.random_seed}")
    
    tp = designCentering.ThingPlotter()

    if (len(argv) > 1):
        # read cmd-line and settings
        #try:
        #    center = [1,2,3,4,5,6,7,8]
        #    #json.loads(argv[1])
        #except ValueError:
        #    log.warning(" {:s} is not a vector \n".format(argv[1]))
        #    sys.stderr.write("JSON decoding failed (in function main) \n")


        config = SlxSimulationConfig(args.configFile)
        slx_version = config.slx_version
        if config.platform_class is not None:
            platform = config.platform_class()
            platform_name = platform.name
        else:
            platform_name = os.path.splitext(
                os.path.basename(config.platform_xml))[0]
            platform = SlxPlatform(platform_name, config.platform_xml, slx_version)

        # create all graphs
        kpns = {}
        if len(config.applications) > 1:
            log.warn("DC Flow just supports one appilcation. The rest will be ignored")
        app_config = config.applications[0]
        app_name = app_config.name
        kpn = SlxKpnGraph(app_name, app_config.cpn_xml, slx_version) 
        rep_type_str = args.rep_type_str
        if rep_type_str == "GeomDummy":
            representation = "GeomDummy"
        elif rep_type_str not in dir(reps.RepresentationType):
            log.exception("Representation " + rep_type_str + " not recognized. Available: " + ", ".join(dir(reps.RepresentationType)))
            raise RuntimeError('Unrecognized representation.')
        else:
            representation_type = reps.RepresentationType[rep_type_str]
            log.info(f"initializing representation ({rep_type_str})")
            representation = representation_type.getClassType()(kpn,platform)

        # run DC algorithm
        # starting volume (init): 
        if representation == "GeomDummy":
            center = [1,2,3,4,5,6,7,8]
        else:
            center = representation.uniform()
        if (conf.shape == "cube"):
            v = dc_volume.Cube(center, len(center))
        
        config = args.configFile
        oracle = dc_oracle.Oracle(args.configFile) #the oracle could get the kpn and platform (now, pykpn objects, SLX independent) passed as files (see Issue #3)
        dc = designCentering.DesignCentering(v, conf.distr, oracle,representation)
        center = dc.ds_explore()

        # plot explored design space (in 2D)
        #if True:
        #    tp.plot_samples(dc.samples)
        log.info("center: {} radius: {:f}".format(dc.vol.center, dc.vol.radius))
        log.info("==== Design Centering done ====")

        json_dc_dump = {}
        json_dc_dump['center'] = {}
        json_dc_dump['center']['mapping'] = center.getMapping(0).to_list()
        json_dc_dump['center']['feasible'] = center.getFeasibility()
        json_dc_dump['center']['runtime'] = center.getSimContext().exec_time / 1000000000.0

        # run perturbation test
        if conf.run_perturbation:
            log.info("==== Run Perturbation Test ====")
            num_pert = conf.num_perturbations
            num_mappings = conf.num_mappings
            pm = p.PerturbationManager( config, num_mappings, num_pert)
            map_set = pm.create_randomMappings()

            pert_res = []
            s,c = pm.run_perturbation(center.getMapping(0), pm.apply_singlePerturbation)
            pert_res.append(s)

            json_dc_dump['center']['pert'] = c
            json_dc_dump['center']['passed'] = s

            for i,m in enumerate(map_set):
                s,c = pm.run_perturbation(m, pm.apply_singlePerturbation)
                pert_res.append(s)
                json_dc_dump['rand mapping' + str(i)] = {}
                json_dc_dump['rand mapping' + str(i)]['mapping'] = m.to_list()
                json_dc_dump['rand mapping' + str(i)]['pert'] = c
                json_dc_dump['rand mapping' + str(i)]['passed'] = s

            tp.plot_perturbations(pert_res)
            log.info("==== Perturbation Test done ====")

        with open('dump.json', 'w') as dump:
            json.dump(json_dc_dump, dump, indent=4)

    else:
        log.info("usage: python designCentering [x1,x2,...,xn]\n")

    return 0

if __name__ == "__main__":
    main()

# calls
#/slx_random_walk -V ~/misc_code/kpn-apps/audio_filter/parallella/config.ini /tmp -n5000
#./bin/dc_run ~/misc_code/kpn-apps-2/audio_filter/parallella/config.ini -w pykpn.design_centering
