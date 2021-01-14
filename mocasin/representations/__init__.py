# Copyright (C) 2018-2020 TU Dresden
# All Rights Reserved
#
# Author: Andres Goens

import numpy as np
from numpy.random import randint
from copy import copy
import random
import timeit
from os.path import exists

try:
    import pynauty as pynauty
except ModuleNotFoundError:
    pass

try:
    import pympsym
except ModuleNotFoundError:
    pass


from mocasin.mapper.partial import ProcPartialMapper, ComFullMapper

from .metric_spaces import FiniteMetricSpace, FiniteMetricSpaceSym, FiniteMetricSpaceLP, FiniteMetricSpaceLPSym, arch_to_distance_metric
from .embeddings import MetricSpaceEmbedding
from .automorphisms import to_labeled_edge_graph, edge_to_node_autgrp, list_to_tuple_permutation
from .permutations import Permutation, PermutationGroup
import mocasin.util.random_distributions.lp as lp
from mocasin.util import logging
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

       A representation has to implement a function `changed_parameters`
       that checks if the representation-specific parameters are different
       (takes the same parameters in the same order as the init function,
       except for the application and platform)

       In general, representations work with mapping objects
       and can return something which corresponds to the
       type of the representation. However, it is also possible
       to work directly with simple vectors, if that is more efficient.
    """
    _instances = {}

    @staticmethod
    def gen_hash(kpn,platform):
        kpn_names = ";".join(map(lambda x : x.name, kpn.channels()))
        platform_names = ";".join(map(lambda x : x.name, platform.processors()))
        return kpn_names,platform_names

    def __call__(cls, *args, **kwargs):
        time = timeit.default_timer()
        kpn = args[0]
        platform = args[1]
        kpn_names, platform_names = MappingRepresentation.gen_hash(kpn, platform)

        if (cls, kpn, platform) in cls._instances:
            different = cls._instances[(cls, kpn, platform)].changed_parameters(*args[2:])

        if (cls, kpn, platform) not in cls._instances or different:
            #make hashables of these two
            cls._instances[(cls, kpn_names, platform_names)] = super(MappingRepresentation, cls).__call__(*args, **kwargs)
            log.info(f"Initializing representation {cls} of kpn with processes: {kpn_names} on platform with cores {platform_names}")

        instance = copy(cls._instances[(cls,kpn_names,platform_names)])
        instance.kpn = kpn
        instance.platform = platform
        com_mapper = ComFullMapper(kpn,platform)
        instance.list_mapper = ProcPartialMapper(kpn,platform,com_mapper)
        instance.init_time = timeit.default_timer() - time
        return instance

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


    Methods generally work with objects of the `mocasin.common.mapping.Mapping`
    class. Exceptions are the fromRepresentation method, which takes a vector
    and returns a Mapping object, and methods prefixed with an "_".
    Methods prefixed with "_", like _uniformFromBall generally work directly
    with the representation. Its usage is discouraged for having a standard
    interface, but they are provided in case they prove useful, when you know
    what you are doing.
    """
    def __init__(self, kpn, platform,channels=False,periodic_boundary_conditions=False,norm_p=2):
        self.kpn = kpn
        self.platform = platform
        self.channels = channels
        self.boundary_conditions = periodic_boundary_conditions
        self.p = norm_p
        self.num_procs = len(list(self.kpn._processes.keys()))
        com_mapper = ComFullMapper(kpn,platform)
        self.list_mapper = ProcPartialMapper(kpn,platform,com_mapper)

    def changed_parameters(self,channels,periodic_boundary_conditions,norm_p):
        return self.channels != channels or self.boundary_conditions != periodic_boundary_conditions or self.p != norm_p

    def _uniform(self):
        Procs = sorted(list(self.kpn._processes.keys()))
        PEs = sorted(list(self.platform._processors.keys()))
        pe_mapping = list(randint(0,len(PEs),size=len(Procs)))
        if self.channels:
            return SimpleVectorRepresentation.randomPrimitives(self,pe_mapping)
        else:
            return pe_mapping

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
        if type(mapping) == np.ndarray:
            mapping = mapping.astype(int)
        mapping_obj = self.list_mapper.generate_mapping(mapping)
        return mapping_obj

    def _simpleVec2Elem(self,x):
        if not self.channels:
            return x
        else:
            m = self.list_mapper.generate_mapping(x)
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
            rounded = int(round(point) % P)
            if self.boundary_conditions:
                return rounded
            else:
                if point > P-1:
                    return P-1
                elif point < 0:
                    return 0
                else:
                    return rounded

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
        return self.fromRepresentation(self._uniformFromBall(p,r,npoints=npoints))

    def distance(self,x,y):
        a = np.array(x)
        b = np.array(y)
        return np.linalg.norm(a-b)

    def _distance(self,x,y):
        return self.distance(x,y)

    def approximate(self,x):
        approx = np.rint(x).astype(int)
        P = len(list(self.platform._processors.keys()))
        if self.boundary_conditions:
            res = list(map(lambda t : t % P,approx))
        else:
            res = list(map(lambda t: max(0,min(t , P-1)), approx))
        return res

    def crossover(self,m1,m2,k):
        return self._crossover(self.toRepresentation(m1),self.toRepresentation(m2),k)

    def _crossover(self,m1,m2,k):
        assert len(m1) == len(m2)
        crossover_points = random.sample(range(len(m1)),k)
        swap = False
        for i in range(len(m1)):
            if i in crossover_points:
                swap = not swap
            if swap:
                m1[i] = m2[i]
                m2[i] = m2[i]
        log.debug(f"crossover: {m1},{m2}")

        return m1,m2


