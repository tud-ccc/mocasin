#Copyright (C) 2019 TU Dresden
#All Rights Reserved
#
#Authors: Andrès Goens, Felix Teweleit

from __future__ import unicode_literals, print_function 
try:
    text=unicode
except:
    text=str

from arpeggio import ParserPython, visit_parse_tree
from logicLanguage import Grammar, SemanticAnalysis
from solver import Solver
from pykpn.slx.platform import SlxPlatform
from pykpn.slx.kpn import SlxKpnGraph
from pykpn.mapper.random import RandomMapping

def main():
    kpn = SlxKpnGraph('SlxKpnGraph',  "apps/audio_filter/audio_filter.cpn.xml",'2017.04')
    platform = SlxPlatform('SlxPlatform', 'apps/audio_filter/exynos/exynos.platform', '2017.04')
    
    test = RandomMapping(kpn, platform)
    
    parser = ParserPython(Grammar.logicLanguage, reduce_tree=True, debug=True)
    
    inputQuery = "EXISTS ((ARM01 PROCESSING AND ARM02 PROCESSING) OR (ARM07 PROCESSING AND ARM06 PROCESSING)) AND (src MAPPED ARM03 OR filter_l MAPPED ARM04 OR filter_r MAPPED ARM05)"
    #inputQuery = "EXISTS (task01 MAPPED ARM03 AND ARM06 PROCESSING) OR (ARM04 PROCESSING AND task02 MAPPED ARM02 AND ARM03 PROCESSING AND task04 MAPPED ARM08)"
    #inputQuery = "EXISTS (ARM04 PROCESSING AND src MAPPED ARM03) OR (ARM03 PROCESSING AND ARM02 PROCESSING)"
    
    parse_tree = parser.parse(inputQuery)
    result = visit_parse_tree(parse_tree, SemanticAnalysis(kpn, platform, debug=True))
    solver = Solver(kpn, platform)
    
    if solver.solveQuery(result):
        print("Solved")
    else:
        print("Not so solved")
    
if __name__ == "__main__":
    main()