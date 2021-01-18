# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Felix Teweleit

import math
from mocasin.common.graph import DataflowProcess, DataflowChannel, DataflowGraph
from mocasin.common.platform import (
    Processor,
    FrequencyDomain,
    CommunicationResource,
)


class TgffProcessor:
    """Represents the relevant information about a processor, included in a .tgff file.
    The processor can be transfered into the mocasin representation.
    """

    def __init__(self, name, operations, processor_type):
        self.name = name
        self.type = processor_type
        self.operations = {}
        self.cycle_time = self._get_cycle_time(operations)
        self._transform_operations(operations)

    def get_operation(self, idx):
        return self.operations[idx]

    def to_mocasin_processor(self):
        """Returns a mocasin Processor object, equivalent to the TgffProcessor object.
        :returns: equivalent processor object
        :rtype: Processor
        """
        frequency_domain = FrequencyDomain(
            "fd{0}".format(self.name), math.ceil(1 / self.cycle_time)
        )
        return Processor(self.name, self.type, frequency_domain)

    def _get_cycle_time(self, operations):
        """Calculates the time needed for a single processor cycle, in a way that the
        execution time og all operations are an integer multiple of the cycle time.

        :param operations: maps the indentifier of an operation to its execution time
        :type operations: dict{int : int}
        :returns: largest possible time step for a single cylce
        :rtype: float
        """
        task_time = 1

        for properties in operations.values():
            if properties[2] < task_time and not properties[2] == 0:
                task_time = properties[2]

        tmp_string = list("{0:1.12f}".format(task_time))
        i = len(tmp_string) - 1

        while i > 1:
            if not tmp_string[i] == "0":
                return 1 * (10 ** -(i - 1))
            else:
                i -= 1
        return i

    def _transform_operations(self, operations):
        """Transforms the mapping of operation identifier to execution time
        to a mapping of operation identifier to execution cycles.

        :param operations: mapping of identifier to execution time
        :type operations: dict {int : int}
        """
        for key, properties in operations.items():
            cycles = int(properties[2] / self.cycle_time)
            self.operations.update({key: cycles})


class TgffGraph:
    """Represents the relevant information about a task graph, parsed from
    a .tgff file. The tgff graph can be transfered into a dataflow graph.
    """

    def __init__(self, identifier, task_set, channel_set, quantities):
        self.identifier = identifier
        self.tasks = task_set
        self.channels = channel_set
        self._quantities = quantities

    def get_task_type(self, identifier):
        return self.tasks[identifier]

    def get_execution_order(self, task_name):
        """Returns the order of actions for a single task (node) of the task
        graph

        :param task_name: the name of the specific task
        :type task_name: String
        :returns the order and type of actions the task performs when executed
        :rtype list[tuple(char, string)] a list of actions (read, write execute)
        and their target operation/channel
        """
        execution_order = []
        read_from = []
        write_to = []

        for name, properties in self.channels.items():
            # source
            if task_name == properties[0]:
                write_to.append(name)
            # sink
            if task_name == properties[1]:
                read_from.append(name)

        for channel_name in read_from:
            execution_order.append(("r", channel_name))

        execution_order.append(("e", self.tasks[task_name]))

        for channel_name in write_to:
            execution_order.append(("w", channel_name))

        return execution_order

    def to_dataflow_graph(self):
        """Transfers the the tgff graph into a dataflow graph
        :returns: the equivalent dataflow graph representation
        :rtype: DataflowGraph
        """
        graph = DataflowGraph(self.identifier)
        tasks = []
        channels = []

        # Create process for each node in
        for task in self.tasks:
            task = DataflowProcess(task)
            tasks.append(task)

        # Create channel for each edge in
        for key, properties in self.channels.items():
            name = key
            token_size = int(self._quantities[0][int(properties[2])])
            channel = DataflowChannel(name, token_size)

            for task in tasks:
                if task.name == properties[0]:
                    task.connect_to_outgoing_channel(channel)
                if task.name == properties[1]:
                    task.connect_to_incomming_channel(channel)

            channels.append(channel)

        # Add channels and processes to empty
        for task in tasks:
            graph.add_process(task)

        for channel in channels:
            graph.add_channel(channel)

        return graph


class TgffLink:
    """Represents the information about a hardware link included in a .tgff file."""

    def __init__(self, name, throughput):
        self.name = name
        self.throughput = throughput

    def to_mocasin_communication_resource(self):
        """Transfers the tgff hardware representation into mocasin representation.
        ATTENTION: tgff does not include all necessary information. Mocasin link object
        will be incomplete!
        :returns: An equivalent mocasin communication resource object
        :rtype: CommunicationRessource
        """
        return CommunicationResource(
            self.name,
            None,
            None,
            None,
            self.throughput,
            self.throughput,
            False,
            False,
        )