#FIXME: UNTESTED!!
class MetricSpaceRepresentation(FiniteMetricSpaceLP, metaclass=MappingRepresentation):
    """Metric Space Representation
    A representation for a generic metric space. Currently still untested and undocumented.
    It is recommended to use the Metri Space Embedding Representation instead, as it is more efficient,
    (slightly better) tested and documented.
    """

    def __init__(self,kpn, platform):
        raise RuntimeError("represetation not properly implemented")
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

    Methods generally work with objects of the `mocasin.common.mapping.Mapping`
    class. Exceptions are the fromRepresentation method, which takes a vector
    and returns a Mapping object, and methods prefixed with an "_".
    Methods prefixed with "_", like _allEquivalent generally work directly
    with the representation.

    In order to work with other mappings in the same class, the methods
    allEquivalent/_allEquivalent returns for a mapping, all mappings in that class.
    """
    def __init__(self,kpn, platform,channels=False,periodic_boundary_conditions=False,norm_p=2,canonical_operations=True,disable_mpsym=False):
        self._topologyGraph = platform.to_adjacency_dict()
        self.kpn = kpn
        self.platform = platform
        self._d = len(kpn.processes())
        init_app_ncs(self,kpn)
        self._arch_nc_inv = {}
        self.channels=channels
        self.boundary_conditions = periodic_boundary_conditions
        self.p = norm_p
        com_mapper = ComFullMapper(kpn,platform)
        self.list_mapper = ProcPartialMapper(kpn,platform,com_mapper)
        self.canonical_operations = canonical_operations


        n = len(self.platform.processors())

        if disable_mpsym:
            self.sym_library = False
        else:
            try:
                pympsym
            except NameError:
                self.sym_library = False
            else:
                self.sym_library = True
                if hasattr(platform, 'ag'):
                    self._ag = platform.ag
                    log.info("Symmetries initialized with mpsym: Platform Generator.")
                elif hasattr(platform,'ag_json') and exists(platform.ag_json):
                    #todo: make sure the correspondence of cores is correct!
                    self._ag = pympsym.ArchGraphSystem.from_json_file(platform.ag_json)
                    log.info("Symmetries initialized with mpsym: JSON file.")

                else:
                    #only calculate this if not already present
                    log.info("No pre-comupted mpsym symmetry group available. Initalizing architecture graph...")
                    adjacency_dict, num_vertices, coloring, self._arch_nc = to_labeled_edge_graph(self._topologyGraph)
                    nautygraph = pynauty.Graph(num_vertices, True, adjacency_dict, coloring)
                    log.info("Architecture graph initialized. Calculating automorphism group using Nauty...")
                    autgrp_edges = pynauty.autgrp(nautygraph)
                    autgrp, _ = edge_to_node_autgrp(autgrp_edges[0], self._arch_nc)
                    self._ag = pympsym.ArchGraphAutomorphisms([pympsym.Perm(g) for g in autgrp])
                    for node in self._arch_nc:
                        self._arch_nc_inv[self._arch_nc[node]] = node
                        #TODO: ensure that nodes_correspondence fits simpleVec

        if not self.sym_library:
            log.info("Using python symmetries: Initalizing architecture graph...")
            adjacency_dict, num_vertices, coloring, self._arch_nc = to_labeled_edge_graph(self._topologyGraph)
            nautygraph = pynauty.Graph(num_vertices, True, adjacency_dict, coloring)
            log.info("Architecture graph initialized. Calculating automorphism group using Nauty...")
            autgrp_edges = pynauty.autgrp(nautygraph)
            autgrp, _ = edge_to_node_autgrp(autgrp_edges[0], self._arch_nc)
            permutations_lists = map(list_to_tuple_permutation,autgrp)
            permutations = [Permutation(p,n=n) for p in permutations_lists]
            self._G = PermutationGroup(permutations)
            log.info("Initialized automorphism group with internal symmetries")

    def _simpleVec2Elem(self,x):
        x_ = x[:self._d]
        _x = x[self._d:] #keep channels if exist (they should be mapped accordingly...)
        if self.sym_library:
            return list(self._ag.representative(x_)) + _x
        else:
            return self._G.tuple_normalize(x_) + _x

    def changed_parameters(self):
        return False

    def _elem2SimpleVec(self,x):
        return x

    def _uniform(self):
        procs_only = SimpleVectorRepresentation._uniform(self)[:self._d]
        if self.sym_library:
            return self._ag.representative(procs_only)
        else:
            return self._G.tuple_normalize(procs_only)

    def uniform(self):
        return self.fromRepresentation(self._uniform())

    def _allEquivalent(self,x):
        x_ = x[:self._d]
        if self.sym_library:
            return frozenset([tuple(p) for p in self._ag.orbit(x_)])
        else:
            return self._G.tuple_orbit(x_)

    def allEquivalent(self,x):
        x_ = x.to_list(channels=False)
        orbit = self._allEquivalent(x_)
        res = []
        for elem in orbit:
            mapping = self.list_mapper.generate_mapping(list(elem))
            if hasattr(x,"metadata"):
                mapping.metadata  = copy(x.metadata)
            res.append(mapping)
        return res

    def toRepresentation(self,mapping):
        return self._simpleVec2Elem(mapping.to_list(channels=self.channels))

    def toRepresentationNoncanonical(self,mapping):
        return SimpleVectorRepresentation.toRepresentation(self,mapping)

    def fromRepresentation(self,mapping):
        #Does not check if canonical. This is deliberate.
        mapping_obj = self.list_mapper.generate_mapping(mapping)
        return mapping_obj

    def _uniformFromBall(self,p,r,npoints=1):
        return SimpleVectorRepresentation._uniformFromBall(self,p,r,npoints=npoints)

    def uniformFromBall(self,p,r,npoints=1):
        return self.fromRepresentation(self._uniformFromBall(p,r,npoints=npoints))

    def distance(self,x,y):
        if self.canonical_operations:
            return SimpleVectorRepresentation.distance(self, self.toRepresentation(x), self.toRepresentation(y))
        else:
            xsv = SimpleVectorRepresentation.toRepresentation(self,x)
            ysv = SimpleVectorRepresentation.toRepresentation(self,y)
            return SimpleVectorRepresentation.distance(self,xsv,ysv)

    def crossover(self,m1,m2,k):
        if self.canonical_operations:
            return SimpleVectorRepresentation._crossover(self,self.toRepresentation(m1),self.toRepresentation(m2),k)
        else:
            xsv = SimpleVectorRepresentation.toRepresentation(self,m1)
            ysv = SimpleVectorRepresentation.toRepresentation(self,m2)
            return SimpleVectorRepresentation._crossover(self,xsv,ysv,k)

    def _crossover(self,x,y,k):
        if self.canonical_operations:
            xcan = self._simpleVec2Elem(x)
            ycan = self._simpleVec2Elem(y)
            xcx,ycx = SimpleVectorRepresentation._crossover(self,xcan,ycan,k)
            #update manually so that we return DEAP Individuals in DEAP
            for i in range(len(x)):
                x[i] = xcx[i]
                y[i] = ycx[i]
            return x,y
        else:
            return SimpleVectorRepresentation._crossover(self,x,y,k)

    def approximate(self,x):
        approx = SimpleVectorRepresentation.approximate(self,x)
        return self._simpleVec2Elem(approx)

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
        adjacency_dict, num_vertices, coloring, self._arch_nc = to_labeled_edge_graph(self._topologyGraph)
        init_app_ncs(self,kpn)
        self._arch_nc_inv = {}
        for node in self._arch_nc:
            self._arch_nc_inv[self._arch_nc[node]] = node
        #TODO: ensure that nodes_correspondence fits simpleVec

        n = len(self.platform.processors())
        nautygraph = pynauty.Graph(num_vertices,True,adjacency_dict, coloring)
        autgrp_edges = pynauty.autgrp(nautygraph)
        autgrp, new_nodes_correspondence = edge_to_node_autgrp(autgrp_edges[0],self._arch_nc)
        permutations_lists = map(list_to_tuple_permutation,autgrp)
        permutations = [Permutation(p,n= n) for p in permutations_lists]
        self._G = PermutationGroup(permutations)
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
    structure. For multiple processes, a single embedding for the architecture is
    calculated. The multi-process vector space is the orthogonal sum of copies of a vector
    space emebedding for the single-process case. This provably preserves the distortion
    and makes calculations much more efficient.

    The additional option, extra_dims, adds additional dimensions for each PE to count
    when multiple processes are mapped to the same PE. The scaling factor for those extra
    dimensions is controlled by the value of extra_dims_factor.

    """
    def __init__(self,kpn, platform, norm_p,extra_dimensions=True,
                 extra_dimensions_factor=3,ignore_channels=True,
                 target_distortion=1.1,jlt_tries=10,
                 verbose=False):
        # todo: make sure the correspondence of cores is correct!
        M_matrix, self._arch_nc, self._arch_nc_inv = \
            arch_to_distance_metric(platform,heterogeneity=extra_dimensions)
        self._M = FiniteMetricSpace(M_matrix)
        self.kpn = kpn
        self.platform = platform
        self.extra_dims = extra_dimensions
        self.jlt_tries = jlt_tries
        self.target_distortion = target_distortion
        self.ignore_channels = ignore_channels
        self.verbose = verbose
        if hasattr(platform, 'embedding_json'):
            self.embedding_matrix_path = platform.embedding_json
        else:
            self.embedding_matrix_path = None

        if not self.ignore_channels:
            log.warning("Not ignoring channels might lead"
                        " to invalid mappings when approximating.")
        self.extra_dims_factor = extra_dimensions_factor
        self._d = len(kpn.processes())
        if self.extra_dims:
            self._split_d = self._d
            self._split_k = len(platform.processors())
            self._d += len(kpn.channels())
        self.p = norm_p
        com_mapper = ComFullMapper(kpn,platform)
        self.list_mapper = ProcPartialMapper(kpn,platform,com_mapper)
        init_app_ncs(self,kpn)
        if self.p != 2:
            log.error(f"Metric space embeddings only supports p = 2."
                      f" For p = 1, for example, finding such an embedding"
                      f" is NP-hard (See Matousek, J.,  Lectures on Discrete"
                      f" Geometry, Chap. 15.5)")
        MetricSpaceEmbedding.\
            __init__(self,self._M,self._d, jlt_tries=self.jlt_tries,
                     embedding_matrix_path = self.embedding_matrix_path,
                     target_distortion=self.target_distortion, verbose=verbose)
        log.info(f"Found embedding with distortion: {self.distortion}")

    def changed_parameters(self,norm_p):
        return self.p != norm_p

    def _simpleVec2Elem(self,x):
        proc_vec = x[:self._d]
        as_array = np.array(self.i(proc_vec)).flatten()
        #[value for comp in self.i(x) for value in comp]

        return as_array

    def _elem2SimpleVec(self,x):
        return self.inv(self.approx(x[:(self._k*self._d)]).tolist())

    def _uniform(self):
        res = np.array(self.uniformVector()).flatten()
        return res

    def uniform(self):
        return self.fromRepresentation(np.array(self.uniformVector()).flatten())

    def _uniformFromBall(self,p,r,npoints=1):
        log.debug(f"Uniform from ball with radius r={r} around point p={p}")
        #print(f"point of type {type(p)} and shape {p.shape}")
        point = np.array(p).flatten()
        results_raw = MetricSpaceEmbedding.uniformFromBall(self,point,r,npoints)
        results = list(map(lambda x : np.array(list(np.array(x).flat)),results_raw))
        if self.extra_dims:
            results = list(map(lambda x : self._simpleVec2Elem(self._elem2SimpleVec(x)),results))

        #print(f"results uniform from ball: {results}")
        return results

    def uniformFromBall(self,p,r,npoints=1):
        log.debug(f"Uniform from ball with radius r={r} around point p={p}")
        point = self.toRepresentation(p)
        uniformpoints = MetricSpaceEmbedding.uniformFromBall(self,point,r,npoints)
        elements = map(self.fromRepresentation,uniformpoints)
        return list(elements) #Returns a list not map object. Do we want to change this?


    def toRepresentation(self,mapping):
        return self._simpleVec2Elem(mapping.to_list(channels=self.extra_dims))

    def fromRepresentation(self,mapping):
        simple_vec = self._elem2SimpleVec(mapping)
        if self.ignore_channels:
            simple_vec = simple_vec[:self._split_d]
        mapping_obj = self.list_mapper.generate_mapping(simple_vec)
        return mapping_obj

    def _distance(self,x,y):
        return lp.p_norm(x-y,self.p)

    def distance(self,x,y):
        return self._distance(self.toRepresentation(x),self.toRepresentation(y))

    def approximate(self,x):
        res = np.array(self.approx(x[:(self._d*self._k)])).flatten()
        return res

    def crossover(self, m1, m2, k):
        return self._crossover(self.toRepresentation(m1), self.toRepresentation(m2), k)

    def _crossover(self, m1, m2, k):
        assert len(m1) == len(m2)
        crossover_points = np.array(random.sample(range(self._d), k)) * self._k
        swap = False
        for i in range(len(m1)):
            if i in crossover_points:
                swap = not swap
            if swap:
                m1[i] = m2[i]
                m2[i] = m2[i]
        return m1, m2


