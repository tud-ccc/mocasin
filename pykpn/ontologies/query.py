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
from pykpn.common.mapping import Mapping

def main():
    kpn = SlxKpnGraph('SlxKpnGraph',  "apps/audio_filter/audio_filter.cpn.xml",'2017.04')
    platform = SlxPlatform('SlxPlatform', 'apps/audio_filter/exynos/exynos.platform', '2017.04')
    
    parser = ParserPython(Grammar.logicLanguage, reduce_tree=True, debug=False)
    
    inputString = "EXISTS ((ARM01 PROCESSING AND ARM02 PROCESSING) OR (ARM07 PROCESSING AND ARM06 PROCESSING)) AND (src MAPPED ARM03 OR filter_l MAPPED ARM04 OR filter_r MAPPED ARM05)"
    #inputString = "EXISTS (task01 MAPPED ARM03 AND ARM06 PROCESSING) OR (ARM04 PROCESSING AND task02 MAPPED ARM02 AND ARM03 PROCESSING AND task04 MAPPED ARM08)"
    #inputString = "EXISTS (ARM04 PROCESSING AND src MAPPED ARM03) OR (ARM03 PROCESSING AND ARM02 PROCESSING)"
    #inputString = "EXISTS sink MAPPED ARM01 AND src MAPPED ARM02 AND ARM03 PROCESSING AND ARM04 PROCESSING"
    #inputString = "EXISTS src MAPPED ARM00 AND sink MAPPED ARM01"
    
    parse_tree = parser.parse(inputString)
    query = visit_parse_tree(parse_tree, SemanticAnalysis(kpn, platform, debug=True))
    solver = Solver(kpn, platform)
    generator = solver.getMappingGenerator(query)
    
    i = 0
    for mapping in generator.nextMapping():
        if isinstance(mapping, Mapping):
            print(mapping.to_list())
        i += 1
        if i == 10:
            break
    
if __name__ == "__main__":
    main()
    
    