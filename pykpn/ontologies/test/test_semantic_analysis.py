#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

from arpeggio import visit_parse_tree
from pykpn.ontologies.logicLanguage import Grammar, SemanticAnalysis

class TestSemanticAnalysis(object):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_query_1(self, parser, kpnGraph, platform):
        inputQuery = "EXISTS ARM04 PROCESSING AND src MAPPED ARM03"
        parse_tree = parser.parse(inputQuery)
        result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, debug=False))
        
        assert(len(result) == 1)
        assert(len(result[0]) == 2)
    
    def test_query_2(self, parser, kpnGraph, platform):
        inputQuery = "EXISTS ARM04 PROCESSING OR src MAPPED ARM03"
        parse_tree = parser.parse(inputQuery)
        result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, debug=False))
        
        assert(len(result) == 2)
        for constraintSet in result:
            assert(len(constraintSet) == 1)
        
    def test_query_3(self, parser, kpnGraph, platform):
        inputQuery = "EXISTS ((ARM01 PROCESSING AND ARM02 PROCESSING) OR (ARM07 PROCESSING AND ARM06 PROCESSING)) AND (src MAPPED ARM03 OR filter_l MAPPED ARM04 OR filter_r MAPPED ARM05)"
        parse_tree = parser.parse(inputQuery)
        result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, debug=False))
        
        assert(len(result) == 6)
        for constraintSet in result:
            assert(len(constraintSet) == 3)
    
    def test_query_4(self, parser, kpnGraph, platform):
        inputQuery = "EXISTS fft_r MAPPED ARM00 AND sink MAPPED ARM01 AND filter_l MAPPED ARM01 AND ARM05 PROCESSING AND ARM07 PROCESSING"
        parse_tree = parser.parse(inputQuery)
        result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, debug=False))
        
        assert(len(result) == 1)
        assert(len(result[0]) == 5)
        
    def test_query_5(self, parser, kpnGraph, platform):
        inputQuery = "EXISTS (ARM00 PROCESSING AND (fft_l MAPPED ARM01 OR sink MAPPED ARM03)) AND (ARM04 PROCESSING OR ARM02 PROCESSING OR (ARM01 PROCESSING AND sink MAPPED ARM02))"
        parse_tree = parser.parse(inputQuery)
        result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, debug=False))
        
        assert(len(result) == 6)
        
        """Count occurrence of different set lengths  
        """
        lenThree = 0
        lenFour = 0
        lenDefault = 0
        
        for element in result:
            if len(element) == 3:
                lenThree += 1
            elif len(element) == 4:
                lenFour += 1
            else:
                lenDefault += 1
                
        assert(lenThree == 4)
        assert(lenFour == 2)
        assert(lenDefault == 0)
        
    def test_query_6(self, parser, kpnGraph, platform):
        inputQuery = "EXISTS (ARM00 PROCESSING OR (fft_l MAPPED ARM01 AND sink MAPPED ARM03)) OR ((ARM04 PROCESSING AND (ARM02 PROCESSING OR ARM03 PROCESSING)) OR (ARM01 PROCESSING AND sink MAPPED ARM02))"
        parse_tree = parser.parse(inputQuery)
        result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, debug=False))
        
        assert(len(result) == 5)
        
        """Count occurrence of different set lengths  
        """
        lenOne = 0
        lenTwo = 0
        lenDefault = 0
        
        for element in result:
            if len(element) == 1:
                lenOne += 1
            elif len(element) == 2:
                lenTwo += 1
            else:
                lenDefault += 1
                
        assert(lenOne == 1)
        assert(lenTwo == 4)
        assert(lenDefault == 0)
        

    
    
    
    
    
    
    