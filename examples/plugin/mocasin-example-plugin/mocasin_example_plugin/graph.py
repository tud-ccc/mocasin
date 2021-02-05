# Copyright (C) 2021 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Authors: Christian Menard


from mocasin.common.graph import DataflowGraph, DataflowProcess, DataflowChannel


class ExampleGraph(DataflowGraph):

    def __init__(self):
        super().__init__("example")

        a = DataflowProcess("a")
        b = DataflowProcess("b")
        c = DataflowChannel("c", 16)

        self.add_process(a)
        self.add_process(b)
        self.add_channel(c)

        a.connect_to_outgoing_channel(c)
        b.connect_to_incomming_channel(c)
