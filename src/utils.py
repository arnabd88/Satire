
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
import multiprocessing
import multiprocessing.pool
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
gelpia_max_iters = 4000
gelpia_seed = 0

timeout = 10



def partition(items, predicate):
	a, b = tee((predicate(item), item) for item in items)
	return ((item for pred, item in a if not pred), (item for pred, item in b if pred))


def partitionList(items, predicate):
	a, b = tee((predicate(item), item) for item in items)
	return (list(item for pred, item in a if not pred), list(item for pred, item in b if pred))

	
def extract_input_dep(free_syms):
	ret_list = list()
	flist = [str(i) for i in free_syms]
	flist.sort()
	for fsyms in flist:
		ret_list += [str(fsyms), " = ", str(Globals.inputVars[seng.var(fsyms)]["INTV"]), ";"]
	return "".join(ret_list)

def hashSig( inSig, alg ):
	hobj = hashlib.md5(str(inSig).encode('utf-8'))
	return hobj.hexdigest()


def genSig(sym_expr):
	d = OrderedDict()
	flist = [str(i) for i in sym_expr.free_symbols]
	flist.sort()
	freeSyms = [seng.var(fs) for fs in flist]
	fpt = map(lambda i : (str(freeSyms[i]), str(i)+"_"+"{intv}".format(intv=Globals.inputVars[freeSyms[i]]["INTV"])), \
	                      range(len(freeSyms)))
	d =	{p[0]:p[1] for p in fpt}

	regex = re.compile("(%s)" % "|".join(map(re.escape, d.keys())))

	strSig = regex.sub(lambda mo: d[mo.string[mo.start():mo.end()]], str(sym_expr))

	return hashSig(strSig, "md5")

def invoke_gelpia(sexpr_inpstr_tuple):
	inputStr = sexpr_inpstr_tuple[1]
	str_expr = str(sexpr_inpstr_tuple[0])
	str_expr = re.sub(r'\*\*', "^", str_expr)
	str_expr = re.sub(r'Abs', "abs", str_expr)
	str_expr = re.sub(r're\b', "", str_expr)
	str_expr = re.sub(r'im\b', "0.0*", str_expr)
	str_expr = inputStr + str_expr

	if Globals.argList.gverbose:
		filename = "gelpia_{batchid}_{pid}.txt".format(batchid=Globals.batchID, pid=os.getpid())
		fout = open(filename, 'w')
		fout.write("# --input-epsilon {ieps}\n".format(ieps=str(gelpia_input_epsilon)))
		fout.write("# --output-epsilon {oeps}\n".format(oeps=str(gelpia_output_epsilon)))
		fout.write("# --output-epsilon-relative {oreps}\n".format(oreps=str(gelpia_output_epsilon_relative)))
		fout.write("# --timeout {tout}\n".format(tout=str(gelpia_timeout)))
		fout.write("# --max-iters {miters}\n".format(miters=str(gelpia_max_iters)))
		fout.write(str_expr)
		fout.close()
	
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

	return [min_lower, max_upper.value]




## Paralleized reduction call
## For each query obtain a hashsig
## Group queries by common hashsig
## only send unique queries per hashsig

## The below code works for python3.6.9 but fails for higher versions
# class NoDaemonicProcess(multiprocessing.Process):
# 	def _get_daemon(self):
# 		return False
# 	def _set_daemon(self, value):
# 		pass
# 	daemon = property(_get_daemon, _set_daemon)
# 
# class MyPool(multiprocessing.pool.Pool):
#     Process = NoDaemonicProcess
##--

class NoDaemonicProcess(multiprocessing.Process):
	@property
	def daemon(self):
		return False

	@daemon.setter
	def daemon(self, value):
		pass

class NoDaemonContext(type(multiprocessing.get_context())):
	Process = NoDaemonicProcess

class MyPool(multiprocessing.pool.Pool):
	def __init__(self, *args, **kwargs):
		kwargs['context'] = NoDaemonContext()
		super(MyPool, self).__init__(*args, **kwargs)


