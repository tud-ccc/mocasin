# Copyright (C) 2019 TU Dresden
# Licensed under the ISC license (see LICENSE.txt)
#
# Author: Gerald Hempel

from mocasin.representations import SimpleVectorRepresentation

# imports to run DC
from mocasin.design_centering import DesignCentering, volume
from mocasin.design_centering.sample import MetricSpaceSampleGen


def test_dc_holistic(graph, platform, conf, oracle):
    # Mapping
    print("--- Generate DC Test ---")
    representation = SimpleVectorRepresentation(graph, platform)
    starting_center = representation.uniform()

    # print(oracle.validate_set())
    v = volume.LPVolume(
        graph, platform, representation, starting_center, radius=2.0
    )
    sg = MetricSpaceSampleGen(representation)
    dc = DesignCentering(v, oracle, sg, representation)
    center, history = dc.ds_explore()
    # TODO: inserting some kind of assert statement? What is actually tested here?
