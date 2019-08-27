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
import random

#SLX specific imports
from pykpn.slx.global_config import GlobalConfig
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.slx.mapping import export_slx_mapping
from pykpn.slx.platform import SlxPlatform
from pykpn.slx.trace import SlxTraceReader

#Design Centering
from pykpn.design_centering.design_centering import dc_oracle
from pykpn.design_centering.design_centering import dc_sample
from pykpn.design_centering.design_centering import dc_volume
from pykpn.design_centering.design_centering import designCentering
from pykpn.design_centering.design_centering import perturbationManager as p
from pykpn.util import logging
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

    #parser.add_argument(
    #    '-R',
    #    '--representation',
    #    type=str,
    #    help='Select the representation type for the mapping space.\nAvailable:'
    #         + ", ".join(dir(reps.RepresentationType)),
    #    dest='rep_type_str',
    #    default='GeomDummy')

    args = parser.parse_args()
    logging.setup_from_args(args)

    gconf = GlobalConfig(args.configFile)

    log.info("==== Found system combinations ====")
    for cn in gconf.system.keys():
        log.info(cn)

    argv = sys.argv
    
    #print(gconf.keys)
    #exit(1)

    log.info("==== Run Design Centering ====")
    #logging.basicConfig(filename="dc.log", filemode = 'w', level=logging.DEBUG)


    tp = designCentering.ThingPlotter()

    if (len(argv) > 1):
        # read cmd-line and settings
        #try:
        #    center = [1,2,3,4,5,6,7,8]
        #    #json.loads(argv[1])
        #except ValueError:
        #    log.warning(" {:s} is not a vector \n".format(argv[1]))
        #    sys.stderr.write("JSON decoding failed (in function main) \n")


        # config = SlxSimulationConfig(args.configFile)

        # use multiprocessing?
        for app_pl in gconf.system.keys():
            log.info("==== Running " + app_pl + " ====")
            json_dc_dump = {}
            json_dc_dump['common settings'] = gconf.system[app_pl]['sconf'].__dict__
            json_dc_dump['runs'] = {}

            for setting in gconf.system[app_pl]['settings']:
                random.seed(setting.random_seed)
                log.info("Initialized random number generator. Seed: {" + str(setting.random_seed) + "}")
                slx_version = setting.slx_version
                # if config.platform_class is not None:
                #     platform = config.platform_class()
                #     platform_name = platform.name
                # else:
                #     platform_name = os.path.splitext(
                #         os.path.basename(config.platform_xml))[0]
                #     platform = SlxPlatform(platform_name, config.platform_xml, slx_version)
                # create all graphs
                kpns = {}
                # if len(config.applications) > 1:
                #     log.warn("DC Flow just supports one appilcation. The rest will be ignored")
                app_config = (gconf.system[app_pl]['sconf'], setting)
                platform = SlxPlatform(app_config[0].platform_name, app_config[0].platform_xml, slx_version)
                #print(f"config arch{app_config[0].platform_xml}")
                app_name = app_config[0].app_name
                #TODO: check if there is only on kpn in config
                kpn = SlxKpnGraph(app_name, app_config[0].cpn_xml, slx_version)
                #trace_reader = SlxTraceReader.factory(app_config[0].trace_dir, '%s.' % (app_name), slx_version)
                trace_reader_gen = lambda : SlxTraceReader.factory(app_config[0].trace_dir, '%s.' % (app_name), slx_version)

                rep_type_str = app_config[1].representation
                if rep_type_str == "GeomDummy":
                    representation = "GeomDummy"
                elif rep_type_str not in dir(reps.RepresentationType):
                    log.exception("Representation " + rep_type_str + " not recognized. Available: " + ", ".join(dir(reps.RepresentationType)))
                    raise RuntimeError('Unrecognized representation.')
                else:
                    representation_type = reps.RepresentationType[rep_type_str]
                    log.info(f"initializing representation ({rep_type_str})")
                    #import pdb
                    #pdb.set_trace()

                    representation = (representation_type.getClassType())(kpn,platform)

                # run DC algorithm
                # starting volume (init):
                if representation == "GeomDummy":
                    center = [1,2,3,4,5,6,7,8]
                else:
                    center = representation.uniform()
                if (app_config[1].shape == "cube"):
                    v = dc_volume.Cube(center, center.get_numProcs(),app_config[1])
                elif (app_config[1].shape == "lpvol"): 
                    v = dc_volume.LPVolume(center, center.get_numProcs(),kpn,platform,app_config[1],representation_type)


                # config = args.configFile
                oracle = dc_oracle.Oracle(app_config, app_name, kpn, platform, trace_reader_gen)
                dc = designCentering.DesignCentering(v, app_config[1].distr, oracle, representation)
                center = dc.ds_explore()

                # plot explored design space (in 2D)
                #if True:
                #    tp.plot_samples(dc.samples)
                log.info("center: {} radius: {:f}".format(dc.vol.center, dc.vol.radius))
                log.info("==== Design Centering done ====")


                json_dc_dump['runs'][app_config[1].idx] = {}
                json_dc_dump['runs'][app_config[1].idx]['settings'] = app_config[1].__dict__
                json_dc_dump['runs'][app_config[1].idx]['center'] = {}
                json_dc_dump['runs'][app_config[1].idx]['center']['mapping'] = center.getMapping(0).to_list()
                json_dc_dump['runs'][app_config[1].idx]['center']['feasible'] = center.getFeasibility()
                json_dc_dump['runs'][app_config[1].idx]['center']['runtime'] = center.getSimContext().exec_time / 1000000000.0

                # run perturbation test
                if app_config[1].run_perturbation:
                    log.info("==== Run Perturbation Test ====")
                    num_pert = app_config[1].num_perturbations
                    num_mappings = app_config[1].num_mappings
                    pm = p.PerturbationManager( app_config, num_mappings, num_pert)
                    map_set = pm.create_randomMappings()

                    pert_res = []
                    s,c = pm.run_perturbation(center.getMapping(0), pm.apply_singlePerturbation)
                    pert_res.append(s)

                    json_dc_dump['runs'][app_config[1].idx]['center']['pert'] = c
                    json_dc_dump['runs'][app_config[1].idx]['center']['passed'] = s

                    for i,m in enumerate(map_set):
                        s,c = pm.run_perturbation(m, pm.apply_singlePerturbation)
                        pert_res.append(s)
                        json_dc_dump['runs'][app_config[1].idx]['rand mapping' + str(i)] = {}
                        json_dc_dump['runs'][app_config[1].idx]['rand mapping' + str(i)]['mapping'] = m.to_list()
                        json_dc_dump['runs'][app_config[1].idx]['rand mapping' + str(i)]['pert'] = c
                        json_dc_dump['runs'][app_config[1].idx]['rand mapping' + str(i)]['passed'] = s

                    tp.plot_perturbations(pert_res)
                    log.info("==== Perturbation Test done ====")

            if not os.path.exists(gconf.system[app_pl]['sconf'].out_dir):
                os.mkdir(gconf.system[app_pl]['sconf'].out_dir)
            with open(gconf.system[app_pl]['sconf'].out_dir + '/dump.json', 'w+') as dump:
                json.dump(json_dc_dump, dump, indent=4)

    else:
        log.info("usage: python designCentering [x1,x2,...,xn]\n")

    return 0

if __name__ == "__main__":
    main()

# calls
#/slx_random_walk -V ~/misc_code/kpn-apps/audio_filter/parallella/config.ini /tmp -n5000
#./bin/dc_run ~/misc_code/kpn-apps-2/audio_filter/parallella/config.ini -w pykpn.design_centering
