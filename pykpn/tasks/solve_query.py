#Copyright (C) 2020 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

import hydra
from pykpn.util.logging import getLogger
from pykpn.ontologies.solver import Solver

logger = getLogger(__name__)

@hydra.main(config_path='conf/solve_query.yaml')
def solve_query(cfg):
    #TODO:
    #find a way to hand in a set of mappings on which equal_operations can be applied

    kpn = hydra.utils.instantiate(cfg['kpn'])
    platform = hydra.utils.instantiate(cfg['platform'])
    query = cfg['query']
    vector = cfg['vector']

    solver = Solver(kpn, platform)

    if not vector == 'None':
        starting_vector = []

        for element in vector.split(','):
            starting_vector.append(int(element))

        result = solver.request(query, vec=starting_vector)

    else:
        result = solver.request(query)

    print(result.to_list())
