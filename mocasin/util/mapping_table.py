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

    This class reads the content of the CSV file and returns a list of
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


class MappingTableWriter:
    """A CSV Mapping Table Writer.

    This class writes the multiple mappings of one application onto the platform
    in the CSV file.

    The output CSV format description:
    Rows of the CSV table describe different mappings of an application to a
    platform. The columns starting with `process_prefix` and ending with
    `process_suffix` describe the process allocation onto the platform.
    The columns `metadata_exec_time` and `metadata_energy` describe the metadata
    value.

    Usage:
    ```
    writer = MappingTableWriter(platform, graph, path)
    writer.open()
    writer.write_header()
    writer.write_mapping(mapping1)
    writer.write_mapping(mapping2)
    writer.close()
    ```

    Altenatevely, you may use with-statements:
    ```
    with MappingTableWriter(platform, graph, path) as writer:
        writer.write_header()
        writer.write_mapping(mapping1)
        writer.write_mapping(mapping2)
    ```

    :param platform: The platform.
    :type platform: Platform
    :param graph: The dataflow graph.
    :type graph: DataflowGraph
    :param path: Path to the output file.
    :type path: string
    :param process_prefix: The prefix of processes in the CSV table.
    :type process_prefix: string
    :param process_suffix: The suffix of processes in the CSV table.
    :type process_suffix: string
    :param metadata_exec_time: The name of the execution time column.
    :type metadata_exec_time: string or None
    :param metadata_energy: The name of the energy column.
    :type metadata_energy: string or None
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
    ):
        self.platform = platform
        self.graph = graph
        self.path = path
        self.file = None
        self.csv = None

        self._process_prefix = process_prefix
        self._process_suffix = process_suffix
        self._metadata_exec_time = metadata_exec_time
        self._metadata_energy = metadata_energy

        # Generate field names
        self.fieldnames = ["mapping"]  # mapping identifier
        self.fieldnames.extend(
            [self._process_fieldname(p.name) for p in graph.processes()]
        )
        self.fieldnames.append(metadata_exec_time)
        self.fieldnames.append(metadata_energy)

        # Initialize counter
        self._cnt = 0

    def _process_fieldname(self, name):
        return self._process_prefix + name + self._process_suffix

    def open(self):
        """Open a file to write."""
        self.file = open(self.path, "w")
        self.csv = csv.DictWriter(self.file, fieldnames=self.fieldnames)

    def __enter__(self):
        self.open()
        return self

    def close(self):
        """Close file."""
        self.file.close()
        self.file = None
        self.csv = None

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def write_header(self):
        """Write header line."""
        self.csv.writeheader()
        pass

    def write_mapping(self, mapping):
        """Write a mapping to the file.

        :param mapping: Mapping to write
        :type mappings: Mapping
        """
        d = {"mapping": self._cnt}

        if mapping.graph.name != self.graph.name:
            raise RuntimeError(
                f"Attempting to write the mapping for the application "
                f"{mapping.graph.name}, while the MappingTableWriter is "
                f"initialized for the application {self.graph.name}"
            )

        if mapping.platform.name != self.platform.name:
            raise RuntimeError(
                f"Attempting to write the mapping to the platform "
                f"{mapping.platform.name}, while the MappingTableWriter is "
                f"initialized for the platform {self.platform.name}"
            )

        # Write processes
        for p in self.graph.processes():
            d.update(
                {self._process_fieldname(p.name): mapping.affinity(p).name}
            )

        # Write metadata
        d.update({self._metadata_exec_time: mapping.metadata.exec_time})
        d.update({self._metadata_energy: mapping.metadata.energy})

        self.csv.writerow(d)
        self._cnt += 1
        pass