#def error_query_reduction( QworkList, reduction=True ):
#
#	#!pred, pred
#	print("New reduction query", [seng.count_ops(x) for x in QworkList])
#	QS, QC = partition(QworkList, lambda x: seng.count_ops(x)==0)
#	#QS = [(str(sym_expr),extract_input_dep(list(sym_expr.free_symbols))) for sym_expr in QS]
#	QS = map( lambda x: (str(x), extract_input_dep(list(x.free_symbols))), QS )
#
#	#sigTup = tuple(map(genSig, QS))
#
#	#intv_QS = tuple(map(invoke_gelpia, QS))+tuple([float(str(x))]*2 for x in QC)
#
#	pool = MyPool()
#	intv_QS = tuple(pool.map(invoke_gelpia, QS))+tuple([float(str(x))]*2 for x in QC)
#	pool.close()
#	pool.join()
#	print("End reduction query")
#
#	return sum([max([abs(i) for i in intv]) for intv in intv_QS])

	
def error_query_reduction_with_pool(QworkList, numProcesses=os.cpu_count()//1):
	QworkList_object = map( lambda x : (str(x), extract_input_dep(list(x.free_symbols))), QworkList)
	pool = MyPool(numProcesses)
	intv_results = tuple(pool.map(invoke_gelpia, QworkList_object))
	pool.close()
	pool.join()
	Globals.batchID += 1
	Globals.gelpiaID += len(intv_results)
	return intv_results


def error_query_reduction( QworkList):

	if len(QworkList)==1:
		intv = generate_signature(QworkList[0])
		return max([abs(i) for i in intv])

	else:
		pass

	# SymQueryList      -> Elements are symbolic queries
	# ConstQueryList    -> Elements are constant queries
	SymQueryList, ConstQueryList = partitionList(QworkList, lambda x: seng.count_ops(x)==0)

	# HashList -> ordered List of the hash signatures of expressions in SymQueryList
	HashList = list(map(genSig, SymQueryList))

	# HashBin -> Dictionary of key->value pairs such that: {key=signature : value=[indices in Hashlist of corresponding symbolic expressions with matching signatures}
	HashBin = {sig : [i for i,x in enumerate(HashList) if x==sig] for sig in list(set(HashList))}

	# Exist_Signatures -> List of matching signatures found in older hashbanks
	# New_Signatures   -> List of new signatures generated for this incoming batch of queries
	Exist_Signatures, New_Signatures =  partitionList(HashList, lambda x: x not in Globals.hashBank.keys())

	# New_SymQueryList -> List of new freshly minted symbolic queries identified by their unique md5 signatures
	#New_SymQueryList = [SymQueryList[HashBin[sig][0]] for sig in New_Signatures]
	New_SymQueryList = map(lambda x: SymQueryList[HashBin[x][0]],New_Signatures)

	# New_SymQuery_object -> Formatted New_SymQueryList with required datatypes
	# New_SymQuery_object = map( lambda x : (str(x), extract_input_dep(list(x.free_symbols))), New_SymQueryList)
	intv_QS = error_query_reduction_with_pool(New_SymQueryList)

	New_SymQuery_Accumulator = sum( \
	            					[ \
									  max([abs(i) for i in intv])*len(HashBin[New_Signatures[j]]) \
									  for j,intv in enumerate(intv_QS)\
									]\
								)

	Exist_SymQuery_Accumulator = sum( \
	            [ \
				  max([abs(i) for i in intv])*len(HashBin[Exist_Signatures[j]]) \
				  for j,intv in enumerate([Globals.hashBank[k] for k in Exist_Signatures])\
				]\
				)

	ConstQuery_Accumulator = sum([abs(float(str(x))) for x in ConstQueryList])

	## ---------- update the hashBank for a specific threshold size ------- ##
	hbs = len(Globals.hashBank.keys())
	if len(New_Signatures)==0:
		pass
	elif (hbs > 100):
		list(map(lambda x : Globals.hashBank.popitem(x) , list(Globals.hashBank.keys())[0:int(hbs/2)]))

	for i,k in enumerate(New_Signatures):
		Globals.hashBank[k] = intv_QS[i] 

	error_acc = New_SymQuery_Accumulator + Exist_SymQuery_Accumulator + ConstQuery_Accumulator
	print("Happy to exit\n")
	return error_acc




def invoke_gelpia_serial(symExpr):
	inputStr = extract_input_dep(list(symExpr.free_symbols))
	str_expr = re.sub(r'\*\*', "^", str(symExpr))
	str_expr = re.sub(r'Abs', "abs", str_expr)
	str_expr = re.sub(r're\b', "", str_expr)
	str_expr = re.sub(r'im\b', "0.0*", str_expr)
	str_expr = inputStr + str_expr
	
	max_lower = Value("d", float("nan"))
	max_upper = Value("d", float("nan"))
	#print("ID:",Globals.gelpiaID, "\t Finding max, min\n")
	##-- Create dumps if verbose is on ---
	if Globals.argList.gverbose:
		filename = "gelpia_{batchid}_{pid}.txt".format(batchid=Globals.batchID, pid=os.getpid())
		fout = open(filename, 'w')
		fout.write("# --input-epsilon {ieps}\n".format(ieps=str(gelpia_input_epsilon)))
		fout.write("# --output-epsilon {oeps}\n".format(oeps=str(gelpia_output_epsilon)))
		fout.write("# --output-epsilon-relative {oreps}\n".format(oreps=str(gelpia_output_epsilon_relative)))
		fout.write("# --timeout {tout}\n".format(tout=str(gelpia_timeout)))
		fout.write("# --max-iters {miters}\n".format(miters=str(gelpia_max_iters)))
		fout.write(str_expr)
		fout.close()

	##---
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

	return [min_lower, max_upper.value]



def generate_signature(sym_expr):
	try:
		if(seng.count_ops(sym_expr)==0):
			const_intv = float(str(sym_expr))
			return [const_intv, const_intv]
	except ValueError:
	    pass


	return invoke_gelpia_serial(sym_expr)



def isConst(obj):
	if type(obj).__name__ == "Num":
		return True
	else:
		return False



