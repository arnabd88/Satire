
import Globals
import math
import symengine as seng
from collections import defaultdict

import logging

logger = logging.getLogger(__name__)

def getProbeList():
	return [Globals.symTable[outVar] for outVar in Globals.outVars]


def dfs_expression_builder(node, reachable, parent_dict):

	for child in node.children:
		if not reachable[child.depth].__contains__(child):
			dfs_expression_builder(child, reachable, parent_dict)
		parent_dict[child].append(node)

	node.set_expression(node.eval(node))
	#print(node.f_expression)
	reachable[node.depth].add(node)


def expression_builder(probeList):

	parent_dict = defaultdict(list)
	reachable = defaultdict(set)

	for node in probeList:
		if not reachable[node.depth].__contains__(node):
			dfs_expression_builder(node, reachable, parent_dict)

	del reachable

	return parent_dict


## for these two, expressions are pre-built
def dfs_partial_ast(node, reachable, parent_dict):

	for child in node.children:
		if reachable[child.depth].__contains__(child):
			pass
		else:
			dfs_partial_ast(child, reachable, parent_dict)
		parent_dict[child].append(node)

	#node.set_expression(node.eval(node))
	#print(node.f_expression)
	reachable[node.depth].add(node)


def build_partial_ast(probeList):

	parent_dict = [] #defaultdict(set)
	reachable = defaultdict(set)

	for node in probeList:
		if not reachable[node.depth].__contains__(node):
			dfs_partial_ast(node, reachable, parent_dict)

	del reachable

	# Debug Check
	#for k,v in parent_dict.items():
	#	if k.depth > 2:
	#		print(k.depth, len(v), len(k.parents))
	#print(Globals.symTable.keys())
	#selN = Globals.symTable[seng.var('xp2_8')]
	#print(selN.depth, len(selN.parents))
	return parent_dict


def pretraverse(node, reachable):
	
	for child in node.children:
		if reachable[child.depth].__contains__(child):
			pass
		else:
			pretraverse(child, reachable)

	#print(node.depth)
	reachable[node.depth].add(node)

def PreProcessAST():

	probeList = getProbeList()
	reachable = defaultdict(set)
	
	rhstbl = {}
	for k, v in Globals.symTable.items():
		rhstbl[v] = k

	for node in probeList:
		if not reachable[node.depth].__contains__(node):
			pretraverse(node, reachable)

	print("Pre :", len(Globals.symTable))
	Globals.symTable =	{syms : node for node,syms in rhstbl.items() \
							if reachable[node.depth].__contains__(node)}
	print("Post :", len(Globals.symTable))
	prev_numNodes = sum([ len(Globals.depthTable[el]) for el in Globals.depthTable.keys() if el!=0] )
	Globals.depthTable = reachable
	curr_numNodes = sum([ len(Globals.depthTable[el]) for el in Globals.depthTable.keys() if el!=0] )
	print("Pre Total nodes post processing: ", prev_numNodes)
	print("Pre Total nodes post processing: ", curr_numNodes)

def filterCandidate(bdmin, bdmax, dmax):
	return list(filter( lambda x:x.depth >= bdmin and x.depth <= bdmax ,\
	                           [v for k,v in Globals.symTable.items() if v.depth!=0]\
							 ))

	#f = lambda x : float(x.depth)/(max_abs_depth) + 0.1
	#g = lambda x, y : (-1)*y*math.log(y,2)*len(x.parents)

	#lambda x : [node.depth, g(x,f(x)]

def evaluate_cost( node, max_abs_depth):
	prob_depth = float(node.depth)/(max_abs_depth) + 0.1
	c_depth_info = (-1)*prob_depth*math.log(prob_depth,2)*len(node.parents)

