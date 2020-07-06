# Copyright (C) 2019-2020 TU Dresden
# All Rights Reserved
#
# Authors: Felix Teweleit, Andrés Goens

import pytest
from pykpn.platforms import topologies as tp

class TestTopologies(object):
    
    def test_ringTopologyShort(self, peListShort):
        result = tp.ringTopology(peListShort)
        assert(result == {'PE00' : ['PE03', 'PE01'],
                          'PE01' : ['PE00', 'PE02'],
                          'PE02' : ['PE01', 'PE03'],
                          'PE03' : ['PE02', 'PE00']})
    
    def test_ringTopology(self, peList):
        result = tp.ringTopology(peList)
        assert(result == {'PE00' : ['PE09', 'PE01'],
                          'PE01' : ['PE00', 'PE02'],
                          'PE02' : ['PE01', 'PE03'],
                          'PE03' : ['PE02', 'PE04'],
                          'PE04' : ['PE03', 'PE05'],
                          'PE05' : ['PE04', 'PE06'],
                          'PE06' : ['PE05', 'PE07'],
                          'PE07' : ['PE06', 'PE08'],
                          'PE08' : ['PE07', 'PE09'],
                          'PE09' : ['PE08', 'PE00']})
        
    def test_ringTopologyLong(self, peListLong):
        result = tp.ringTopology(peListLong)
        assert(result == {'PE00' : ['PE19', 'PE01'],
                          'PE01' : ['PE00', 'PE02'],
                          'PE02' : ['PE01', 'PE03'],
                          'PE03' : ['PE02', 'PE04'],
                          'PE04' : ['PE03', 'PE05'],
                          'PE05' : ['PE04', 'PE06'],
                          'PE06' : ['PE05', 'PE07'],
                          'PE07' : ['PE06', 'PE08'],
                          'PE08' : ['PE07', 'PE09'],
                          'PE09' : ['PE08', 'PE10'],
                          'PE10' : ['PE09', 'PE11'],
                          'PE11' : ['PE10', 'PE12'],
                          'PE12' : ['PE11', 'PE13'],
                          'PE13' : ['PE12', 'PE14'],
                          'PE14' : ['PE13', 'PE15'],
                          'PE15' : ['PE14', 'PE16'],
                          'PE16' : ['PE15', 'PE17'],
                          'PE17' : ['PE16', 'PE18'],
                          'PE18' : ['PE17', 'PE19'],
                          'PE19' : ['PE18', 'PE00']})
        
    def test_fullyConnectedTopologyShort(self, peListShort):
        result = tp.fullyConnectedTopology(peListShort)
        assert(result == {'PE00' : ['PE01', 'PE02', 'PE03'],
                          'PE01' : ['PE00', 'PE02', 'PE03'],
                          'PE02' : ['PE00', 'PE01', 'PE03'],
                          'PE03' : ['PE00', 'PE01', 'PE02']})
    
    def test_fullyConnectedTopology(self, peList):
        result = tp.fullyConnectedTopology(peList)
        assert(result == {'PE00' : ['PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09'],
                          'PE01' : ['PE00', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09'],
                          'PE02' : ['PE00', 'PE01', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09'],
                          'PE03' : ['PE00', 'PE01', 'PE02', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09'],
                          'PE04' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09'],
                          'PE05' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE06', 'PE07', 'PE08', 'PE09'],
                          'PE06' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE07', 'PE08', 'PE09'],
                          'PE07' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE08', 'PE09'],
                          'PE08' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE09'],
                          'PE09' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08'] })
        
    def test_fullyConnectedTopologyLong(self, peListLong):
        result = tp.fullyConnectedTopology(peListLong)
        assert(result == {'PE00' : ['PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE01' : ['PE00', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE02' : ['PE00', 'PE01', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE03' : ['PE00', 'PE01', 'PE02', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE04' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE05' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE06' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE07' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE08' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE09' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE10' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09',
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE11' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE12' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE13' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE14' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE15', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE15' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE16', 'PE17', 'PE18', 'PE19'],
                        'PE16' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE17', 'PE18', 'PE19'],
                        'PE17' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE18', 'PE19'],
                        'PE18' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE19'],
                        'PE19' : ['PE00', 'PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09', 'PE10', 
                                    'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PE16', 'PE17', 'PE18'] })

    def test_meshTopology(self, peListNineElems):
        result = tp.meshTopology(peListNineElems)
        expected = {'PE00': ['PE01', 'PE03'],
                    'PE01': ['PE00', 'PE02', 'PE04'],
                    'PE02': ['PE01', 'PE05'],
                    'PE03': ['PE00', 'PE04', 'PE06'],
                    'PE04': ['PE01', 'PE03', 'PE05', 'PE07'],
                    'PE05': ['PE02', 'PE04', 'PE08'],
                    'PE06': ['PE03', 'PE07'],
                    'PE07': ['PE04', 'PE06', 'PE08'],
                    'PE08': ['PE05','PE07']}
        assert sorted(list(result.keys())) == sorted(list(expected.keys()))
        for PE in result:
            assert sorted(result[PE]) == expected[PE]

    def test_starTopology(self, peList):
        result = tp.starTopology(peList)
        expected = {'PE00' : ['PE01', 'PE02', 'PE03', 'PE04', 'PE05', 'PE06', 'PE07', 'PE08', 'PE09'],
                    'PE01' : ['PE00'],
                    'PE02' : ['PE00'],
                    'PE03' : ['PE00'],
                    'PE04' : ['PE00'],
                    'PE05' : ['PE00'],
                    'PE06' : ['PE00'],
                    'PE07' : ['PE00'],
                    'PE08' : ['PE00'],
                    'PE09' : ['PE00'] }
        assert sorted(list(result.keys())) == sorted(list(expected.keys()))
        for PE in result:
            assert sorted(result[PE]) == expected[PE]

    def test_torusTopologyShort(self, peListShort):
        result = tp.torusTopology(peListShort)
        assert(result == {'PE00' : ['PE03', 'PE01'],
                          'PE01' : ['PE00', 'PE02'],
                          'PE02' : ['PE01', 'PE03'],
                          'PE03' : ['PE02', 'PE00']})
        
    def test_torusTopology(self, peListTorus):
        result = tp.torusTopology(peListTorus)
        assert(result == { 'PE00' : ['PE03', 'PE01', 'PE12', 'PE04'],
                          'PE01' : ['PE00', 'PE02', 'PE13', 'PE05'],
                          'PE02' : ['PE01', 'PE03', 'PE14', 'PE06'],
                          'PE03' : ['PE02', 'PE00', 'PE15', 'PE07'],
                          'PE04' : ['PE07', 'PE05', 'PE00', 'PE08'],
                          'PE05' : ['PE04', 'PE06', 'PE01', 'PE09'],
                          'PE06' : ['PE05', 'PE07', 'PE02', 'PE10'],
                          'PE07' : ['PE06', 'PE04', 'PE03', 'PE11'],
                          'PE08' : ['PE11', 'PE09', 'PE04', 'PE12'],
                          'PE09' : ['PE08', 'PE10', 'PE05', 'PE13'],
                          'PE10' : ['PE09', 'PE11', 'PE06', 'PE14'],
                          'PE11' : ['PE10', 'PE08', 'PE07', 'PE15'],
                          'PE12' : ['PE15', 'PE13', 'PE08', 'PE00'],
                          'PE13' : ['PE12', 'PE14', 'PE09', 'PE01'],
                          'PE14' : ['PE13', 'PE15', 'PE10', 'PE02'],
                          'PE15' : ['PE14', 'PE12', 'PE11', 'PE03'] })
        
    def test_torusTopologyError(self, peListLong):
        with pytest.raises(RuntimeError, match=r"You need a square number amount of elements for a torus topology!"):
            tp.torusTopology(peListLong)
        
        