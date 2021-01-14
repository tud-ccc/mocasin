# Copyright (C) 2020 TU Dresden
# All Rights Reserved
#
# Authors: Andrés Goens

import pickle
from glob import glob

from mocasin.util import logging
from mocasin.common.mapping import Mapping
from mocasin.representations import MappingRepresentation

log = logging.getLogger(__name__)


class FromFileMapper:
    """Generates multiple mappings from a pickled files.
    [At some point we should replace pickle with
    some mapping format of our own.]
    """

    def __init__(self, kpn, platform, trace, representation, files_pattern):
        """Generates multiple mappings for a given platform and KPN application, reading from files.

        :param kpn: a KPN graph
        :type kpn: KpnGraph
        :param platform: a platform
        :type platform: Platform
        :param trace: a trace generator
        :type trace: TraceGenerator
        :param representation: a mapping representation object
        :type representation: MappingRepresentation
        :param files_pattern: pattern for finding files
        :type files_pattern: string
        """
        self.kpn = kpn
        self.platform = platform
        self.representation = representation
        self.mappings = []
        for file_path in glob(files_pattern):
            try:
                with open(file_path, "rb") as f:
                    p = pickle.Unpickler(f)
                    mapping = p.load()
                    assert isinstance(mapping, Mapping)
                    self.mappings.append(mapping)
            except IOError as e:
                log.error("Unable to read file.")
                raise e

        if len(self.mappings) == 0:
            log.error(
                f"Could not find any mappings matching pattern: '{files_pattern}'."
            )
            raise RuntimeError

    def generate_multiple_mappings(self):
        """Generates a list of mappings from the read files."""

        n = len(self.mappings)
        mappings = []
        for _ in range(n):
            mappings.append(self.generate_mapping())
        return mappings

    def generate_mapping(self):
        """Generates a single mapping from the list of read files."""

        # get next mapping
        try:
            mapping = self.mappings.pop()
        except IndexError:
            log.error("Trying to generate more mappings than files read.")
            raise RuntimeError
        # check that mapping is valid
        kpn_names, platform_names = MappingRepresentation.gen_hash(
            self.kpn, self.platform
        )
        read_kpn_names, read_platform_names = MappingRepresentation.gen_hash(
            mapping.kpn, mapping.platform
        )
        if kpn_names != read_kpn_names:
            log.error("Mapping application does not match application")
            raise RuntimeError
        if platform_names != read_platform_names:
            log.error("Mapping platform does not match platform")
            raise RuntimeError

        # if mapping is valid, update objects in representation
        mapping.platform = self.platform
        mapping.update_kpn_object(self.kpn)
        self.representation.platform = self.platform
        self.representation.kpn = self.kpn
        return mapping
