
import copy
import os
import sys
import re
import math as mt
import time
#import numpy as np
import Globals
#import sympy as sym
import random
import struct
import time
import subprocess as sb
from multiprocessing import Process, Value, Manager
import hashlib
from collections import OrderedDict
import symengine as seng

from itertools import tee

import shutil
import os.path as path
gelpia_path = shutil.which("gelpia")
gelpia_dir = path.dirname(gelpia_path)

sys.path.append(gelpia_dir)
import gelpia
import gelpia_logging as logging
logging.set_log_level(logging.QUIET)
logging.set_log_filename(None)


gelpia.setup_requirements(gelpia.GIT_DIR)
gelpia_rust_executable = gelpia.setup_rust_env(gelpia.GIT_DIR, False)

gelpia_input_epsilon = 1e-4
gelpia_output_epsilon = 1e-4
gelpia_output_epsilon_relative = 1e-4
gelpia_epsilons = (gelpia_input_epsilon,
                   gelpia_output_epsilon,
                   gelpia_output_epsilon_relative)
gelpia_timeout = 10
gelpia_grace = 0
gelpia_update = 0
gelpia_max_iters = 20000
gelpia_seed = 0

timeout = 10


def hashSig( inSig, alg ):
	hobj = hashlib.md5(str(inSig).encode('utf-8'))
	return hobj.hexdigest()




def invoke_gelpia(symExpr, inputStr, label="Func-> Dur:"):
	#try:
	#    const_intv = float(str(symExpr))
	#    return [const_intv, const_intv]
	#except ValueError:
	#    pass
	
	#print("In gelpia", seng.count_ops(symExpr))
	#print(symExpr)
	str_expr = re.sub(r'\*\*', "^", str(symExpr))
	str_expr = re.sub(r'Abs', "abs", str_expr)
	str_expr = re.sub(r're\b', "", str_expr)
	str_expr = re.sub(r'im\b', "0.0*", str_expr)
	#print("Pass conversion gelpia")
	str_expr = inputStr + str_expr
	#print("Begining New gelpia query->ID:", Globals.gelpiaID)
	Globals.gelpiaID += 1
	fout = open("gelpia_"+str(Globals.gelpiaID)+".txt", "w")
	fout.write("# --input-epsilon {ieps}\n".format(ieps=str(gelpia_input_epsilon)))
	fout.write("# --output-epsilon {oeps}\n".format(oeps=str(gelpia_output_epsilon)))
	fout.write("# --output-epsilon-relative {oreps}\n".format(oreps=str(gelpia_output_epsilon_relative)))
	fout.write("# --timeout {tout}\n".format(tout=str(gelpia_timeout)))
	fout.write("# --max-iters {miters}\n".format(miters=str(gelpia_max_iters)))
	fout.write(str_expr)
	fout.close()

	#print(str_expr)
	start_time = time.time()
	
	max_lower = Value("d", float("nan"))
	max_upper = Value("d", float("nan"))
	#print("ID:",Globals.gelpiaID, "\t Finding max, min\n")
	p = Process(target=gelpia.find_max, args=(str_expr,
	                                          gelpia_epsilons,
	                                          gelpia_timeout,
	                                          gelpia_grace,
	                                          gelpia_update,
	                                          gelpia_max_iters,
	                                          gelpia_seed,
	                                          False,
	                                          gelpia.SRC_DIR,
	                                          gelpia_rust_executable,
	                                          max_lower,
	                                          max_upper))
	p.start()
	min_lower, min_upper = gelpia.find_min(str_expr,
	                                       gelpia_epsilons,
	                                       gelpia_timeout,
	                                       gelpia_grace,
	                                       gelpia_update,
	                                       gelpia_max_iters,
	                                       gelpia_seed,
	                                       False,
	                                       gelpia.SRC_DIR,
	                                       gelpia_rust_executable)
	p.join()
	end_time = time.time()
	#print("Finishing gelpia query->ID:", Globals.gelpiaID)
	
	#print(str_expr)
	#print(label, end_time - start_time, "  , FSYM: ", len(symExpr.free_symbols))
	
	return [min_lower, max_upper.value]

	
