

import sys
import time
import argparse 
#import subprocess
#
import Globals
from gtokens import *
from lexer import Slex
from parser import Sparser

from AnalyzeNode_Serial import AnalyzeNode_Serial
from ASTtypes import *
import helper 

import logging

def parseArguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('--file', help='Test file name', required=True)
	parser.add_argument('--parallel', help='Enable parallel optimizer queries:use for large ASTs',\
							default=False, action='store_true')
	parser.add_argument('--enable-abstraction', help='Enable abstraction of internal node defintions,\
													  value indiactes level\
													  of abstraction. By default enabled to level-1. \
													  To disable pass 0', default=False, action='store_true')
	parser.add_argument('--mindepth', help='Min depth for abstraction. Default is 10',\
									  default=20, type=int)
	parser.add_argument('--maxdepth', help='Max depth for abstraction. Limiting to 40', \
									  default=40, type=int)
	#parser.add_argument('--fixdepth', help='Fix the abstraction depth. Default is -1(disabled)', \
	#								  default=-1, type=int)
	#parser.add_argument('--alg', help='Heuristic level for abstraction(default 0), \
	#									0 -> Optimal depth within mindepth and maxdepth(may loose correlation), \
	#									1 -> User defined fixed depth, \
	#									2 -> User Tagged nodes or only lhs nodes', \
	#									default=0, type=int)
	parser.add_argument('--simplify', help='Simplify expression -> could be costly for very large expressions',
										default=False, action='store_true')
	parser.add_argument('--logfile', help='Python logging file name -> default is default.log', default='default.log')
	parser.add_argument('--outfile', help='Name of the output file to write error info', default='outfile.txt')
	parser.add_argument('--std', help='Print the result to stdout', default=False, action='store_true')
	parser.add_argument('--sound', help='Turn on analysis for higher order errors', default=False, action='store_true')
	                                  

	result = parser.parse_args()
	return result




def simplify_with_abstraction(sel_candidate_list, argList, abs_depth):

	local_hashBank = {}
	mappedList = {}

	obj = AnalyzeNode_Serial(sel_candidate_list, argList)
	results = obj.start()
	print(results)




def	ErrorAnalysis(argList):

	absCount = 1
	probeList = helper.getProbeList()
	maxdepth = max([node.depth for node in probeList])
	maxdepth1 = max(list(Globals.depthTable.keys())+[0])
	assert(maxdepth == maxdepth1)

	logger.info("AST_DEPTH : {AST_DEPTH}".format(AST_DEPTH = maxdepth))

	bound_mindepth , bound_maxdepth = argList.mindepth, argList.maxdepth

	if ( argList.enable_abstraction ) :
		print("Abstraction Enabled... \n")
		#while ( maxdepth >= bound_maxdepth and max_depth >= bound_mindepth):
		[abs_depth,sel_candidate_list] = helper.selectCandidateNodes(maxdepth, bound_mindepth, bound_maxdepth)
		if ( len(sel_candidate_list) > 0 ):
			absCount += 1
			simplify_with_abstraction(sel_candidate_list, argList, abs_depth)
		else:
			pass
	


if __name__ == "__main__":
	start_exec_time = time.time()
	argList = parseArguments()
	sys.setrecursionlimit(10**6)
	print(argList)
	text = open(argList.file, 'r').read()
	fout = open(argList.outfile, 'w')
	##-----------------------
	logging.basicConfig(filename= argList.logfile,
					level = logging.INFO,
					filemode = 'w')
	logger = logging.getLogger()
	##-----------------------
	start_parse_time = time.time()
	lexer = Slex()
	parser = Sparser(lexer)
	parser.parse(text)
	del parser
	del lexer
	end_parse_time = time.time()
	parse_time = end_parse_time - start_parse_time
	logger.info("Parsing time : {parse_time} secs".format(parse_time = parse_time))

	##----- PreProcess to eliminate all redundant defintions ------
	pr1=time.time()
	helper.PreProcessAST()
	pr2=time.time()
	
	ea1 = time.time()
	results = ErrorAnalysis(argList)
	ea2 = time.time()
	#writeToFile(results)





	end_exec_time = time.time()
	##------ End of Analysis Results ------
	print("Parsing time : {parsing_time}\n".format(parsing_time = parse_time))
	print("PreProcessing time : {preprocess_time}\n".format(preprocess_time = pr2-pr1))
	print("Analysis time : {analysis_time}\n".format(analysis_time = ea2-ea1))
	print("Full time : {full_time}\n".format(full_time = end_exec_time-start_exec_time))



