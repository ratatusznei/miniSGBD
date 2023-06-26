from pprint import pprint
from Parser import *
import sys

p = Parser(sys.argv[1])
q = p.parse()

pprint(q.__dict__)