def extract_input_dep(free_syms):
	ret_list = list()
	flist = [str(i) for i in free_syms]
	flist.sort()
	for fsyms in flist:
		ret_list += [str(fsyms), " = ", str(Globals.inputVars[seng.var(fsyms)]["INTV"]), ";"]
	return "".join(ret_list)
    #for name,val in inputs.items():
    #    ret_list += [name, " = ", str(val["INTV"]), ";"]
    #return "".join(ret_list)

def genSig(sym_expr):
	try:
		if seng.count_ops(sym_expr) == 0 :
			return float(str(sym_expr))
	except ValueError:
		pass
	d = OrderedDict()
	flist = [str(i) for i in sym_expr.free_symbols]
	flist.sort()
	freeSyms = [seng.var(fs) for fs in flist]
	# make this to a map
	#for i in range(0, len(freeSyms)):
	#	inp = freeSyms[i]
	#	d[inp] = str(i)+"_"+"{intv}".format(intv=Globals.inputVars[inp]["INTV"])

	fpt = map(lambda i : (str(freeSyms[i]), str(i)+"_"+"{intv}".format(intv=Globals.inputVars[freeSyms[i]]["INTV"])), \
	                      range(len(freeSyms)))
	d =	{p[0]:p[1] for p in fpt}

	regex = re.compile("(%s)" % "|".join(map(re.escape, d.keys())))

	strSig = regex.sub(lambda mo: d[mo.string[mo.start():mo.end()]], str(sym_expr))

	return hashSig(strSig, "md5")

def generate_signature(sym_expr):
	try:
		if(seng.count_ops(sym_expr)==0):
			const_intv = float(str(sym_expr))
			return [const_intv, const_intv]
	except ValueError:
	    pass

	#d = OrderedDict()
	#freeSyms = [str(i) for i in sym_expr.free_symbols]
	#freeSyms.sort()
	#for i in range(0,len(freeSyms)):
	#	inp = freeSyms[i]
	#	#print(inp, type(inp), Globals.inptbl[inp])
	#	d[inp] = str(i)+"_"+"{intv}".format(intv=Globals.inputVars[inp]["INTV"])

	#regex = re.compile("(%s)" % "|".join(map(re.escape, d.keys())))

	#strSig = regex.sub(lambda mo: d[mo.string[mo.start():mo.end()]], str(sym_expr))
	#sig = hashSig(strSig, "md5")
	#print("STRSIG->", strSig, sig)
	#Globals.hashBank[sig] = Globals.hashBank.get(sig, utils.invoke_gelpia(sym_expr, self._inputStr))
	#s1 = time.time()
	hbs = len(Globals.hashBank.keys())
	#s2 = time.time()
	#print("\nTime for hashing sig = ", s2 - s1)
	#print("************ HBS : ", hbs, " ******************")
	if(hbs > 100):
		list(map(lambda x : Globals.hashBank.popitem(x) , list(Globals.hashBank.keys())[0:int(hbs/2)]))
	sig = genSig(sym_expr)
	check = Globals.hashBank.get(sig, None)
	if check is None:
		inputStr = extract_input_dep(list(sym_expr.free_symbols))
		#print("Gelpia input expr ops ->", seng.count_ops(sym_expr))
		g1 = time.time()
		val = invoke_gelpia(sym_expr, inputStr)
		#print("Actual return :", val, Globals.gelpiaID)
		Globals.hashBank[sig] = [val, Globals.gelpiaID] #invoke_gelpia(sym_expr, inputStr)
		g2 = time.time()
		print("Gelpia solve = ", g2 - g1, "opCount =", seng.count_ops(sym_expr))
	else:
		#inputStr = extract_input_dep(list(sym_expr.free_symbols))
		#orig_query = invoke_gelpia(sym_expr, inputStr)
		#hashed_query = Globals.hashBank[sig][0]
		#match_queryid = Globals.hashBank[sig][1]
		#print("MATCH FOUND")
		#if orig_query != hashed_query:
		#	print(orig_query, hashed_query,  match_queryid, Globals.gelpiaID)
		##Globals.hashBank[sig] = check
		pass

	return Globals.hashBank[sig][0]


