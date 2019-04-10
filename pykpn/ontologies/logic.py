from __future__ import unicode_literals, print_function
try:
    text=unicode
except:
    text=str

from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, \
    ParserPython, PTNodeVisitor, visit_parse_tree, OrderedChoice
from arpeggio import RegExMatch as _

#white space
def ws():
    return _(r'\s*')

def logic():
    return (expression, EOF)

#Left associative order of operations: (), Relation, !, &&, ||, ->
def expression():
    return (a, implyOp)

def implyOp():
    return ZeroOrMore(_(r'\s*->\s*'), a)

def a():
    return (b, orOp)

def orOp():
    return ZeroOrMore( _(r'\s*\|\|\s*') ,b)

def b():
    return (nonInfix, andOp)

def andOp():
    return ZeroOrMore( _(r'\s*\&\&\s*') ,nonInfix)

#boolean must proceed relation, relation must proceed parens
def nonInfix():
    return OrderedChoice([boolean, relation, parens, notOp ])

def parens():
    return ( _(r'\s*\(\s*') ,expression, _(r'\s*\)\s*') )

def relation():
    return (ws, name, _(r'\('), ws , args , ws, _(r'\)'), ws  )

def args():
    return Optional((literal, ZeroOrMore( ws, _(r',') , ws , literal, ws )  ))

def notOp():
    return ( _(r'\s*\!\s*') , expression)

def integer():
    return (ws, _(r'\d+'), ws)

def decimal():
    return (ws, _(r'\d*\.\d+') ,ws)

#Backslash is an escape character for quotes
def string():
    return (ws, _(r'"'), _(r'(?:[^"\\]|\\.)*'), _(r'"') ,ws) 


def boolean():
    return OrderedChoice([trueBoolean, falseBoolean])

def trueBoolean():
    return (ws, _(r'true'), ws)

def falseBoolean():
    return (ws, _(r'false'), ws)

def terminal():
    return OrderedChoice([boolean, string, decimal, integer])

def name():
    return _(r'[ab-z](([ab-z]|[AB-z]|[0-9]|\_)*)')

def variable():
    return (ws, name ,ws)

def literal():
    return OrderedChoice([terminal, variable])



# def number():     return _(r'\d*\.\d*|\d+')
# def factor():     return Optional(["+","-"]), [number,
#                           ("(", expression, ")")]
# def term():       return factor, ZeroOrMore(["*","/"], factor)
# def expression(): return term, ZeroOrMore(["+", "-"], term)
# def calc():       return OneOrMore(expression), EOF


def main(debug=False):
    # First we will make a parser - an instance of the calc parser model.
    # Parser model is given in the form of python constructs therefore we
    # are using ParserPython class.
    parser = ParserPython(logic, debug=debug)

    # An expression we want to evaluate
    #input_expr = ' false -> (false && false) && ! superRelation38() '
    input_expr = ' false -> (false && false) && ! superRelation38( true, 52, "words with \\" to mess it up!2times\\\ ", false, 28.18 ) '
    #input_expr = '  superRelation38( what ) '

    # We create a parse tree out of textual input_expr
    parse_tree = parser.parse(input_expr)

if __name__ == "__main__":
    # In debug mode dot (graphviz) files for parser model
    # and parse tree will be created for visualization.
    # Checkout current folder for .dot files.
    main(debug=True)

