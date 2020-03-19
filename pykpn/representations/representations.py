# Copyright (C) 2018-2019 TU Dresden
# All Rights Reserved
#
# Author: Andres Goens

from enum import Enum
import numpy as np
from numpy.random import randint

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
    
       This applies on a per kpn/platform combination basis.
       It means that if you have a different combination of kpn/platform,
       a new representation object will be initialized even if
       a representation of that type already exists.
    
       In general, representations work with mapping objects
       and can return something which corresponds to the
       type of the representation. However, it is also possible
       to work directly with simple vectors, if that is more efficient.
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        #print(str(cls) + " is being called")
        kpn = ";".join(map(lambda x : x.name, args[0].channels()))
        platform = args[1].name
        if (cls,kpn,platform) not in cls._instances:
            #make hashables of these two
            cls._instances[(cls,kpn,platform)] = super(MappingRepresentation,cls).__call__(*args, **kwargs)
            log.info(f"Initializing representation {cls} of kpn with processes: {kpn} on platform {platform}")
            cls._instances[(cls,kpn,platform)]._representationType = cls
        return cls._instances[(cls,kpn,platform)]

    def toRepresentation(self,mapping): 
        return self.simpleVec2Elem(mapping.to_list())

    def fromRepresentation(self,mapping): 
        log.error(f"Trying to transform to an unknown representation")
        return None

def init_app_ncs(self,kpn):
    n = 0
    self._app_nc = {}
    self._app_nc_inv = {}
    for proc in self.kpn.processes():
        self._app_nc[n] = proc
        self._app_nc_inv[proc] = n

class SimpleVectorRepresentation(metaclass=MappingRepresentation):
    """Simple Vector Representation:
    This representation treats mappings as vectors. The first dimensions (or components)
    of this vector represent the processes, and the values represent the PE where
    said processes are mapped. After the mapping of processes to PEs, the same
    method is applied to encode the channel to communication primitive mapping.
    This is only done if the channels variable is set when intializing the
    repreresentation object.
    
    A visualization of the encoding:
    [ P_1, P_2, ... , P_k, C_1, ..., C_l]
       ^ PE where           ^ Comm. prim.
         process 1            where chan. 1
         is mapped.           is mapped.
    

    Methods generally work with objects of the `pykpn.common.mapping.Mapping`
    class. Exceptions are the fromRepresentation method, which takes a vector
    and returns a Mapping object, and methods prefixed with an "_".
    Methods prefixed with "_", like _uniformFromBall generally work directly
    with the representation. Its usage is discouraged for having a standard
    interface, but they are provided in case they prove useful, when you know
    what you are doing.
    """
    def __init__(self, kpn, platform,config,channels=False):
        self.kpn = kpn
        self.platform = platform
        self.channels=channels
        self.config = config
        self.p = config['norm_p']
        self.num_procs = len(list(self.kpn._processes.keys()))
    def _uniform(self):
      Procs = sorted(list(self.kpn._processes.keys()))
      PEs = sorted(list(self.platform._processors.keys()))
      pe_mapping = list(randint(0,len(PEs),size=len(Procs)))
      return SimpleVectorRepresentation.randomPrimitives(self,pe_mapping)
    def randomPrimitives(self,pe_mapping):
      Procs = sorted(list(self.kpn._processes.keys()))
      PEs = sorted(list(self.platform._processors.keys()))
      CPs = sorted(list(self.platform._primitives.keys()))
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
        primitive = suitable_primitives[randint(0,len(suitable_primitives))].name
        primitive_idx = [i for i,x in enumerate(CPs) if x == primitive][0]
        res.append(primitive_idx)
      return res

    def uniform(self):
        return self.fromRepresentation(self._uniform())

    def toRepresentation(self,mapping):
        return mapping.to_list(channels=self.channels)

    def fromRepresentation(self,mapping):
        mapping_obj = Mapping(self.kpn,self.platform)
        mapping_obj.from_list(mapping)
        return mapping_obj

    def _simpleVec2Elem(self,x):
        if not self.channels:
            return x
        else:
            m = Mapping(self.kpn,self.platform)
            m.from_list(x)
            return m.to_list(channels=True)
        
    def _elem2SimpleVec(self,x):
        if self.channels:
            return x
        else:
            return x[:self.num_procs]

    def _uniformFromBall(self,p,r,npoints=1,simple=False):
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
          
        center = p[:len(Procs)]
        for _ in range(npoints):
            if simple:
                radius = _round(r/2)
                offset = []
                for _ in range(len(Procs)):
                    offset.append(randint(-radius,radius))

            else:
                offset = r * lp.uniform_from_p_ball(p=self.p,n=len(Procs))
            real_point = (np.array(center) + np.array(offset)).tolist() 
            v = list(map(_round,real_point))

            if self.channels:
                res.append(self.randomPrimitives(v))
            else:
                res.append(v)
        log.debug(f"uniform from ball: {res}")
        return res
      
    def uniformFromBall(self,p,r,npoints=1):
        return self.fromRepresentation(self._uniformFRomBall(p,r,npoints=npoints))

    def distance(self,x,y):
        a = np.array(x)
        b = np.array(y)
        return np.linalg.norm(a-b)

    def _distance(self,x,y):
        return self.distance(x,y)

    def approximate(self,x):
        approx = np.around(x)
        P = len(list(self.platform._processors.keys()))
        if self.config['periodic_boundary_conditions']:
            res = list(map(lambda t : t % P,approx))
        else:
            res = list(map(lambda t: max(0,min(t , P-1)), approx))
        return res