def wrap_generate_signature( sym_expr, collect_list, index):
	#print("Par->", os.getpid())
	valIntv = generate_signature(sym_expr)
	collect_list[index] = valIntv[1]

def generate_signature1(sym_expr):

	try:
	    const_intv = float(str(sym_expr))
	    return [const_intv, const_intv]
	except ValueError:
	    pass
	inputStr = extract_input_dep(list(map(str, sym_expr.free_symbols)))
	#print("Gelpia input expr ops ->", seng.count_ops(sym_expr))
	return invoke_gelpia(sym_expr, inputStr)

def generate_signature_herror(sym_expr):

	try:
	    const_intv = float(str(sym_expr))
	    return [const_intv, const_intv]
	except ValueError:
	    pass
	inputStr = extract_input_dep(list(map(str, sym_expr.free_symbols)))
	#print("Gelpia input expr ops ->", seng.count_ops(sym_expr))
	return invoke_gelpia_herror(sym_expr, inputStr)
	
#def extract_partialAST(NodeList_in, duplicate):
#
#	NodeList = copy.deepcopy(NodeList_in) if duplicate else NodeList_in
#
#	retainList = copy.copy(NodeList)
#	inspectList = copy.copy(NodeList)
#	seenList = []
#
#	while(len(inspectList) > 0):
#		node = inspectList.pop(0)
#		#print(node.name,"child->", [child.name for child in node.children])
#		#print("retainList:", [n.f_expression for n in retainList])
#		for child in node.children:
#			if child in seenList:
#				pass
#			else:
#				seenList.append(child)
#				retainList.append(child)
#				child.parents = [parent for parent in child.parents if parent in retainList]
#				inspectList.append(child)
#	return NodeList



def isConst(obj):
	if type(obj).__name__ == "Num":
		return True
	else:
		return False
		#try:
		#	x = float(str(obj.f_expression))
		#	return True
		#except:
		#	return False


def partition(items, predicate):
	a, b = tee((predicate(item), item) for item in items)
	return ((item for pred, item in a if not pred), (item for pred, item in b if pred))


def extract_partialAST(NodeList):

	parent_dict = dict()

	max_depth = max(list(map(lambda x: x.depth, NodeList)))
	it1, it2 = partition(NodeList, lambda x:x.depth==max_depth)
	next_workList = list(it1)
	workList = list(it2)

	for w in NodeList:
		parent_dict[w] = []

	# the assumption is all previous depths are seen by now
	while(len(workList) > 0): 
		node = workList.pop(0)
		for child in node.children:
			parent_dict[child] = parent_dict.get(child, [])
			parent_dict[child].append(node)
			next_workList.append(child)

		curr_depth = node.depth
		next_depth = curr_depth - 1
		if(len(workList)==0 and next_depth != -1 and len(next_workList)!=0):
			nextIter, currIter = partition(next_workList, \
				                                     lambda x:x.depth==next_depth)
			workList = list(set(currIter))
			next_workList = list(set(nextIter))

	## debug check
	#for k, vlist in parent_dict.items():
	#	print(k.f_expression, [v.f_expression for v in vlist])

	return parent_dict
			
########## Extra code for the selective tuner ####################
### some is redundant, remove later #############

#def extract_input_dep(free_syms, inputVars=Globals.inputVars):
#	ret_list = list()
#	for fsyms in free_syms:
#		#print(fsyms)
#		#print(inputVars.keys())
#		#print(inputVars[fsyms])
#		ret_list += [str(fsyms), " = ", str(inputVars[fsyms]["INTV"]), ";"]
#	return "".join(ret_list)
#
#def generate_signature_tuner(sym_expr, inputVars=Globals.inputVars):
#
#	try:
#	    const_intv = float(str(sym_expr))
#	    return [const_intv, const_intv]
#	except ValueError:
#	    pass
#	#inputStr = extract_input_dep(list(map(str, sym_expr.free_symbols)), inputVars)
#	inputStr = extract_input_dep(sym_expr.free_symbols, inputVars)
#	#print("Gelpia input expr ops ->", seng.count_ops(sym_expr))
#	return invoke_gelpia(sym_expr, inputStr)