class SymmetryEmbeddingRepresentation(MetricSpaceEmbedding, metaclass=MappingRepresentation):
    """Symmetry Embedding Representation
    A representation combining symmetries with an embedding of a metric space.
    The mapping is first normalized using symmetries and then converted with the embedding.
    """
    def __init__(self, kpn, platform, norm_p, verbose=False,
                 periodic_boundary_conditions=False, jlt_tries=10,
                 extra_dimensions=True, extra_dimensions_factor=3,
                 ignore_channels=True, target_distortion=1.1,
                 canonical_operations=True, disable_mpsym=False):

        self.sym =\
            SymmetryRepresentation(kpn,platform,channels=extra_dimensions,
                                   norm_p=norm_p, disable_mpsym=disable_mpsym,
                                   periodic_boundary_conditions = periodic_boundary_conditions,
                                   canonical_operations=canonical_operations)
        self.emb =\
            MetricEmbeddingRepresentation(kpn,platform,norm_p,verbose=verbose,
                                          extra_dimensions=extra_dimensions,
                                          extra_dimensions_factor=extra_dimensions_factor,
                                          target_distortion=target_distortion,
                                          jlt_tries=jlt_tries,ignore_channels=ignore_channels)
        self.canonical_operations = canonical_operations
        log.warning("The SymmetryEmbedding representation is not well-tested yet."
                    " In particular, it currently ignores the symmetries of the channels,"
                    "which should not be very problematic, however.")

    def _simpleVec2Elem(self,x):
        canonical = self.sym._simpleVec2Elem(x)
        return self.emb._simpleVec2Elem(canonical)

    def _elem2SimpleVec(self,x):
        return self.emb._elem2SimpleVec(x)

    def _uniform(self):
        return self.emb._uniform()

    def uniformFromBall(self,p,r,npoints=1):
        return self.emb.uniformFromBall(p,r,npoints=npoints)

    def _uniformFromBall(self,p,r,npoints=1):
        return self.emb._uniformFromBall(p,r,npoints=npoints)

    def changed_parameters(self,norm_p):
        return self.emb.changed_parameters(norm_p) or\
               self.sym.changed_parameters()

    def toRepresentation(self,mapping):
        canonical = self.sym.toRepresentation(mapping)
        return self._simpleVec2Elem(canonical)

    def toRepresentationNoncanonical(self,mapping):
        return self.emb.toRepresentation(mapping)

    def fromRepresentation(self,mapping):
        return self.emb.fromRepresentation(mapping)

    def _distance(self,x,y):
        return lp.p_norm(x-y,self.p)

    def distance(self,x,y):
        return self._distance(self.toRepresenatation(x),self.toRepresentation(y))

    def approximate(self,x):
        res = self.emb._elem2SimpleVec(self.emb.approximate(x))
        can = self.sym._simpleVec2Elem(res)
        return self.emb._simpleVec2Elem(can)

    def crossover(self, m1, m2, k):
        return self.approximate(self.emb._crossover(self.toRepresentation(m1), self.toRepresentation(m2), k))

    def _crossover(self, m1, m2, k):
        return self.emb._crossover(m1,m2,k)