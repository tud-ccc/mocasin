#!/usr/bin/env python3

# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andres Goens

import logging
import hydra
from pykpn.util.multirun_reader import read_multirun
from importlib import import_module

log = logging.getLogger(__name__)

_parsers = {
    'mapper_statistics': (
       'pykpn.mapper.utils',
       'statistics_parser',
       'Parses the statistics file from a mapper'),
}

def available_parsers():
    res_str = ""
    for parser in _parsers:
        res_str += parser + ":\n"
        res_str += _parsers[parser][2] + ":\n"
    return res_str


def load_parser(name):
   """Loads an individual task.

   :param task: name of the task to be executed
   :return:
   """

   if name not in _parsers:
       log.error(f"Unknown parser: {name}. Available parsers are:" + available_parsers())
       raise RuntimeError()

   else:
       # load the parser
       module_name = _parsers[name][0]
       function_name = _parsers[name][1]
       module = import_module(module_name)
       function = getattr(module, function_name)
       return function


@hydra.main(config_path='../conf', config_name='parse_multirun')
def parse_multirun(cfg):
    try:
        parsers = []
        for parser in cfg['parsers']:
            parsers.append(load_parser(parser))
        path = cfg['path']
        read_multirun(path,parsers)
    except Exception:
        print("parse_multirun usage: pykpn parse_multirun path=<multirun_root_directory> parsers=[<parser list>]\n")
        print("For example, to look at the mapper statistics after a multirun mapping:")
        print("pykpn path=parse_multirun examples/multirun/1999-12-31-23-59-59 parsers=[mapper_statistics]")


