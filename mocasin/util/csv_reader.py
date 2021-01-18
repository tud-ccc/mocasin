# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit, Robert Khasanov

import csv
import zipfile
import os

from _collections import OrderedDict
from mocasin.common.mapping import Mapping
from mocasin.common.platform import Platform
from mocasin.common.graph import DataflowGraph
from mocasin.mapper.partial import ComFullMapper, ProcPartialMapper

# TODO(RK): Make a unit test which checks a case with multiple objectives


class DataReader:
    def __init__(
        self,
        platform,
        graph,
        file_path,
        attribute="default",
        process_prefix="default",
        process_suffix="default",
        exec_time_col=None,
        energy_col=None,
    ):
        if not isinstance(platform, Platform):
            raise RuntimeError("Platform object is not valid")

        if not isinstance(graph, DataflowGraph):
            raise RuntimeError("DataflowGraph object is not valid")

        self._mProcessNames = []
        self._mProcessorNumbers = {}
        self._mDataDict = {}
        self._mMappingDict = OrderedDict()
        self._mPlatform = platform
        self._mGraphInstance = graph
        self._mComMapper = ComFullMapper(graph, platform)
        self._mMapper = ProcPartialMapper(graph, platform, self._mComMapper)

        for process in sorted(
            [x.name for x in self._mGraphInstance.processes()]
        ):
            self._mProcessNames.append(process)
        for i, pe in enumerate(
            sorted([x.name for x in self._mPlatform.processors()])
        ):
            self._mProcessorNumbers[pe] = i

        if attribute == "default":
            self._desiredProperty = "wall_clock_time"
        else:
            self._desiredProperty = attribute

        if not isinstance(self._desiredProperty, list):
            self._desiredProperty = [self._desiredProperty]

        if process_prefix == "default":
            self._prefix = "t_"
        else:
            self._prefix = process_prefix

        if process_suffix == "default":
            self._suffix = ""
        else:
            self._suffix = process_suffix

        self._exec_time_col = exec_time_col
        self._energy_col = energy_col

        path_as_list = file_path.split("/")
        last_element = path_as_list[len(path_as_list) - 1]
        if last_element.split(".")[len(last_element.split(".")) - 1] == "zip":

            with zipfile.ZipFile(file_path, "r") as zipFile:
                i = 0

                for file in zipFile.namelist():
                    extracted = zipFile.extract(file)

                    with open(extracted) as csvFile:
                        reader = csv.DictReader(csvFile)

                        for row in reader:
                            to_update = {i: {}}

                            for name in self._mProcessNames:
                                to_update[i].update(
                                    {
                                        name: row[
                                            self._prefix + name + self._suffix
                                        ]
                                    }
                                )
                            # Save desired property to a dict
                            for p in self._desiredProperty:
                                to_update[i].update({p: row[p]})
                            # Save energy-utility metadata to a dict
                            if self._exec_time_col is not None:
                                to_update[i].update(
                                    {
                                        self._exec_time_col: row[
                                            self._exec_time_col
                                        ]
                                    }
                                )
                            if self._energy_col is not None:
                                to_update[i].update(
                                    {self._energy_col: row[self._energy_col]}
                                )
                            self._mDataDict.update(to_update)
                            i += 1

                    os.remove(extracted)

        else:

            with open(file_path) as csvFile:
                reader = csv.DictReader(csvFile)
                i = 0

                for row in reader:
                    to_update = {i: {}}

                    for name in self._mProcessNames:
                        to_update[i].update(
                            {name: row[self._prefix + name + self._suffix]}
                        )
                    # Save desired property to a dict
                    for p in self._desiredProperty:
                        to_update[i].update({p: row[p]})
                    # Save energy-utility metadata to a dict
                    if self._exec_time_col is not None:
                        to_update[i].update(
                            {self._exec_time_col: row[self._exec_time_col]}
                        )
                    if self._energy_col is not None:
                        to_update[i].update(
                            {self._energy_col: row[self._energy_col]}
                        )
                    self._mDataDict.update(to_update)
                    i += 1

    def formMappings(self):
        for entry in self._mDataDict:
            fromList = []

            for key in self._mProcessNames:
                pe = self._mProcessorNumbers[self._mDataDict[entry][key]]
                fromList.append(pe)

            if fromList != []:
                mapping = self._mMapper.generate_mapping(fromList)
                # Update energy-utility metadata
                if self._exec_time_col is not None:
                    mapping.metadata.exec_time = float(
                        self._mDataDict[entry][self._exec_time_col]
                    )
                if self._energy_col is not None:
                    mapping.metadata.energy = float(
                        self._mDataDict[entry][self._energy_col]
                    )
            else:
                mapping = Mapping(self._mGraphInstance, self._mPlatform)

            self._mMappingDict.update(
                {
                    entry: (mapping,)
                    + tuple(
                        self._mDataDict[entry][p] for p in self._desiredProperty
                    )
                }
            )
        return self._mMappingDict


class DataReaderFromHydra(DataReader):
    def __init__(self, platform, graph, cfg):
        file_path = cfg["csv_file"]
        attribute = cfg["property"]
        process_prefix = cfg["prefix"]
        process_suffix = cfg["suffix"]
        super(DataReaderFromHydra, self).__init__(
            platform,
            graph,
            file_path,
            attribute,
            process_prefix,
            process_suffix,
        )
