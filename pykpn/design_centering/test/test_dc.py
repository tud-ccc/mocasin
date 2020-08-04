# Copyright (C) 2019-2020 TU Dresden
# All Rights Reserved
#
# Author: Gerald Hempel

from unittest.mock import Mock

#imports to run DC
from pykpn.design_centering import DesignCenteringFromHydra, volume
from pykpn.representations import representations as reps

def test_dc_holistic(kpn, platform, conf, oracle):
    #Mapping
    representation_type = reps.RepresentationType['SimpleVector']
    print("--- Generate DC Test ---")
    representation = (representation_type.getClassType())(kpn, platform, conf)
    starting_center = representation.uniform()
   
    #print(oracle.validate_set())
    v = volume.LPVolume(starting_center, starting_center.get_numProcs(), kpn, platform, conf, representation_type)
    dc = DesignCenteringFromHydra(v, oracle, representation, conf)
    center, history = dc.ds_explore()
    #TODO: inserting some kind of assert statement? What is actually tested here?
