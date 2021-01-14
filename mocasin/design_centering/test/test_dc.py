# Copyright (C) 2019-2020 TU Dresden
# All Rights Reserved
#
# Author: Gerald Hempel

from mocasin.representations import SimpleVectorRepresentation

# imports to run DC
from mocasin.design_centering import DesignCentering, volume
from mocasin.design_centering.sample import MetricSpaceSampleGen


def test_dc_holistic(kpn, platform, conf, oracle):
    # Mapping
    print("--- Generate DC Test ---")
    representation = SimpleVectorRepresentation(kpn, platform)
    starting_center = representation.uniform()

    # print(oracle.validate_set())
    v = volume.LPVolume(
        kpn, platform, representation, starting_center, radius=2.0
    )
    sg = MetricSpaceSampleGen(representation)
    dc = DesignCentering(v, oracle, sg, representation)
    center, history = dc.ds_explore()
    # TODO: inserting some kind of assert statement? What is actually tested here?
