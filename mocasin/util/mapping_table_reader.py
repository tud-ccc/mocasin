# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Robert Khasanov

from mocasin.common.mapping import Mapping
from mocasin.mapper.partial import ComFullMapper, ProcPartialMapper

import csv
import logging

log = logging.getLogger(__name__)


class MappingTableReader:
    """A CSV Mapping Table reader.

    This class reads the content of the CSV file and returns an ordered dict of
    mappings along with its attributes.

    Rows of the CSV table describe different mappings of an application to a
    platform. The columns starting with `process_prefix` and ending with
    `process_suffix` describe the process allocation onto the platform.
    The columns `metadata_exec_time` and `metadata_energy` describe the metadata
    value. The collumns in the `attributes` list describe the additional mapping
    attribute to extract.

    :param platform: The platform.
    :type platform: Platform
    :param graph: The dataflow graph.
    :type graph: DataflowGraph
    :param path: The path to CSV file.
    :type path: string
    :param process_prefix: The prefix of processes in the CSV table.
    :type process_prefix: string
    :param process_suffix: The suffix of processes in the CSV table.
    :type process_suffix: string
    :param metadata_exec_time: The name of the execution time column.
    :type metadata_exec_time: string or None
    :param metadata_energy: The name of the energy column.
    :type metadata_energy: string or None
    :param attributes: The list of attributes to extract.
    :type attributes: list of strings or None
    """

    def __init__(
        self,
        platform,
        graph,
        path,
        process_prefix="t_",
        process_suffix="",
        metadata_exec_time="executionTime",
        metadata_energy="totalEnergy",
        attributes=None,
    ):
        self.platform = platform
        self.graph = graph
        self.path = path

        self._process_prefix = process_prefix
        self._process_suffix = process_suffix
        self._metadata_exec_time = metadata_exec_time
        self._metadata_energy = metadata_energy
        self._attributes = attributes
        if self._attributes is None:
            self._attributes = []

        # Parsed data
        self._data = []
        # Read and constructed mappings
        self.mappings = None

        self.com_mapper = ComFullMapper(graph, platform)
        self.mapper = ProcPartialMapper(graph, platform, self.com_mapper)

        self._process_names = [p.name for p in self.graph.processes()]

        self._processor_numbers = {}
        for i, pe in enumerate(self.platform.processors()):
            self._processor_numbers[pe.name] = i

        self._read_csv()

    def _read_csv(self):
        prefix = self._process_prefix
        suffix = self._process_suffix
        time_col = self._metadata_exec_time
        energy_col = self._metadata_energy

        with open(self.path) as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                to_update = {}

                for name in self._process_names:
                    to_update.update({name: row[prefix + name + suffix]})
                # Save desired property to a dict
                for p in self._attributes:
                    to_update.update({p: row[p]})
                # Save energy-utility metadata to a dict
                if time_col is not None:
                    to_update.update({time_col: row[time_col]})
                if energy_col is not None:
                    to_update.update({energy_col: row[energy_col]})
                self._data.append(to_update)

    def form_mappings(self):
        """Form mappings from the parsed data.

        Returns the list of tuples, the first element of the tuple is the
        `Mapping` object, the next elements are the attribute values in the
        order of `attributes` paramater.
        """
        if self.mappings is not None:
            log.warning("Mappings were already generated, returning them.")
            return self.mappings

        time_col = self._metadata_exec_time
        energy_col = self._metadata_energy
        self.mappings = []
        for entry in self._data:
            from_list = []

            for process in self._process_names:
                pe = self._processor_numbers[entry[process]]
                from_list.append(pe)

            if from_list != []:
                mapping = self.mapper.generate_mapping(from_list)
                # Update energy-utility metadata
                if time_col is not None:
                    mapping.metadata.exec_time = float(entry[time_col])
                if energy_col is not None:
                    mapping.metadata.energy = float(entry[energy_col])
            else:
                mapping = Mapping(self.graph, self.platform)

            self.mappings.append(
                (mapping,) + tuple(entry[p] for p in self._attributes)
            )
        return self.mappings
