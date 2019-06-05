# Copyright (C) 2018-2019 TU Dresden
# All Rights Reserved
#
# Author: Andres Goens

from enum import Enum
from numpy.random import random_integers
import numpy as np

try:
    import pynauty as pynauty
except:
    pass

from pykpn.common.mapping import Mapping

from .metric_spaces import FiniteMetricSpace, FiniteMetricSpaceSym, FiniteMetricSpaceLP, FiniteMetricSpaceLPSym, arch_graph_to_distance_metric
from .embeddings import MetricSpaceEmbedding, DEFAULT_DISTORTION
import pykpn.representations.automorphisms as aut
import pykpn.representations.permutations as perm
import pykpn.util.random_distributions.lp as lp
from pykpn.util import logging
log = logging.getLogger(__name__)

class MappingRepresentation(type):
    """Metaclass managing the representation of mappings. 
       We want to have only one object representing the mapping space,
       even if we have different mappings in that representation. 
       Currently, only a single space will be allowed for all
       mappings of a single representation, so this metaclass essentially
       defines a Singleton for every representation type.
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        #print(str(cls) + " is being called")
        if cls not in cls._instances:
            cls._instances[cls] = super(MappingRepresentation,cls).__call__(*args, **kwargs)
            cls._instances[cls]._representationType = cls
        return cls._instances[cls]

def toRepresentation(representation,mapping): #this could also be in some base class?
  return representation.simpleVec2Elem(mapping.to_list())

def init_app_ncs(self,kpn):
    n = 0
    self._app_nc = {}
    self._app_nc_inv = {}
    for proc in self.kpn.processes():
        self._app_nc[n] = proc
        self._app_nc_inv[proc] = n

class SimpleVectorRepresentation(metaclass=MappingRepresentation):
    def __init__(self, kpn, platform):
        self.kpn = kpn
        self.platform = platform
    def uniform(self):
      Procs = list(self.kpn._processes.keys())
      PEs = list(self.platform._processors.keys())
      pe_mapping = list(random_integers(0,len(PEs)-1,size=len(Procs)))
      return self.randomPrimitives(pe_mapping)
    def randomPrimitives(self,pe_mapping):
      Procs = list(self.kpn._processes.keys())
      PEs = list(self.platform._processors.keys())
      CPs = list(self.platform._primitives.keys())
      res = pe_mapping[:len(Procs)]
      for c in self.kpn.channels():
        suitable_primitives = []
        for p in self.platform.primitives():
                    #assert: len([..]) list in next line == 1
          src_proc_idx = [i for i,x in enumerate(Procs) if x == c.source.name][0]
          src_pe_name = PEs[res[src_proc_idx]]
          src = self.platform.find_processor(src_pe_name)
          sink_procs_idxs = [i for i,x in enumerate(Procs) if x in [snk.name for snk in c.sinks]]
          try:
            sink_pe_names = [PEs[res[s]] for s in sink_procs_idxs]
          except:
            log.error(f"Invalid mapping: {res} \n PEs: {PEs},\n sink_procs_idxs: {sink_procs_idxs}\n")
          sinks = [self.platform.find_processor(snk) for snk in sink_pe_names]
          if p.is_suitable(src,sinks):
            suitable_primitives.append(p)
        primitive = suitable_primitives[random_integers(0,len(suitable_primitives)-1)].name
        primitive_idx = [i for i,x in enumerate(CPs) if x == primitive][0]
        res.append(primitive_idx)
      return res

    def simpleVec2Elem(self,x):
        return x
    def elem2SimpleVec(self,x):
        return x
    def uniformFromBall(self,p,r,npoints=1):
      Procs = list(self.kpn._processes.keys())
      PEs = list(self.platform._processors.keys())
      P = len(PEs)
      res = []
      def _round(point):
        #perodic boundary conditions
        return int(round(point) % P)
        #if point > P-1:
        #  return P-1
        #elif point < 0:
        #  return 0
        #else:
        
      for _ in range(npoints):
        v = list(map(_round,(np.array(p[:len(Procs)]) + np.array(r*lp.uniform_from_p_ball(p=1,n=len(Procs)))).tolist()))
        res.append(self.randomPrimitives(v))
      log.debug(f"unfiorm from ball: {res}")
      return res
      
class MetricSpaceRepresentation(FiniteMetricSpaceLP, metaclass=MappingRepresentation):
    def __init__(self,kpn, platform, p=1):
        self._topologyGraph = platform.to_adjacency_dict()
        M_list, self._arch_nc, self._arch_nc_inv = arch_graph_to_distance_metric(self._topologyGraph)
        M = FiniteMetricSpace(M_list)
        self.kpn = kpn
        self.platform = platform
        d = len(kpn.processes())
        init_app_ncs(self,kpn)
        super().__init__(M,d)
        
    def simpleVec2Elem(self,x): 
        return x

    def elem2SimpleVec(self,x):
        return x

class SymmetryRepresentation(metaclass=MappingRepresentation):
    def __init__(self,kpn, platform):
        self._topologyGraph = platform.to_adjacency_dict()
        self.kpn = kpn
        self.platform = platform
        self._d = len(kpn.processes())
        adjacency_dict, num_vertices, coloring, self._arch_nc = aut.to_labeled_edge_graph(self._topologyGraph)
        init_app_ncs(self,kpn)
        self._arch_nc_inv = {}
        for node in self._arch_nc:
            self._arch_nc_inv[self._arch_nc[node]] = node
        #TODO: ensure that nodes_correspondence fits simpleVec
            
        n = len(self.platform.processors())
        nautygraph = pynauty.Graph(num_vertices,True,adjacency_dict, coloring)
        autgrp_edges = pynauty.autgrp(nautygraph)
        autgrp, new_nodes_correspondence = aut.edge_to_node_autgrp(autgrp_edges[0],self._arch_nc)
        permutations_lists = map(aut.list_to_tuple_permutation,autgrp)
        permutations = [perm.Permutation(p,n= n) for p in permutations_lists]
        self._G = perm.PermutationGroup(permutations)
        
    def simpleVec2Elem(self,x): 
        return self._G.tuple_normalize(x[:self._d])
    def elem2SimpleVec(self,x):
        return x
    def uniform(self):
        procs_only = SimpleVectorRepresentation.uniform(self)[:self._d]
        return self._G.tuple_normalize(procs_only)
    def allEquivalent(self,x):
        orbit = self._G.tuple_orbit(x[:self._d])
        res = []
        for elem in orbit:
            mapping = Mapping(self.kpn, self.platform)
            mapping.from_list(list(elem))
            res.append(mapping)
        return res


#FIXME: UNTESTED!!
class MetricSymmetryRepresentation(FiniteMetricSpaceLPSym, metaclass=MappingRepresentation):
    def __init__(self,kpn, platform):
        self._topologyGraph = platform.to_adjacency_dict()
        self.kpn = kpn
        self.platform = platform
        self._d = len(kpn.processes())
        M_matrix, self._arch_nc, self._arch_nc_inv = arch_graph_to_distance_metric(self._topologyGraph)
        M = FiniteMetricSpace(M_matrix)
        adjacency_dict, num_vertices, coloring, self._arch_nc = aut.to_labeled_edge_graph(self._topologyGraph)
        init_app_ncs(self,kpn)
        self._arch_nc_inv = {}
        for node in self._arch_nc:
            self._arch_nc_inv[self._arch_nc[node]] = node
        #TODO: ensure that nodes_correspondence fits simpleVec
            
        n = len(self.platform.processors())
        nautygraph = pynauty.Graph(num_vertices,True,adjacency_dict, coloring)
        autgrp_edges = pynauty.autgrp(nautygraph)
        autgrp, new_nodes_correspondence = aut.edge_to_node_autgrp(autgrp_edges[0],self._arch_nc)
        permutations_lists = map(aut.list_to_tuple_permutation,autgrp)
        permutations = [perm.Permutation(p,n= n) for p in permutations_lists]
        self._G = perm.PermutationGroup(permutations)
        FiniteMetricSpaceLPSym.__init__(self,M,self._G,self._d)
        self.p = 1
        
        
    def simpleVec2Elem(self,x): 
        return x
    def elem2SimpleVec(self,x):
        return x
      



class MetricEmbeddingRepresentation(MetricSpaceEmbedding, metaclass=MappingRepresentation):
    def __init__(self,kpn, platform, distortion=DEFAULT_DISTORTION):
        self._topologyGraph = platform.to_adjacency_dict()
        M_matrix, self._arch_nc, self._arch_nc_inv = arch_graph_to_distance_metric(self._topologyGraph)
        self._M = FiniteMetricSpace(M_matrix)
        self.kpn = kpn
        self.platform = platform
        self._d = len(kpn.processes())
        self.p = 1
        init_app_ncs(self,kpn)
        MetricSpaceEmbedding.__init__(self,self._M,self._d,distortion)
        
    def simpleVec2Elem(self,x): 
        proc_vec = x[:self._d]
        return self.i(proc_vec)# [value for comp in self.i(x) for value in comp]

    def elem2SimpleVec(self,x):
        return self.invapprox(x)

    def uniform(self):
        return self.elem2SimpleVec(self.uniformVector())

    def uniformFromBall(self,p,r,npoints=1):
      log.debug(f"Uniform from ball with radius r={r} around point p={p}")
      point = self.simpleVec2Elem(p)
      return MetricSpaceEmbedding.uniformFromBall(self,point,r,npoints)
    
class SymmetryEmbeddingRepresentation(MetricSpaceEmbedding, metaclass=MappingRepresentation):
    def __init__(self,kpn, platform, distortion=DEFAULT_DISTORTION):
        self.kpn = kpn
        self.platform = platform
        self._d = len(kpn.processes())
        self._topologyGraph = platform.to_adjacency_dict()
        init_app_ncs(self,kpn)
        n = len(self.platform.processors())
        M_matrix, self._arch_nc, self._arch_nc_inv = arch_graph_to_distance_metric(self._topologyGraph)
        adjacency_dict, num_vertices, coloring, self._arch_nc = aut.to_labeled_edge_graph(self._topologyGraph)
        nautygraph = pynauty.Graph(num_vertices,True,adjacency_dict, coloring)
        autgrp_edges = pynauty.autgrp(nautygraph)
        autgrp, new_nodes_correspondence = aut.edge_to_node_autgrp(autgrp_edges[0],self._arch_nc)
        permutations_lists = map(aut.list_to_tuple_permutation,autgrp)
        permutations = [perm.Permutation(p,n= n) for p in permutations_lists]
        self._G = perm.PermutationGroup(permutations)
        M = FiniteMetricSpace(M_matrix)
        self._M = FiniteMetricSpaceLPSym(M,self._G,self._d)
        self._M._populateD()
        MetricSpaceEmbedding.__init__(self,self._M,1,distortion)
        
    def simpleVec2Elem(self,x): 
        proc_vec = x[:self._d]
        return self.i(proc_vec)# [value for comp in self.i(x) for value in comp]

    def elem2SimpleVec(self,x):
        return self.invapprox(x)

    def uniform(self):
        return self.uniformVector()
    
class RepresentationType(Enum):
    """Simple enum to store the different types of representations a mapping can have.
    """
    SimpleVector = SimpleVectorRepresentation
    FiniteMetricSpaceLP = FiniteMetricSpaceLP
    Symmetries = FiniteMetricSpaceSym
    FiniteMetricSpaceLPSym = FiniteMetricSpaceLPSym
    MetricSpaceEmbedding = MetricSpaceEmbedding
    SymmetryEmbedding = SymmetryEmbeddingRepresentation

    def getClassType(self):

        if self is RepresentationType['SimpleVector']:
            return SimpleVectorRepresentation
        if self is RepresentationType['FiniteMetricSpaceLP']:
            return MetricSpaceRepresentation
        if self is RepresentationType['Symmetries']:
            return SymmetryRepresentation
        if self is RepresentationType['FiniteMetricSpaceLPSym']:
            return MetricSymmetryRepresentation
        if self is RepresentationType['MetricSpaceEmbedding']:
            return MetricEmbeddingRepresentation
        if self is RepresentationType['SymmetryEmbedding']:
            return SymmetryEmbeddingRepresentation
