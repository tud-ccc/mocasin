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
    
    def testMapperInitialisation1(self, kpnGraph, platform, parser, solver):
        inputQuery = "EXISTS src MAPPED ARM00 AND sink MAPPED ARM01"
        parse_tree = parser.parse(inputQuery)
        constraints = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, debug=False))
        
        #make sure there is only one constraint set at the moment
        assert(len(constraints) == 1)
        
        generator = solver.getMappingGenerator(constraints)
        
        result = [0, -1, -1, -1, -1, -1, -1, 1]
        assert(result == generator.getProcessMapping())
        
        result = [0, 0, 0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        assert([] == generator.getMapperState()[1])
        
        result = [7, 7, 7, 7, 7, 7]
        generator.setMapperState(result)
        assert(result == generator.getMapperState()[0])
        
    def testMapperInitialisation2(self, kpnGraph, platform, parser, solver):
        inputQuery = "EXISTS src MAPPED ARM00 AND fft_l MAPPED ARM01 AND filter_l MAPPED ARM02 AND ifft_l MAPPED ARM03"
        parse_tree = parser.parse(inputQuery)
        constraints = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, debug=False))
        
        #make sure there is only one constraint set at the moment
        assert(len(constraints) == 1)
        
        generator = solver.getMappingGenerator(constraints)
        
        result = [0, 1, 2, 3, -1, -1, -1, -1]
        assert(result == generator.getProcessMapping())
        
        result = [0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        assert([] == generator.getMapperState()[1])
        
        result = [1, 1, 3, 4]
        generator.setMapperState(result)
        assert(result == generator.getMapperState()[0])
        
    def testMapperInitialisation3(self, kpnGraph, platform, parser, solver):
        inputQuery = "EXISTS src MAPPED ARM00 AND fft_l MAPPED ARM01 AND filter_l MAPPED ARM02 AND ARM03 PROCESSING AND ARM04 PROCESSING"
        parse_tree = parser.parse(inputQuery)
        constraints = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, debug=False))
        
        #make sure there is only one constraint set at the moment
        assert(len(constraints) == 1)
        
        generator = solver.getMappingGenerator(constraints)
        
        result = [0, 1, 2, -1, -1, -1, -1, -1]
        assert(result == generator.getProcessMapping())
        
        result = [0, 0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        assert([0,1] == generator.getMapperState()[1])
        
        result = [1, 1, 3, 4, 5]
        generator.setMapperState(result)
        assert(result == generator.getMapperState()[0])
        
    def testMappingGeneration1(self, kpnGraph, platform, parser, solver):
        inputQuery = "EXISTS src MAPPED ARM00 AND fft_l MAPPED ARM01"
        parse_tree = parser.parse(inputQuery)
        constraints = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, debug=False))
        
        #make sure there is only one constraint set at the moment
        assert(len(constraints) == 1)
        
        generator = solver.getMappingGenerator(constraints)
        
        result = [0, 1, -1, -1, -1, -1, -1, -1]
        assert(result == generator.getProcessMapping())
        
        result = [0, 0, 0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        assert([] == generator.getMapperState()[1])
        
        #First iteration
        result = [0, 1, 0, 0, 0, 0, 0, 0]
        for mapping in generator.nextMapping():
            assert(result == mapping)
            break
        
        result = [1, 0, 0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        
        #Second iteration
        result = [0, 1, 1, 0, 0, 0, 0, 0]
        for mapping in generator.nextMapping():
            assert(result == mapping)
            break
        
        result = [2, 0, 0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        
        #Third iteration
        result = [0, 1, 2, 0, 0, 0, 0, 0]
        for mapping in generator.nextMapping():
            assert(result == mapping)
            break
        
        result = [3, 0, 0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        
    def testMappingGeneration2(self, kpnGraph, platform, parser, solver):
        inputQuery = "EXISTS src MAPPED ARM00 AND fft_l MAPPED ARM01 AND sink MAPPED ARM02"
        parse_tree = parser.parse(inputQuery)
        constraints = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, debug=False))
        
        #make sure there is only one constraint set at the moment
        assert(len(constraints) == 1)
        
        generator = solver.getMappingGenerator(constraints)
        
        result = [0, 1, -1, -1, -1, -1, -1, 2]
        assert(result == generator.getProcessMapping())
        
        result = [0, 0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        assert([] == generator.getMapperState()[1])
        
        #First iteration
        result = [0, 1, 0, 0, 0, 0, 0, 2]
        for mapping in generator.nextMapping():
            assert(result == mapping)
            break
        
        result = [1, 0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        
        #Second iteration
        result = [0, 1, 1, 0, 0, 0, 0, 2]
        for mapping in generator.nextMapping():
            assert(result == mapping)
            break
        
        result = [2, 0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        
        #Third iteration
        result = [0, 1, 2, 0, 0, 0, 0, 2]
        for mapping in generator.nextMapping():
            assert(result == mapping)
            break
        
        result = [3, 0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        
    def testSetVector(self, kpnGraph, platform, parser, solver):
        inputQuery = "EXISTS src MAPPED ARM00 AND fft_l MAPPED ARM01 AND sink MAPPED ARM02 AND ARM04 PROCESSING"
        parse_tree = parser.parse(inputQuery)
        constraints = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, debug=False))
        
        #make sure there is only one constraint set at the moment
        assert(len(constraints) == 1)
        
        generator = solver.getMappingGenerator(constraints)
        
        result = [0, 1, -1, -1, -1, -1, -1, 2]
        assert(result == generator.getProcessMapping())
        
        result = [0, 0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        assert([0] == generator.getMapperState()[1])
        
        #First mapping
        result = [0, 1, 4, 0, 0, 0, 0, 2]
        for mapping in generator.nextMapping():
            assert(result == mapping)
            break
        
        result = [1, 0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        
        #Setting the inner state of the mapper and generate a mapping out of it
        result = [5, 2, 6, 1, 4]
        generator.setMapperState(result)
        assert(result == generator.getMapperState()[0])
    
        result = [0, 1, 4, 2, 6, 1, 4, 2]
        for mapping in generator.nextMapping():
            assert(result == mapping)
            break
        
        result = [6, 2, 6, 1, 4] 
        assert(result == generator.getMapperState()[0])
        
        #Setting another custom inner state for the generator
        result = [7, 7, 7, 7, 7]
        generator.setMapperState(result)
        assert(result == generator.getMapperState()[0])
        
        result = [0, 1, 0, 4, 0, 0, 0, 2]
        i = 0
        for mapping in generator.nextMapping():
            if i == 1:
                assert(result == mapping)
                break
            i += 1
        
        result = [1, 0, 0, 0, 0]
        assert(result == generator.getMapperState()[0])
        assert([1] == generator.getMapperState()[1])
    
    