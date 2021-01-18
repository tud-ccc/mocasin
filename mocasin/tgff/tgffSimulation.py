# Copyright (C) 2020 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Andres Goens

from mocasin.tgff.trace import TgffTraceGenerator
from mocasin.tgff.tgffParser.parser import Parser


import logging

log = logging.getLogger(__name__)

_parsed_tgff_files = {}


class TgffReferenceError(Exception):
    """Referenced a non existent tgff component"""

    pass


class DataflowGraphFromTgff:
    """New, since we want to return a common.graph instance instead of am TgffToDataflowGraph instance"""

    def __new__(cls, tgff_file, name):
        if tgff_file not in _parsed_tgff_files:
            _parsed_tgff_files.update(
                {tgff_file: Parser().parse_file(tgff_file, [])}
            )
            log.warning(
                "TGFF traces should to be initialized first before the application, otherwise processor types might be inconsistent."
            )

        tgff_graphs = _parsed_tgff_files[tgff_file][0]

        if name not in tgff_graphs:
            raise TgffReferenceError()

        return tgff_graphs[name].to_dataflow_graph()


class TraceGeneratorWrapper:
    def __new__(cls, tgff_file, graph_name, repetition=1, processor_types=None):
        if tgff_file not in _parsed_tgff_files:
            if processor_types is None:
                proc_type_list = []
            else:
                proc_type_list = processor_types
            _parsed_tgff_files.update(
                {tgff_file: Parser().parse_file(tgff_file, proc_type_list)}
            )

        tgff_components = _parsed_tgff_files[tgff_file]
        if graph_name not in tgff_components[0]:
            raise TgffReferenceError()

        processor_dict = {}

        for processor in tgff_components[1]:
            processor_dict.update({processor.type: processor})

        trace_generator = TgffTraceGenerator(
            processor_dict, tgff_components[0][graph_name], repetition
        )

        return trace_generator

    def __init__(self, *args, **kwargs):
        pass
