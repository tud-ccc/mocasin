# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Andres Goens

import logging
import hydra

from hydra.utils import to_absolute_path
from os import scandir
from mocasin.util.multirun_reader import read_multirun
from importlib import import_module

log = logging.getLogger(__name__)


class ParserNotFoundException(Exception):
    pass


_parsers = {
    "mapper_statistics": (
        "mocasin.mapper.utils",
        "statistics_parser",
        "Parses the statistics file from a mapper.",
    ),
    "best_mapping_time": (
        "mocasin.mapper.utils",
        "best_time_parser",
        "Parses the execution time from the best mapping found.",
    ),
    "cache_dump_csv": (
        "mocasin.mapper.utils",
        "cache_dump_csv_parser",
        "Parses cache dumps (csv) from iterative mappers.",
    ),
    "cache_dump_h5": (
        "mocasin.mapper.utils",
        "cache_dump_h5_parser",
        "Parses cache dumps (h5) from iterative mappers.",
    ),
    "evolutionary_logbook": (
        "mocasin.mapper.utils",
        "evolutionary_logbook_parser",
        "Parses the evolutionary logbooks from the genetic mapper.",
    ),
    "estimated_total_time": (
        "mocasin.util.multirun_reader",
        "total_time_estimator",
        "Estimates the total execution time for each run using timestamps.",
    ),
    "simulate_summary": (
        "mocasin.tasks.simulate",
        "summary_parser",
        "Parses the summary file from a simulation.",
    ),
}


def available_parsers():
    res_str = ""
    for parser in _parsers:
        res_str += parser + ":\n"
        res_str += _parsers[parser][2] + ":\n"
    return res_str


def load_parser(name):
    """Loads an individual parser.

    :param name: name of the parser to be executed
    :return:
    """

    if name not in _parsers:
        log.error(
            f"Unknown parser: {name}. Available parsers are:\n\n"
            + available_parsers()
        )
        raise ParserNotFoundException()

    else:
        # load the parser
        module_name = _parsers[name][0]
        function_name = _parsers[name][1]
        module = import_module(module_name)
        function = getattr(module, function_name)
        return function


def parse_multirun(cfg):
    """This task parses the directory structure of a Hydra multirun execution.
    It generates a csv file with all options given explicitly to the multirun as columns,
    and every row corresponds to a single execution of the multirun sweep.

    The task can be configured in a modular fashion by adding different parsers. The parsers
    will read a concrete file and generate results to be added as columns in the output csv.
    These parsers are intended to be usecase-specific. The parsers to be used are given as a list
    in the hydra conifuration file.

    Hydra parameters:
     - path: the path of the root of the multirun directory. If empty it will
     search for the latest (by name) in ./multirun/*
     - parsers: a list of the parses to be used

    :param cfg: Hydra (Omegaconf) config file.
    """
    hydra.utils.call(cfg["plugin"])

    try:
        parsers = []
        for parser in cfg["parsers"]:
            parsers.append(load_parser(parser))
        path = cfg["path"]
        if path == "":
            multirun_dirs = sorted(
                [
                    to_absolute_path(x.path)
                    for x in scandir(to_absolute_path("multirun/"))
                    if x.is_dir()
                ]
            )
            path = multirun_dirs[-1]
        else:
            path = to_absolute_path(path)
        read_multirun(
            path,
            parsers,
            output_format=cfg["output_format"],
            output_filename=cfg["output_filename"],
        )
    except ParserNotFoundException:
        print_usage()
        raise ParserNotFoundException()


def print_usage():
    print(
        "parse_multirun usage: mocasin parse_multirun path=<multirun_root_directory> parsers=[<parser list>]\n"
    )
    print(
        "For example, to look at the mapper statistics after a multirun mapping:"
    )
    print(
        "mocasin path=parse_multirun examples/multirun/1999-12-31-23-59-59 parsers=[mapper_statistics]"
    )
    print(
        "-------------------------------------------------------------------------------------------\n"
    )
