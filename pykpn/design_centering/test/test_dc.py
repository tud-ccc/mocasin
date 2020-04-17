# Copyright (C) 2019-2020 TU Dresden
# All Rights Reserved
#
# Author: Gerald Hempel

from unittest.mock import Mock

#imports to run DC
from pykpn.design_centering import DesignCentering
from pykpn.design_centering import volume
from pykpn.representations import representations as reps

def test_dc_holistic(monkeypatch, kpn, platform, conf, oracle):
   def mock_p_values():
       return [0.9, 0.9, 0.9, 0.9]

   def mock_adapt_poly():
       pass
   
   #Mapping
   representation_type = reps.RepresentationType['SimpleVector']
   print("--- Generate DC Test ---")
   representation = (representation_type.getClassType())(kpn, platform, conf)
   starting_center = representation.uniform()
   
   #print(oracle.validate_set())
   v = volume.LPVolume(starting_center, starting_center.get_numProcs(),kpn,platform,conf,representation_type)
   dc = DesignCentering(v, oracle, representation, conf)
   center,history = dc.ds_explore()
   #print("center: {} history: {}".format(center, history))


