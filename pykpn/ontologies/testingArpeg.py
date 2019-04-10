from __future__ import unicode_literals, print_function
try:
    text=unicode
except:
    text=str

from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF
from arpeggio import RegExMatch as _

from arpeggio import ParserPython

def number():     return _(r'\d*\.\d*|\d+')
def factor():     return Optional(["+","-"]), [number, ("(", expression, ")")]
def term():       return factor, ZeroOrMore(["*","/"], factor)
def expression(): return term, ZeroOrMore(["+", "-"], term)
def calc():       return OneOrMore(expression), EOF
#def calc():       return OneOrMore(number), EOF

def easy():       return 3

#print "before parse def" #+ " ???"#str(easy())
parser = ParserPython(calc, debug=True)
#print "*******************past parser def"
parse_tree = parser.parse("35 56")
#parse_tree = parser.parse("-(4-1)*5+(2+4.67)+5.89/(.2+7)/(5 +26)")