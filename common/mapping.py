# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


from enum import Enum
from itertools import product
import pydot

class SchedulingPolicy(Enum):
    FIFO = 0
    RoundRobin=1


class ChannelInfo:
    name = None
    capacity = None
    fromProcessor = None
    toProcessor = None
    viaMemory = None
    primitive = None


class SchedulerInfo:
    name = None
    policy = None
    processNames = None
    processorNames = None


class Mapping:
    def __init__(self):
        self.schedulers = []
        self.channels = []
        self.arch = None
        self.kpn = None



    def getProcess2PEDict(self):
        process2pe = dict()
        for sched in self.schedulers:
            assert len(sched.processorNames) == 1 , ("Schedule (" + str(sched) + ") does not have exactly one PE.")
            for process in sched.processNames:
                process2pe[process] = sched.processorNames[0]
        return process2pe

    def getChann2CPDict(self):
        chann2cp = dict()
        for chann in self.channels:
            chann2cp[chann.name] = (chann.viaMemory,chann.primitive)



    def toPyDot(self,application,proc_labels=True,pe_labels=True,link_labels=False):
        process2pe = self.getProcess2PEDict()
        pe2process = { pe : [] for pe in process2pe.values()}
        for proc in process2pe:
            pe2process[process2pe[proc]].append(proc)

        cpn_graph = pydot.Dot(graph_type='digraph')

        for pe in pe2process:
            if pe_labels == True:
                cluster = pydot.Cluster(str(pe),label=str(pe))
            else:
                cluster = pydot.Cluster(str(pe))
            for proc in pe2process[pe]:
                if proc_labels == True:
                    cluster.add_node(pydot.Node(str(proc),label=str(proc)))
                else:
                    cluster.add_node(pydot.Node(str(proc),label=" "))
            cpn_graph.add_subgraph(cluster)


        # Create and add empty fifo channels for all the pn channels
        links_from = {}
        links_to = {}

        # Note that this does not check if the app corresponds to the mapping!
        # If the mapping at some point supports references and not only strings we should get rid of this necessity
        for pnchannel in application.channels:
            links_from[pnchannel.name] = []
            links_to[pnchannel.name] = []

        for proc in application.processes:
            for out_edge in  proc.outgoing_channels:
                links_from[out_edge.name].append(proc.name)
            for in_edge in  proc.incoming_channels:
                links_to[in_edge.name].append(proc.name)

        for link in links_from:
            edges = product(*[links_from[link],links_to[link]])
            for (v,w) in edges:
                if link_labels == True:
                    cpn_graph.add_edge(pydot.Edge(str(v),str(w),label=link))
                else:
                    cpn_graph.add_edge(pydot.Edge(str(v),str(w)))
        return cpn_graph

    def outputDot(self,application,filename,proc_labels=True,pe_labels=True,link_labels=False):
        self.toPyDot(application,proc_labels=proc_labels,pe_labels=pe_labels,link_labels=link_labels).write_raw(filename)
