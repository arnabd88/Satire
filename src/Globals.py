

## GLobal table tracker

#inptbl = {}
#outtbl = {}

from collections import OrderedDict, defaultdict

inputVars = {}
outVars = []
lhstbl = {}

# symbol table
# obj_name -> {ref, op/token, children[]}
#tbl = {}

# common subexpression table
# to avoid any redundant expression
# f_expression -> obj
csetbl = {}

constTable = {}
symTable = defaultdict(object)
depthTable = defaultdict(set)

hashBank = OrderedDict()

# primary expression roots defines in spec
#roots = []

# ID variables per type 
# incremented at every instance generation and 
# use for object naming
#BinOpID = 0
#TransOpID = 0
gelpiaID = 0
FID=0

## CandidateList to track the depth

## control for gelpia expression and queue sizes
MaxOps = 500
MaxParSolve = 40

simplify = True
