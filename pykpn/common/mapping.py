# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


from enum import Enum
from itertools import product
import pydot


class ChannelMappingInfo:
    '''
    Simple container that associates a KPN channel with a capacity (number of
    tokens) and a communication primitve (defined by the platform)
    '''
    def __init__(self, kpnChannel, capacity, primitive):
        self.kpnChannel = kpnChannel
        self.capacity = capacity
        self.primitive = primitive


class ProcessMappingInfo:
    '''
    Simple container that associates a KPN process with a scheduler (defined by
    the platform) and the scheduling policy that the scheduler is supposed to
    use.
    '''
    def __init__(self, kpnProcess, scheduler, policy):
        self.kpnProcess = kpnProcess
        self.scheduler = scheduler
        self.policy = policy


class Mapping:
    '''
    Represents the mapping of a KPN graph to a platform. Contains a
    ProcessMappingInfo and ChannelMappingInfo object for each KPN process and
    channel in the graph.

    This is just a base class that does not provide any functionality for
    conveniently defining mappings.
    '''
    def __init__(self, kpn, platform):
        self.kpn = kpn
        self.platform = platform
        self.processMappings = []
        self.channelMappings = []


    # TODO: update to use new mapping structure
    def getProcess2PEDict(self):
        process2pe = dict()
        for sched in self.schedulers:
            assert len(sched.processorNames) == 1 , ("Schedule (" + str(sched) + ") does not have exactly one PE.")
            for process in sched.processNames:
                process2pe[process] = sched.processorNames[0]
        return process2pe


    # TODO: update to use new mapping structure
    def getChann2CPDict(self):
        chann2cp = dict()
        for chann in self.channels:
            chann2cp[chann.name] = (chann.viaMemory,chann.primitive)


    # TODO: update to use new mapping structure
    def toPyDot(self,kpn_graph,proc_labels=True,pe_labels=True,link_labels=False):
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
        for pnchannel in kpn_graph.channels:
            links_from[pnchannel.name] = []
            links_to[pnchannel.name] = []

        for proc in kpn_graph.processes:
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

    def outputDot(self,kpn_graph,filename,proc_labels=True,pe_labels=True,link_labels=False):
        self.toPyDot(kpn_graph,proc_labels=proc_labels,pe_labels=pe_labels,link_labels=link_labels).write_raw(filename)
