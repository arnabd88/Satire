

import sys
import time
import copy
import Globals
from gtokens import *
import symengine as seng
import ops_def as ops

from collections import defaultdict
import utils
import helper

import logging

logger = logging.getLogger(__name__)


class AnalyzeNode_Serial(object):

	__slots__ = ['workList', 'next_workList', 'QworkList', 'Qthreshold', 'parentTracker', 'completed', \
	             'Accumulator', 'results', 'bwdDeriv', 'probeList', 'trimList',\
				 'argList', 'parent_dict', 'simplify', 'maxdepth', 'force']
				 

	def initialize(self):
		self.workList = []
		self.next_workList = []
		self.parentTracker = defaultdict(int)
		self.completed = defaultdict(set)
		self.Accumulator = defaultdict(int)
		self.results = {}
		self.bwdDeriv = {}#defaultdict(dict)
		self.QworkList = {}
		self.Qthreshold = 20 if Globals.argList.parallel else 1


	def __init__(self, probeNodeList, argList, maxdepth, force):
		self.initialize()
		self.probeList = probeNodeList
		self.trimList = probeNodeList
		self.argList   = argList
		self.maxdepth = maxdepth
		self.force = force
		## builds with side effects
		self.parent_dict = helper.expression_builder(probeNodeList)

	def __setup_outputs__(self):
		for node in self.trimList:
			print("setup outputs:", node.rnd)
			self.bwdDeriv[node] = {node : 1}
			self.parentTracker[node] = len(self.parent_dict[node])
			self.QworkList[node] = []

	def __init_workStack__(self):
		max_depth = max(list(map(lambda x: x.depth, self.trimList)))
		#print(max_depth)
		it1, it2 = utils.partition(self.trimList, lambda x:x.depth==max_depth)
		self.next_workList = list(it1)
		self.workList = list(it2)
	
	def converge_parents(self, node):
		return True if self.parentTracker[node] >= len(self.parent_dict[node]) else False
	

	def visit_node_deriv(self, node):
		outList = self.bwdDeriv[node].keys()
		opList = [child.f_expression for child in node.children]
		####
		for out in outList:
			print("Debug-deriv:", type(node).__name__)
			print("Node expr:", node.f_expression)
			print("Rounding:", node.get_rounding())
			print("Deriv: ", self.bwdDeriv[node][out])
			print("---------\n\n")
		####
		if(len(node.children) > 0):
			DerivFunc = ops._DFOPS[node.token.type]
			for i, child_node in enumerate(node.children):
				for outVar in outList:
					self.bwdDeriv[child_node] = self.bwdDeriv.get(child_node, {})
					self.bwdDeriv[child_node][outVar] = self.bwdDeriv[child_node].get(outVar, 0) +\
					                       self.bwdDeriv[node][outVar] * \
										   DerivFunc[i](opList)
										   #(0.1 if utils.isConst(child_node) else  DerivFunc[i](opList))
					self.next_workList.append(child_node)
				##------
				self.parentTracker[child_node] += 1
		self.completed[node.depth].add(node)

	def traverse_ast(self):
		next_workList = []
		curr_depth = 0
		next_depth = -1
		while(len(self.workList) > 0):
			node = self.workList.pop(0)
			curr_depth = node.depth
			next_depth = curr_depth - 1
			if (utils.isConst(node) or self.completed[node.depth].__contains__(node) ):
				####
				#for out in self.bwdDeriv[node].keys():
				#	print("Debug-deriv:", type(node).__name__)
				#	print("Node expr:", node.f_expression)
				#	print("Deriv: ", self.bwdDeriv[node][out])
				#	print("---------\n\n")
				####
				pass
			elif (self.converge_parents(node)):
			    self.visit_node_deriv(node)
			else:
			    self.workList.append(node)
			
			if(len(self.workList)==0 and next_depth!=-1 and len(self.next_workList)!=0):
			    nextIter, currIter = utils.partition(self.next_workList, \
			                                           lambda x:x.depth==next_depth)
			    self.workList = list(set(currIter))
			    self.next_workList = list(set(nextIter))


