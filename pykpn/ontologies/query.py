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


def main():
    parser = ParserPython(Grammar.logicLanguage, reduce_tree=True, debug=True)
    
    #inputQuery = "EXISTS ((ARM01 PROCESSING AND ARM02 PROCESSING) OR (ARM07 PROCESSING AND ARM08 PROCESSING)) AND (task01 MAPPED ARM03 OR task02 MAPPED ARM04 OR task03 MAPPED ARM05)"
    #inputQuery = "EXISTS (task01 MAPPED ARM03 AND ARM06 PROCESSING) OR (ARM04 PROCESSING AND task02 MAPPED ARM02 AND ARM03 PROCESSING AND task04 MAPPED ARM08)"
    inputQuery = "EXISTS (task01 MAPPED ARM03 OR ARM04 PROCESSING) AND ARM04 PROCESSING"
    
    parse_tree = parser.parse(inputQuery)
    result = visit_parse_tree(parse_tree, SemanticAnalysis(debug=True))
    
if __name__ == "__main__":
    main()