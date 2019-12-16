# Copyright (C) 2017-2018 TU Dresden
# All Rights Reserved
#
# Authors: Christian Menard, Andres Goens


from pykpn.representations.representations import RepresentationType

from pykpn.util import logging
from pykpn.common.mapping import ChannelMappingInfo, Mapping, ProcessMappingInfo, SchedulerMappingInfo


log = logging.getLogger(__name__)


class RandomMapping(Mapping):
    """A random mapping

    When this class is initialized, it generates a random mapping for a given
    platform and kpn application. The random module is used for pseudo number
    generation. You can call ``random.seed(<...>)`` before instantiating this
    class in order to achieve reproducible results.

    The init function optionally takes another mapping and a radius. If given
    those, it will sample uniformly from the ball with this radius around the
    mapping. This will generate a mapping uniformly in the space of the
    representation of the given mapping. If no radius is given, but a
    mapping is, then an element will be selected uniformly in the representation
    of the given mapping. Note that this might be very inefficient.

    TODO: this has not been tested/implemented on all representations!!

    The implementation of this class is not perfect. Here is a list of known
    problems:

    * Does not select a scheduling policy parameter if it is required.
    * First maps a process to a scheduler and then selects the
      affinity. This way, processes are expected to be evenly distributed
      between schedulers and not between processors. It is likely that a
      processor with it's on scheduler receives more workload than a
      processor that shares the scheduler with other processors.
    * How to select channel bounds?
    """

    def __init__(self, kpn, platform,mapping=None,radius=float("inf"),representation_type=RepresentationType['SimpleVector']):
        """Generate a random mapping

        :param kpn: a kpn graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param mapping: A mapping (ball center)
        :type mapping: Mapping
        :param radius: The ball radius
        :type radius: float
        :param representation_type: A representation type
        :type platform: RepresentationType
        :raises: RuntimeError if the algorithm is not able to find a suitable
            channel mapping for a random process mapping.
        """

        log.debug('start random mapper for %s on %s', kpn.name, platform.name)
        representation = representation_type.getClassType()(kpn,platform)
        super().__init__(kpn,platform)
            
        #elem = None
        if(radius == float("inf")): #uniform
            elem = representation.uniform()
        else:
            elem = self._representation.uniformFromBall(mapping,radius)[0]
        print(elem.to_list())
        self.from_mapping(elem)
        
