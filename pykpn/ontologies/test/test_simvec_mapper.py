#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

from arpeggio import visit_parse_tree
from pykpn.ontologies.logicLanguage import Grammar, SemanticAnalysis

class TestSimvecMapper(object):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
        
    def testMappingGeneration1(self, solver):
        inputQuery = "EXISTS src MAPPED ARM00 AND fft_l MAPPED ARM01"
        result = [0, 1, 0, 0, 0, 0, 0, 0]
        assert(solver.request(inputQuery).to_list() == result)
        
    def testMappingGeneration2(self, solver):
        inputQuery = "EXISTS src MAPPED ARM00 AND fft_l MAPPED ARM01 AND sink MAPPED ARM02"
        result = [0, 1, 0, 0, 0, 0, 0, 2]
        assert(solver.request(inputQuery).to_list() == result)
        
    def testMappingGeneration3(self, solver):
        inputQuery = "EXISTS src MAPPED ARM03 AND fft_l MAPPED ARM04 AND RUNNING TOGETHER [src, filter_l ]"
        result = [3, 4, 3, 0, 0, 0, 0, 0]
        assert(solver.request(inputQuery).to_list() == result)
        
    def testMappingGeneration4(self, solver):
        inputQuery = "EXISTS src MAPPED ARM03 AND ARM05 PROCESSING AND ARM06 PROCESSING"
        result = solver.request(inputQuery).to_list()
        assert(result[0] == 3)
        assert(result.count(5) >= 1)
        assert(result.count(6) >= 1)
        
    def testMappingGeneration5(self, mapDictSolver):
        #identifier and corresponding mapping are provided by conftest
        inputQuery = "EXISTS RUNNING TOGETHER [src, fft_l, fft_r, filter_l, filter_r, ifft_l, ifft_r, sink ] AND EQUALS map_two"
        result = mapDictSolver.request(inputQuery).to_list()
        assert(result.count(result[0]) == 8)
        
    def testMappingGeneration6(self, mapDictSolver):
        #identifier and corresponding mapping are provided by conftest
        inputQuery = "EXISTS RUNNING TOGETHER [src, sink ] AND EQUALS map_one"
        assert(mapDictSolver.request(inputQuery) == False)
    
    def testMappingGeneration7(self, mapDictSolver):
        inputQuery = "EXISTS src MAPPED ARM00 AND filter_l MAPPED ARM01 AND RUNNING TOGETHER [src, filter_l ]"
        assert(mapDictSolver.request(inputQuery) == False)
        
    def testSetVector1(self, solver):
        inputQuery = "EXISTS src MAPPED ARM00 AND fft_l MAPPED ARM01"
        stateVec = [4, 5, 1, 2, 0, 0]
        result = [0, 1, 4, 5, 1, 2, 0, 0]
        assert(solver.request(inputQuery, vec=stateVec).to_list() == result)
        
    def testSetVector2(self, solver):
        inputQuery = "EXISTS src MAPPED ARM00 AND fft_l MAPPED ARM01 AND sink MAPPED ARM02"
        stateVec = [1, 1, 1, 1, 1]
        result = [0, 1, 1, 1, 1, 1, 1, 2]
        assert(solver.request(inputQuery, vec=stateVec).to_list() == result)
    
    def testSetVector3(self, mapDictSolver):
        #identifier and corresponding mapping are provided by conftest
        inputQuery = "EXISTS RUNNING TOGETHER [src, fft_l, fft_r, filter_l, filter_r, ifft_l, ifft_r, sink ] AND EQUALS map_two"
        #setting the state vector should be rejected anyway if the query includes an equals constraint
        stateVec = ["some nonesense"]
        result = mapDictSolver.request(inputQuery, vec=stateVec).to_list()
        assert(result.count(result[0]) == 8)
    
    