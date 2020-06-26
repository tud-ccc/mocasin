#!/usr/bin/env python3

# Copyright (C) 2017-2020 TU Dresden
# All Rights Reserved
#
# Authors: Gerald Hempel, Andres Goens

import os
import json
import logging
import random
import hydra
import numpy as np
import sys

from pykpn.design_centering import DesignCentering
from pykpn.design_centering import volume
from pykpn.design_centering import sample as dc_sample
from pykpn.design_centering import oracle as o
from pykpn.design_centering import util as dc_util
from pykpn.design_centering import perturbation_manager as p
from pykpn.representations import representations as reps

log = logging.getLogger(__name__)


@hydra.main(config_path='conf/design_centering.yaml')
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
            'perturbation_type': cfg['perturbation_type'],
            'run_perturbation': cfg['run_perturbation'],
            'num_perturbations': cfg['num_perturbations'],
            'representation': cfg['representation'],
            'keep_metrics': cfg['keep_metrics'],
            'visualize_mappings': cfg['visualize_mappings'],
            'start_time': cfg['start_time'],
            'app': cfg['kpn']['name'],
            'platform': cfg['platform']['name'],
            'starting_radius': cfg['radius'],
            #'trace_dir': cfg['trace_dir'],
        }}
    if 'periodic_boundary_conditions' in cfg:
        json_dc_dump['config']['periodic_boundary_conditions'] = cfg['periodic_boundary_conditions']
    tp = dc_util.ThingPlotter()
    random.seed(cfg['random_seed'])
    np.random.seed(cfg['random_seed'])
    log.info("Initialized random number generator. Seed: {" + str(cfg['random_seed']) + "}")
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

    kpn = hydra.utils.instantiate(cfg['kpn'])
    platform = hydra.utils.instantiate(cfg['platform'])

    rep_type_str = cfg['representation']
    if rep_type_str == "GeomDummy":
        representation = "GeomDummy"
    elif rep_type_str not in dir(reps.RepresentationType):
        log.exception("Representation " + rep_type_str + " not recognized. Available: " + ", ".join(dir(reps.RepresentationType)))
        raise RuntimeError('Unrecognized representation.')
    else:
        representation_type = reps.RepresentationType[rep_type_str]
        log.info(f"initializing representation ({rep_type_str})")

        representation = (representation_type.getClassType())(kpn,platform,cfg)

    # run DC algorithm

    oracle = o.Oracle(cfg)

    # starting volume (init):
    if representation == "GeomDummy":
        starting_center = [1,2,3,4,5,6,7,8]
    else:
        timeout = 0
        while timeout < cfg['perturbation_max_iters']:
            starting_center = representation.uniform()
            starting_center_sample = dc_sample.Sample(sample=representation.toRepresentation(starting_center),representation = representation)
            oracle.validate_set([starting_center_sample])
            if starting_center_sample.getFeasibility() == True:
                break
            else:
                timeout += 1
    if timeout == cfg['perturbation_max_iters']:
        log.error(f"could not find a feasible starting center after {timeout} iterations")
        sys.exit(1)

    log.info(f"Starting with center: {starting_center.to_list()}")
    #center = dc_sample.Sample(center)

    if (cfg['shape'] == "cube"):
        v = volume.Cube(starting_center, starting_center.get_numProcs(),cfg) #TODO: refactor, remove unnecessary arguments passed
    elif (cfg['shape'] == "lpvol"):
        v = volume.LPVolume(starting_center, starting_center.get_numProcs(),kpn,platform,cfg,representation_type)#TODO: refactor, remove unnecessary arguments passed


    # config = args.configFile
    dc = DesignCentering(v, cfg['distr'], oracle, representation,cfg['record_samples'],cfg['hitting_probability_threshold'])

    center,history = dc.ds_explore()
    centers = history['centers']
    samples = history['samples']
    radii = history['radii']
    # plot explored design space (in 2D)
    #if True:
    #    tp.plot_samples(dc.samples)
    log.info("center: {} radius: {:f}".format(dc.vol.center, dc.vol.radius))
    log.info("==== Design Centering done ====")


    json_dc_dump['center'] = {}
    json_dc_dump['center']['mapping'] = center.getMapping(0).to_list()
    json_dc_dump['center']['feasible'] = center.getFeasibility()
    json_dc_dump['center']['runtime'] = center.getSimContext().exec_time / 1000000000.0
    # FIXME: This crashs with index out of range:
    #json_dc_dump['center']['radius'] = radii[-1]
    if cfg['record_samples']:
        json_dc_dump['samples'] = {}
        for cent_idx,cent in enumerate(centers):
            json_dc_dump['samples'][cent_idx] = { 'center' : {}}
            json_dc_dump['samples'][cent_idx]['center']['mapping'] = cent.getMapping(0).to_list()
            json_dc_dump['samples'][cent_idx]['center']['feasible'] = cent.getFeasibility()
            json_dc_dump['samples'][cent_idx]['center']['runtime'] = cent.getSimContext().exec_time / 1000000000.0
            json_dc_dump['samples'][cent_idx]['center']['radius'] = radii[cent_idx]


        n = cfg['adapt_samples']
        for i,sample in enumerate(samples):
            idx = int(i/n)
            json_dc_dump['samples'][idx][i%n] = { 'mapping' : sample.getMapping(0).to_list()}
            json_dc_dump['samples'][idx][i%n]['feasible'] = sample.getFeasibility()
            json_dc_dump['samples'][idx][i%n]['runtime'] = sample.getSimContext().exec_time / 1000000000.0

    # run perturbation test
    if cfg['run_perturbation']:
        log.info("==== Run Perturbation Test ====")
        num_pert = cfg['num_perturbations']
        num_mappings = cfg['num_reference_mappings']
        pm = p.PerturbationManager( cfg, num_mappings, num_pert) #TODO: propagate cfg
        if cfg['perturbation_type'] == 'classic':
            pert_func = pm.apply_singlePerturbation
        elif cfg['perturbation_type'] == 'representation':
            pert_func = pm.applyPerturbationRepresentation
        else:
            log.error(f"Unknown perturbation type: {cfg['perturbation_type']} ")
            sys.exit(1)
        map_set = pm.create_randomMappings()

        pert_res = []
        s,c = pm.run_perturbation(center.getMapping(0), pert_func)
        pert_res.append(s)

        json_dc_dump['center']['pert'] = c
        json_dc_dump['center']['passed'] = s

        for i,m in enumerate(map_set):
            s,c = pm.run_perturbation(m, pert_func)
            pert_res.append(s)
            json_dc_dump['rand mapping' + str(i)] = {}
            json_dc_dump['rand mapping' + str(i)]['mapping'] = m.to_list()
            json_dc_dump['rand mapping' + str(i)]['pert'] = c
            json_dc_dump['rand mapping' + str(i)]['passed'] = s

        if bool(cfg['plot_perturbations']) and not os.environ.get('DISPLAY', '') == '':
            tp.plot_perturbations(pert_res,cfg['perturbations_out'])
        log.info("==== Perturbation Test done ====")
    #FIXME: it should probably not be oracle.oracle
    log.info(f"total simulations from cache: {oracle.oracle.total_cached}")

    if not os.path.exists(cfg['out_dir']):
        os.mkdir(cfg['out_dir'])
    with open(cfg['out_dir'] + '/dc_out.json', 'w+') as dump:
        json.dump(json_dc_dump, dump, indent=4)