def selectCandidateNodes(maxdepth, bound_mindepth, bound_maxdepth):

	PreCandidateList = filterCandidate(bound_mindepth, bound_maxdepth, maxdepth)
	print("Length Precand List =", len(PreCandidateList))

	## Increment the depth bound if candidate list is Null
	## Keep doing until nodes become available for abstraction

	loc_bdmax = bound_maxdepth
	while ( len(PreCandidateList) <= 0 and loc_bdmax <= maxdepth):
		loc_bdmax += 5
		PreCandidateList = filterCandidate(bound_mindepth, loc_bdmax, maxdepth)

	if(len(PreCandidateList) <= 0):
		return []
	else:
		f = lambda x : float(x.depth)/(loc_bdmax) + 0.1
		g = lambda x, y : (-1)*y*math.log(y,2)*len(x.parents)
		cost_list = list(map( lambda x : [x.depth, g(x, f(x))], \
		                 PreCandidateList \
						))
		## summing up the cost at a given depth
		## [(depthi, costSumi) ...]
		sum_depth_cost = [(depth, sum(list(map(lambda x:x[1] if x[0]==depth\
		                     else 0, cost_list)))) \
							 for depth in range(bound_mindepth, loc_bdmax)]

		sum_depth_cost.sort(key=lambda x:(-x[1], x[0]))
		abs_depth = sum_depth_cost[0][0]

		print("CURRENT AST_DEPTH = : {ast_depth}".format(ast_depth=maxdepth))
		print("ABSTRACTION_DEPTH : {abs_depth}".format(abs_depth=abs_depth))
		logger.info("CURRENT AST_DEPTH = : {ast_depth}".format(ast_depth=maxdepth))
		logger.info("ABSTRACTION_DEPTH : {abs_depth}".format(abs_depth=abs_depth))

		## Obtain all candidate list at this level
		CandidateList = Globals.depthTable[abs_depth]

		## Check back if filter is required on this

		return [abs_depth, CandidateList]
		
	
def writeToFile(results, fout, inpfile, stdflag, sound):

	fout.write("INPUT_FILE : "+inpfile+"\n")
	dumpStr = ''
	for outVar in Globals.outVars:
		#errIntv = results[Globals.lhstbl[outVar]]["ERR"]
		num_ulp_maxError = results[Globals.symTable[outVar]]["ERR"]
		num_ulp_SecondmaxError = results[Globals.symTable[outVar]]["SERR"]
		funcIntv = results[Globals.symTable[outVar]]["INTV"]
		#num_ulp_maxError = max([abs(i) for i in errIntv])
		maxError = num_ulp_maxError*pow(2, -53)
		SecondmaxError = num_ulp_SecondmaxError*pow(2, -53)
		outIntv = [funcIntv[0]-maxError-SecondmaxError, funcIntv[1]+maxError+SecondmaxError]
		abserror = 2*(maxError + SecondmaxError)

		#print("//-------------------------------------")
		#print("Ouput Variable -> ", outVar)
		#print("Real Interval  -> ", funcIntv)
		#print("FP Interval    -> ", outIntv)
		#print("Absolute Error -> ", abserror)
		##print("Estimated bits preserved -> ", 52 - math.log(num_ulp_maxError,2))
		#print("//-------------------------------------\n\n")
		#print("Var:", outVar, "=>", results[Globals.lhstbl[outVar]])
		#print(k.f_expression, v)
		dumpStr += "\n//-------------------------------------\n"
		dumpStr += "VAR : "+ str(outVar) + "\n"
		dumpStr += "ABSOLUTE_ERROR : "+str(abserror)+"\n"
		dumpStr += "First-order Error : "+str(2*maxError)+"\n"
		if sound:
			dumpStr += "Higher-order Error : "+str(2*SecondmaxError)+"\n"
		dumpStr += "REAL_INTERVAL : "+str(funcIntv)+"\n"
		dumpStr += "FP_INTERVAL : "+str(outIntv)+"\n"
		dumpStr += "//-------------------------------------\n"

	fout.write(dumpStr+"\n")
	if stdflag:
		print(dumpStr)


