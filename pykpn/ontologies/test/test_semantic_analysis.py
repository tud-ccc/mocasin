#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Felix Teweleit

from arpeggio import visit_parse_tree
from pykpn.ontologies.logicLanguage import SemanticAnalysis


def test_query_1(parser, kpnGraph, platform, cfg):
    inputQuery = "EXISTS ARM04 PROCESSING AND src MAPPED ARM03"
    parse_tree = parser.parse(inputQuery)
    result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, cfg, debug=False))
        
    assert(len(result) == 1)
    assert(len(result[0]) == 2)
    
def test_query_2(parser, kpnGraph, platform, cfg):
    inputQuery = "EXISTS ARM04 PROCESSING OR src MAPPED ARM03"
    parse_tree = parser.parse(inputQuery)
    result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, cfg, debug=False))
        
    assert(len(result) == 2)
    for constraintSet in result:
        assert(len(constraintSet) == 1)
        
def test_query_3(parser, kpnGraph, platform, cfg):
    inputQuery = "EXISTS ((ARM01 PROCESSING AND ARM02 PROCESSING) OR (ARM07 PROCESSING AND ARM06 PROCESSING)) AND (src MAPPED ARM03 OR filter_l MAPPED ARM04 OR filter_r MAPPED ARM05)"
    parse_tree = parser.parse(inputQuery)
    result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, cfg, debug=False))
        
    assert(len(result) == 6)
    for constraintSet in result:
        assert(len(constraintSet) == 3)
    
def test_query_4(parser, kpnGraph, platform, cfg):
    inputQuery = "EXISTS fft_r MAPPED ARM00 AND sink MAPPED ARM01 AND filter_l MAPPED ARM01 AND ARM05 PROCESSING AND ARM07 PROCESSING"
    parse_tree = parser.parse(inputQuery)
    result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, cfg, debug=False))
        
    assert(len(result) == 1)
    assert(len(result[0]) == 5)
        
def test_query_5(parser, kpnGraph, platform, cfg):
    inputQuery = "EXISTS (ARM00 PROCESSING) AND ((fft_l MAPPED ARM01) OR ((sink MAPPED ARM03) AND ((ARM04 PROCESSING) OR ((ARM02 PROCESSING) OR ((ARM01 PROCESSING) AND (sink MAPPED ARM02))))))"
    parse_tree = parser.parse(inputQuery)
    result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, cfg, debug=False))
        
    assert(len(result) == 4)
        
    """Count occurrence of different set lengths  
    """
    lenTwo = 0
    lenThree = 0
    lenFour = 0
    lenDefault = 0
        
    for element in result:
        if len(element) == 2:
            lenTwo += 1
        elif len(element) == 3:
            lenThree += 1
        elif len(element) == 4:
            lenFour += 1
        else:
            lenDefault += 1
        
    assert(lenTwo == 1)
    assert(lenThree == 2)
    assert(lenFour == 1)
    assert(lenDefault == 0)
        
def test_query_6(parser, kpnGraph, platform, cfg):
    inputQuery = "EXISTS (ARM00 PROCESSING) OR ((fft_l MAPPED ARM01) AND ((sink MAPPED ARM03) OR ((ARM04 PROCESSING) AND ((ARM02 PROCESSING) OR ((ARM03 PROCESSING) OR ((ARM01 PROCESSING) AND (sink MAPPED ARM02)))))))"
    parse_tree = parser.parse(inputQuery)
    result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, cfg, debug=False))
        
    assert(len(result) == 5)
        
    """Count occurrence of different set lengths  
    """
    lenOne = 0
    lenTwo = 0
    lenThree = 0
    lenFour = 0
    lenDefault = 0
        
    for element in result:
        if len(element) == 1:
            lenOne += 1
        elif len(element) == 2:
            lenTwo += 1
        elif len(element)  == 3:
            lenThree += 1
        elif len(element) == 4:
            lenFour += 1
        else:
            lenDefault += 1
                
    assert(lenOne == 1)
    assert(lenTwo == 1)
    assert(lenThree == 2)
    assert(lenFour == 1)
    assert(lenDefault == 0)
        
def test_query_7(parser, kpnGraph, platform, cfg):
    inputQuery = "EXISTS ARM04 PROCESSING AND RUNNING TOGETHER [src, sink, fft_l ]"
    parse_tree = parser.parse(inputQuery)
    result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, cfg, debug=False))
        
    assert(len(result) == 1)
    assert(len(result[0]) == 2)
        
def test_query_8(parser, kpnGraph, platform, cfg):
    inputQuery = "EXISTS RUNNING TOGETHER [src, sink, ifft_r ] AND ARM02 PROCESSING AND ARM03 PROCESSING AND src MAPPED ARM07"
    parse_tree = parser.parse(inputQuery)
    result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, cfg, debug=False))
        
    assert(len(result) == 1)
    assert(len(result[0]) == 4)

def test_query_9(parser, kpnGraph, platform, cfg):
    mapDict = {"map_one" : None}
    inputQuery = "EXISTS ARM04 PROCESSING AND src MAPPED ARM03 AND EQUALS map_one"
    parse_tree = parser.parse(inputQuery)
    result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, cfg, mapDict, debug=False))
        
    assert(len(result) == 1)
    assert(len(result[0]) == 3)
        
def test_query_10(parser, kpnGraph, platform, cfg):
    mapDict = {"map_one" : None, "map_two" : None}
    inputQuery = "EXISTS (ARM04 PROCESSING AND EQUALS map_one) OR (src MAPPED ARM03 AND EQUALS map_two)"
    parse_tree = parser.parse(inputQuery)
    result = visit_parse_tree(parse_tree, SemanticAnalysis(kpnGraph, platform, cfg, mapDict, debug=False))
        
    assert(len(result) == 2)
    assert(len(result[0]) == 2)
    assert(len(result[1]) == 2)
