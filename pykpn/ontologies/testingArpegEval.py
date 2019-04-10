from testingArpeg import *
from arpeggio import ParserPython
parser = ParserPython(calc)
parse_tree = parser.parse("-(4-1)*5+(2+4.67)+5.89/(.2+7)")