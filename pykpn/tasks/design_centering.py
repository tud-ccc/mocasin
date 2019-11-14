#!/usr/bin/env python3

# Copyright (C) 2017-2019 TU Dresden
# All Rights Reserved
#
# Authors: Gerald Hempel, Andres Goens

import os
import json
import logging
import random

from pykpn.slx.kpn import SlxKpnGraph
from pykpn.slx.platform import SlxPlatform

from pykpn.design_centering.design_centering import dc_oracle
from pykpn.design_centering.design_centering import dc_volume
from pykpn.design_centering.design_centering import designCentering
from pykpn.design_centering.design_centering import perturbationManager as p
from pykpn.representations import representations as reps

log = logging.getLogger(__name__)

def dc_task(cfg):
    json_dc_dump = {
        'config' : {
            'max_samples': cfg['max_samples'],
            'adapt_samples': cfg['adapt_samples'],
            'hitting_probability': list(cfg['hitting_probability']),
            'deg_p_polynomial': cfg['deg_p_polynomial'],
            'step_width': list(cfg['step_width']),
            'deg_s_polynomial': cfg['deg_s_polynomial'],
            'adaptable_center_weights': cfg['adaptable_center_weights'],
            'max_step': cfg['max_step'],
            'show_polynomials': cfg['show_polynomials'],
            'show_points': cfg['show_points'],
            'max_pe': cfg['max_pe'],
            'distr': cfg['distr'],
            'shape': cfg['shape'],
            'oracle': cfg['oracle'],
            'random_seed': cfg['random_seed'],
            'threshold': cfg['threshold'],
            'run_perturbation': cfg['run_perturbation'],
            'num_perturbations': cfg['num_perturbations'],
            'representation': cfg['representation'],
            'keep_metrics': cfg['keep_metrics'],
            'visualize_mappings': cfg['visualize_mappings'],
            'slx_version': cfg['slx_version'],
            'start_time': cfg['start_time'],
            'cpn_xml': cfg['cpn_xml'],
            'platform_xml': cfg['platform_xml'],
            'app_name': cfg['app_name'],
            'platform_name': cfg['platform_name'],
            'trace_dir': cfg['trace_dir'],
        }}
    tp = designCentering.ThingPlotter()
    random.seed(cfg['random_seed'])
    log.info("Initialized random number generator. Seed: {" + str(cfg['random_seed']) + "}")
    slx_version = cfg['slx_version']
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
    #app_config = (gconf.system[app_pl]['sconf'], setting) #TODO: where is this being read?
    platform = SlxPlatform(cfg['platform_name'], cfg['platform_xml'], cfg['slx_version'])
    app_name = cfg['app_name']
    kpn = SlxKpnGraph(app_name, cfg['cpn_xml'], slx_version)
    rep_type_str = cfg['representation']
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
    if (cfg['shape'] == "cube"):
        v = dc_volume.Cube(center, center.get_numProcs(),cfg) #TODO: refactor, remove unnecessary arguments passed
    elif (cfg['shape'] == "lpvol"):
        v = dc_volume.LPVolume(center, center.get_numProcs(),kpn,platform,cfg,representation_type)#TODO: refactor, remove unnecessary arguments passed


    # config = args.configFile
    oracle = dc_oracle.Oracle(cfg) #TODO: propagate cfg change here
    dc = designCentering.DesignCentering(v, cfg['distr'], oracle,representation)
    center = dc.ds_explore()

    # plot explored design space (in 2D)
    #if True:
    #    tp.plot_samples(dc.samples)
    log.info("center: {} radius: {:f}".format(dc.vol.center, dc.vol.radius))
    log.info("==== Design Centering done ====")


    json_dc_dump['center'] = {}
    json_dc_dump['center']['mapping'] = center.getMapping(0).to_list()
    json_dc_dump['center']['feasible'] = center.getFeasibility()
    json_dc_dump['center']['runtime'] = center.getSimContext().exec_time / 1000000000.0

    # run perturbation test
    if cfg['run_perturbation']:
        log.info("==== Run Perturbation Test ====")
        num_pert = cfg['num_perturbations']
        num_mappings = cfg['num_reference_mappings']
        pm = p.PerturbationManager( cfg, num_mappings, num_pert) #TODO: propagate cfg
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

    if not os.path.exists(cfg['out_dir']):
        os.mkdir(cfg['out_dir'])
    with open(cfg['out_dir'] + '/dc_out.json', 'w+') as dump:
        json.dump(json_dc_dump, dump, indent=4)
if __name__ == "__main__":
    main()

# calls
#/slx_random_walk -V ~/misc_code/kpn-apps/audio_filter/parallella/config.ini /tmp -n5000
#./bin/dc_run ~/misc_code/kpn-apps-2/audio_filter/parallella/config.ini -w pykpn.design_centering