#	def propagate_symbolic(self, node):
#		for outVar in self.bwdDeriv[node].keys():
#			expr_solve = (((\
#			                (self.bwdDeriv[node][outVar]))*\
#							(node.get_noise(node))*(max(node.get_rounding(),outVar.get_rounding()) if node.rnd!=0.0 else node.get_rounding()  ))\
#							).__abs__()
#
#			if seng.count_ops(self.Accumulator[outVar]) > 4000:
#				intv = max(utils.generate_signature(self.Accumulator[outVar]))
#				self.Accumulator[outVar] = seng.expand(expr_solve)
#				expr_solve = intv
#			elif seng.count_ops( expr_solve ) > 1000:
#				expr_solve = max(utils.generate_signature(expr_solve))
#			self.Accumulator[outVar] += seng.expand(expr_solve)

	def propagate_symbolic(self, node):
		for outVar in self.bwdDeriv[node].keys():
			expr_solve = (((\
			                (self.bwdDeriv[node][outVar]))*\
							(node.get_noise(node))*(max(node.get_rounding(),outVar.get_rounding()) if node.rnd!=0.0 else node.get_rounding()  ))\
							).__abs__()

			if seng.count_ops(self.Accumulator[outVar]) > 4000:
				self.QworkList[outVar].append(self.Accumulator[outVar])
				self.Accumulator[outVar] = seng.expand(expr_solve)
			elif seng.count_ops( expr_solve ) > 1000:
				self.QworkList[outVar].append(expr_solve)
			else:
				self.Accumulator[outVar] += seng.expand(expr_solve)
			if len(self.QworkList[outVar]) >= self.Qthreshold:
				self.Accumulator[outVar] += utils.error_query_reduction(self.QworkList[outVar])
				self.QworkList[outVar].clear()
			#self.Accumulator[outVar] += seng.expand(expr_solve)

	def visit_node_ferror(self, node):
		
		for child in node.children:
			if not self.completed[child.depth].__contains__(child):
				self.visit_node_ferror(child)

		self.propagate_symbolic(node)
		self.completed[node.depth].add(node)


	def first_order_error(self):

		for node in self.trimList:
			if not self.completed[node.depth].__contains__(node):
				self.visit_node_ferror(node)

		#for node in self.Accumulator.keys():
		#	errIntv = utils.generate_signature(self.Accumulator[node])
		#	print("----------- Dump the error expression for plotting ---------- ")
		#	print(self.Accumulator[node])
		#	print("// end dump ")
		#	err = max([abs(i) for i in errIntv])
		#	fintv = utils.generate_signature(node.f_expression)
		#	self.results[node] = { "ERR" : err, \
		#						  "SERR" : 0.0, \
		#						  "INTV" : fintv \
		#						 }

		for node in self.Accumulator.keys():
			
			self.QworkList[node].append(self.Accumulator[node])
			self.Accumulator[node] = utils.error_query_reduction(self.QworkList[node])
			self.QworkList[node].clear()
			fintv = utils.generate_signature(node.f_expression)
			self.results[node] = {"ERR"	: self.Accumulator[node], \
								  "SERR" : 0.0, \
								  "INTV" : fintv \
								 }

		return self.results
			


	def start(self):

		local_hashbank = {}
		mappedList = {}
		#print("Reached here\n")
		self.trimList = self.probeList
		maxOpCount = max([seng.count_ops(n.f_expression) for n in self.trimList])
		abs_depth = max([n.depth for n in self.trimList])
		#print(maxOpCount, self.maxdepth, abs_depth)
		if self.force:
			pass
		elif maxOpCount > 1000 and self.maxdepth > 10 and abs_depth > 5:
			if self.argList.mindepth==self.argList.maxdepth:
				pass
			else:
				return {"maxOpCount" : maxOpCount, "flag" : False}
			
		
		if self.argList.compress:
			if(len(self.trimList) > 1):
				for node in self.probeList:
					sig = utils.genSig(node.f_expression )
					enode = local_hashbank.get(sig, None)
					if enode is None:
						local_hashbank[sig] = node
						mappedList[node] = []
					else:
						#print("Ever")
						mappedList[local_hashbank[sig]].append(node)
				self.trimList = mappedList.keys()

			print(len(self.probeList), len(self.trimList))
			logger.info("Primary cand list={l1}, Cmpressed cand list={l2}".format(l1=len(self.probeList), l2=len(self.trimList)))
			#print("const:", [(n.f_expression,id(n)) for n in Globals.depthTable[0]])
			self.parent_dict = helper.expression_builder(self.trimList, build=False)

		self.__init_workStack__()
		self.__setup_outputs__()

		#print("Begin Derivatives\n", time.time())
		self.traverse_ast()
		#print("Finished Derivatives\n", time.time())
		self.completed.clear()
		results =  self.first_order_error()

		del local_hashbank

		for node, depList in mappedList.items():
			for dnode in depList:
				results[dnode] = copy.deepcopy(results[node])
				assert(dnode in self.probeList)
		return results

	
