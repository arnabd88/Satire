
import Globals
import math
import symengine as seng
from collections import defaultdict

import logging

logger = logging.getLogger(__name__)

def getProbeList():
	return [Globals.symTable[outVar] for outVar in Globals.outVars]


def dfs_partial_ast(node, reachable, parent_dict):

	for child in node.children:
		if reachable[child.depth].__contains__(child):
			pass
		else:
			dfs_partial_ast(child, reachable, parent_dict)
		parent_dict[child].add(node)

	node.set_expression(node.eval(node))
	#print(node.f_expression)
	reachable[node.depth].add(node)


def build_partial_ast(probeList):

	parent_dict = defaultdict(set)
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

		print("ABSTRACTION_DEPTH : {abs_depth}".format(abs_depth=abs_depth))
		logger.info("ABSTRACTION_DEPTH : {abs_depth}".format(abs_depth=abs_depth))

		## Obtain all candidate list at this level
		CandidateList = Globals.depthTable[abs_depth]

		## Check back if filter is required on this

		return [abs_depth, CandidateList]
		
	