#FIXME: UNTESTED!!
class MetricSpaceRepresentation(FiniteMetricSpaceLP, metaclass=MappingRepresentation):
    """Metric Space Representation
    A representation for a generic metric space. Currently still untested and undocumented.
    It is recommended to use the Metri Space Embedding Representation instead, as it is more efficient,
    (slightly better) tested and documented.
    """

    def __init__(self,kpn, platform, cfg=None):
        self._topologyGraph = platform.to_adjacency_dict()
        M_list, self._arch_nc, self._arch_nc_inv = arch_graph_to_distance_metric(self._topologyGraph)
        M = FiniteMetricSpace(M_list)
        self.kpn = kpn
        self.platform = platform
        d = len(kpn.processes())
        init_app_ncs(self,kpn)
        super().__init__(M,d)
        
    def _simpleVec2Elem(self,x): 
        return x

    def _elem2SimpleVec(self,x):
        return x



class SymmetryRepresentation(metaclass=MappingRepresentation):
    """Symmetry Representation
    This representation considers the *archtiecture* symmetries for mappings.
    Application symmetries are still WIP. Mappings in this representation are
    vectors, too, just like in the Simple Vector Representation. The difference
    is that the vectors don't correspond to a single mapping, but to an equivalence
    class of mappings. Thus, two mappings that are equivalent through symmetries
    will yield the same vector in this representation. This unique vectors
    for each equivalent class are called "canonical mappings", because they 
    are canonical representatives of their orbit. Canonical mappings are the
    lexicographical lowest elements of the equivalence class.

    For example, if the PEs 0-3 are all equivalent, and PEs 4-7
    are also equivalent independently (as would be the case on
    an Exynos ARM big.LITTLE), these two mappings of 5 Processes
    are equivalent:
       [1,1,3,4,6] and [1,1,0,5,4]
    This representation would yield neither of them, as the
    following mapping is smaller lexicographically than both:
       [0,0,1,4,5]
    This is the canonical mapping of this orbit and what this representation would
    use to represent the class.

    This representation currently just supports global symmetries,
    partial symmetries are WIP.

    Methods generally work with objects of the `pykpn.common.mapping.Mapping`
    class. Exceptions are the fromRepresentation method, which takes a vector
    and returns a Mapping object, and methods prefixed with an "_".
    Methods prefixed with "_", like _allEquivalent generally work directly
    with the representation. 
    
    In order to work with other mappings in the same class, the methods
    allEquivalent/_allEquivalent returns for a mapping, all mappings in that class.
    """
    def __init__(self,kpn, platform,cfg=None):
        self._topologyGraph = platform.to_adjacency_dict()
        self.kpn = kpn
        self.platform = platform
        self._d = len(kpn.processes())
        adjacency_dict, num_vertices, coloring, self._arch_nc = aut.to_labeled_edge_graph(self._topologyGraph)
        init_app_ncs(self,kpn)
        self._arch_nc_inv = {}
        self.channels=False
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
        
    def _simpleVec2Elem(self,x): 
        return self._G.tuple_normalize(x[:self._d])
    def _elem2SimpleVec(self,x):
        return x

    def _uniform(self):
        procs_only = SimpleVectorRepresentation._uniform(self)[:self._d]
        return self._G.tuple_normalize(procs_only)

    def uniform(self):
        return self.fromRepresentation(self._uniform())

    def _allEquivalent(self,x):
        return self._G.tuple_orbit(x[:self._d])
    def allEquivalent(self,x):
        orbit = self._allEquivalent(x)
        res = []
        for elem in orbit:
            mapping = Mapping(self.kpn, self.platform)
            mapping.from_list(list(elem))
            res.append(mapping)
        return res

    def toRepresentation(self,mapping):
        return self._simpleVec2Elem(mapping.to_list(mapping))

    def fromRepresentation(self,mapping):
        #Does not check if canonical. This is deliberate.
        mapping_obj = Mapping(self.kpn,self.platform)
        mapping_obj.from_list(mapping)
        return mapping_obj

    def _uniformFromBall(self,p,r,npoints=1):
        return SimpleVectorRepresentation._uniformFromBall(self,p,r,npoints=npoints)

    def uniformFromBall(self,p,r,npoints=1):
        return self.fromRepresentation(self._uniformFRomBall(p,r,npoints=npoints))

    def distance(self,x,y):
        return SimpleVectorRepresentation.distance(self,x,y)

    def approximate(self,x):
        return SimpleVectorRepresentation.approximate(self,x)

