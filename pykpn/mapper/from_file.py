# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens

import os
import pickle

from pykpn.util import logging
from pykpn.common.mapping import Mapping
log = logging.getLogger(__name__)


class FromFileMapper:
    """Generates a mapping from a pickled file.
    [At some point we should replace pickle with
    some mapping format of our own.]
    """

    def __init__(self, kpn, platform, trace, representation, file_path):
        """Generates a default mapping for a given platform and KPN application.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param trace: a trace generator
        :type trace: TraceGenerator
        :param representation: a mapping representation object
        :type representation: MappingRepresentation
        :param file_path: path to file to read
        :type file_path: os.PathLike
        """
        self.full_mapper = True
        try:
            with open(file_path,'rb') as f:
                p = pickle.Unpickler(f)
                mapping = p.load()
                assert isinstance(mapping,Mapping)
                self.mapping = mapping
        except IOError as e:
            log.error("Unable to read file.")
            raise e


        #check that mapping is valid
        kpn_names, platform_names = type(representation).gen_hash(kpn,platform)
        read_kpn_names, read_platform_names = type(representation).gen_hash(self.mapping.kpn, self.mapping.platform)
        if kpn_names != read_kpn_names:
            log.error("Mapping application does not match application")
            raise RuntimeError
        if platform_names != read_platform_names:
            log.error("Mapping platform does not match platform")
            raise RuntimeError

        #if mapping is valid, update objects in representation
        representation.platform = platform
        representation.kpn = kpn
        self.mapping.platform = platform
        self.mapping.update_kpn_object(kpn)


    def generate_mapping(self):
        """ Generates a mapping from the input list


        :param seed: initial seed for the random generator
        :type seed: integer
        :param part_mapping: partial mapping to start from
        """
        return self.mapping
