# Copyright (C) 2017 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


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
        '''
        Create an empty mapping.

        Derived classes should extend this function to actually define
        process and channel mappings.
        '''
        self.kpn = kpn
        self.platform = platform
        self.processMappings = []
        self.channelMappings = []

    def getSchedulerToProcessesDict(self):
        '''
        Returns a dictionary that associates scheduler names with a list of
        KPN processes.
        '''
        sched2proc = dict()

        # initialize with empty list
        for s in self.platform.schedulers:
            sched2proc[s.name] = []

        for pm in self.processMappings:
            sched2proc[pm.scheduler.name].append(pm.kpnProcess)

        return sched2proc

    def toPyDot(self, proc_labels=True, pe_labels=True, link_labels=False):
        '''
        Create a dot graph visualizing how the application is mapped to the
        platform

        :param proc_labels: print KPN process names
        :param pe_labels: print processor names
        :param link_labels: print KPN channel names
        :returns: pydot object
        '''
        sched2proc = self.getSchedulerToProcessesDict()
        cpn_graph = pydot.Dot(graph_type='digraph')

        for s in self.platform.schedulers:
            if len(s.processors) == 1:
                p_name = s.processors[0].name
                if pe_labels is True:
                    cluster = pydot.Cluster(p_name, label=p_name)
                else:
                    cluster = pydot.Cluster(p_name)

                for p in sched2proc[s.name]:
                    if proc_labels is True:
                        cluster.add_node(pydot.Node(p.name, label=p.name))
                    else:
                        cluster.add_node(pydot.Node(p.name, label=" "))
                cpn_graph.add_subgraph(cluster)
            else:
                raise RuntimeError('The scheduler ' + s.name + ' manages ' +
                                   'multiple processors. Visualization for ' +
                                   'that is not yet implemented!')

        # Create and add empty fifo channels for all the pn channels
        links_from = {}
        links_to = {}
        for pnchannel in self.kpn.channels:
            links_from[pnchannel.name] = []
            links_to[pnchannel.name] = []

        for proc in self.kpn.processes:
            for out_edge in proc.outgoing_channels:
                links_from[out_edge.name].append(proc.name)
            for in_edge in proc.incoming_channels:
                links_to[in_edge.name].append(proc.name)

        for link in links_from:
            edges = product(*[links_from[link], links_to[link]])
            for (v, w) in edges:
                if link_labels is True:
                    cpn_graph.add_edge(pydot.Edge(v, w, label=link))
                else:
                    cpn_graph.add_edge(pydot.Edge(v, w))

        return cpn_graph

    def outputDot(self, filename, proc_labels=True, pe_labels=True,
                  link_labels=False):
        '''
        Create a dot graph visualizing how the application is mapped to the
        platform and write it to file.

        :param filename: name of the output file
        :param proc_labels: print KPN process names
        :param pe_labels: print processor names
        :param link_labels: print KPN channel names
        '''
        self.toPyDot(proc_labels=proc_labels,
                     pe_labels=pe_labels,
                     link_labels=link_labels).write_raw(filename)