#FIXME: UNTESTED!!
class MetricSymmetryRepresentation(FiniteMetricSpaceLPSym, metaclass=MappingRepresentation):
    """Metric Symmetry Representation
    A representation combining symmetries and a metric space. Currently still untested and undocumented.
    It is recommended to use the Symmetry Embedding Representation instead, as it is more efficient.
    """
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
        
        
    def _simpleVec2Elem(self,x): 
        return x
    def _elem2SimpleVec(self,x):
        return x
      



class MetricEmbeddingRepresentation(MetricSpaceEmbedding, metaclass=MappingRepresentation):
    """Metric Space Representation
    A representation for a metric space that uses an efficient embedding into a real space.
    Upon initialization, this representation calculates an embedding into a real space such
    that the distances in the metric space differ from the embedded distances by a factor of 
    at most `distortion`. 

    Elements in this representation are real vectors, the meaning of the components
    does not have a concrete interpretation. However, they do have a particular
    structure. For multiple processes, a single embedding for the archticeture is
    calculated. The multi-process vector space is the orthogonal sum of copies of a vector
    space emebedding for the single-process case. This provably preserves the distortion
    and makes calculations much more efficient.

    """
    def __init__(self,kpn, platform, cfg=None):
        if cfg is None:
            p = 2
            distortion = DEFAULT_DISTORTION
        else:
            p = cfg['norm_p']
            distortion = cfg['distortion']
        self._topologyGraph = platform.to_adjacency_dict()
        M_matrix, self._arch_nc, self._arch_nc_inv = arch_graph_to_distance_metric(self._topologyGraph)
        self._M = FiniteMetricSpace(M_matrix)
        self.kpn = kpn
        self.platform = platform
        self._d = len(kpn.processes())
        self.p = p
        init_app_ncs(self,kpn)
        if self.p != 2:
            log.warning(f"Metric space embeddings (currently) only supports p = 2. Embedding will not be low-distortion with regards to chosen p ({self.p})")
        MetricSpaceEmbedding.__init__(self,self._M,self._d,distortion)
        #Debug:
        #for p in self.iotainv.keys():
        #    for q in self.iotainv.keys():
        #        print(lp.p_norm(np.array(p)-np.array(q),self.p))
        #        print(self.M.D[self.iotainv[p],self.iotainv[q]])
        
    def _simpleVec2Elem(self,x): 
        proc_vec = x[:self._d]
        as_array = np.array(self.i(proc_vec)).flatten()# [value for comp in self.i(x) for value in comp]
        return as_array

    def _elem2SimpleVec(self,x):
        return self.inv(self.approx(x))

    def _uniform(self):
        res = np.array(self.uniformVector()).flatten()
        return res
    
    def uniform(self):
        return self.fromRepresentation(np.array(self.uniformVector()).flatten())

    def _uniformFromBall(self,p,r,npoints=1):
      log.debug(f"Uniform from ball with radius r={r} around point p={p}")
      #print(f"point of type {type(p)} and shape {p.shape}")
      point = []
      for i in range(self._d):
          val = []
          point.append(list(p)[self._k*i:self._k*(i+1)])
      results_raw = MetricSpaceEmbedding.uniformFromBall(self,point,r,npoints)
      results = list(map(lambda x : np.array(list(np.array(x).flat)),results_raw))
      #print(f"results uniform from ball: {results}")
      return results

    def uniformFromBall(self,p,r,npoints=1):
      log.debug(f"Uniform from ball with radius r={r} around point p={p}")
      point = self.toRepresentation(p)
      uniformpoints = MetricSpaceEmbedding.uniformFromBall(self,point,r,npoints)
      elements = map(self.fromRepresentation,uniformpoints)
      return list(elements) #Returns a list not map object. Do we want to change this?
  

    def toRepresentation(self,mapping):
        return self._simpleVec2Elem(mapping.to_list())

    def fromRepresentation(self,mapping):
        mapping_obj = Mapping(self.kpn,self.platform)
        mapping_obj.from_list(self._elem2SimpleVec(mapping))
        return mapping_obj

    def _distance(self,x,y):
        return lp.p_norm(x-y,self.p)

    def distance(self,x,y):
        return self._distance(x.to_list(),y.to_list())

    def approximate(self,x):
        return np.array(self.approx(x)).flatten()

class SymmetryEmbeddingRepresentation(MetricSpaceEmbedding, metaclass=MappingRepresentation):
    """Symmetry Embedding Representation
    A representation combining symmetries with an embedding of a metric space. Currently still work in progress
    and not ready for using.
    """
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
        
    def _simpleVec2Elem(self,x): 
        proc_vec = x[:self._d]
        return self.i(proc_vec)# [value for comp in self.i(x) for value in comp]

    def _elem2SimpleVec(self,x):
        return self.invapprox(x)

    def _uniform(self):
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
