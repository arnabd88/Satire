
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


# def error_query_reduction( QworkList, reduction=True ):
# 
# 	#!pred, pred
# 	QS, QC = partition(QworkList, lambda x: seng.count_ops(x)==0)
# 	#QS = [(str(sym_expr),extract_input_dep(list(sym_expr.free_symbols))) for sym_expr in QS]
# 	QS = map( lambda x: (str(x), extract_input_dep(list(x.free_symbols))), QS )
# 
# 	#sigTup = tuple(map(genSig, QS))
# 
# 	#intv_QS = tuple(map(invoke_gelpia, QS))+tuple([float(str(x))]*2 for x in QC)
# 
# 	pool = MyPool()
# 	intv_QS = tuple(pool.map(invoke_gelpia, QS))+tuple([float(str(x))]*2 for x in QC)
# 	pool.close()
# 	pool.join()
# 
# 	return sum([max([abs(i) for i in intv]) for intv in intv_QS])

	

def error_query_reduction( QworkList, reduction=True ):

	#!pred, pred
	QS_temp, QC = partitionList(QworkList, lambda x: seng.count_ops(x)==0)
	#QS = [(str(sym_expr),extract_input_dep(list(sym_expr.free_symbols))) for sym_expr in QS]
	#QS = map( lambda x: (str(x), extract_input_dep(list(x.free_symbols))), QS )

	HashList = list(map(genSig, QS_temp))
	HashBin = {sig: [i for i,x in enumerate(HashList) if x==sig] for sig in list(set(HashList))}
	ExistSig, QS_sig = partitionList(HashList, lambda x: x not in Globals.hashBank.keys())
	QS = [QS_temp[HashBin[sig][0]] for sig in QS_sig]
	Fresh = map( lambda x: (str(x), extract_input_dep(list(x.free_symbols))), QS )
	pool = MyPool()
	intv_QS = tuple(pool.map(invoke_gelpia, Fresh))
	pool.close()
	pool.join()

	QS_acc = sum( \
	            [ \
				  max([abs(i) for i in intv])*len(HashBin[QS_sig[j]]) \
				  for j,intv in enumerate(intv_QS)\
				]\
				)

	Exist_acc = sum( \
	            [ \
				  max([abs(i) for i in intv])*len(HashBin[ExistSig[j]]) \
				  for j,intv in enumerate([Globals.hashBank[k] for k in ExistSig])\
				]\
				)


	#Exist_acc = sum([max([abs(i) for i in intv])*len(HashBin[ExistSig[j]]) for j,intv in [Globals.hashBank[k] for k in Exist]])
	QC_acc = sum([abs(float(str(x))) for x in QC])

	## ---------- update the hashBank for a specific threshold size ------- ##
	hbs = len(Globals.hashBank.keys())
	if len(QS)==0:
		pass
	elif (hbs > 100):
		list(map(lambda x : Globals.hashBank.popitem(x) , list(Globals.hashBank.keys())[0:int(hbs/2)]))

	for i,k in enumerate(QS_sig):
		Globals.hashBank[k] = intv_QS[i] 

	error_acc = QS_acc + Exist_acc + QC_acc
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



