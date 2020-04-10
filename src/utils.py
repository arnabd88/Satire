
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

gelpia_input_epsilon = 1e-2
gelpia_output_epsilon = 1e-2
gelpia_output_epsilon_relative = 1e-2
gelpia_epsilons = (gelpia_input_epsilon,
                   gelpia_output_epsilon,
                   gelpia_output_epsilon_relative)
gelpia_timeout = 10
gelpia_grace = 0
gelpia_update = 0
gelpia_max_iters = 0
gelpia_seed = 0

timeout = 10


def hashSig( inSig, alg ):
	hobj = hashlib.md5(str(inSig).encode('utf-8'))
	return hobj.hexdigest()

#def get_inputString(inputs):
#	inputStrList=[]
#	for inp in inputs.keys():
#		inputStrList.append(inp+":"+str(inputs[inp]["INTV"]))
#	inputStr = "{"+",".join(inputStrList)+"}"
#	#print("input length:", len(inputStrList), len(inputStrList[0]))
#	return inputStr

# rewrite this for returning list of combinatorial intervals


## this is for the case where we need to break down the size of
## string for subprocess call
## def get_inputString(inputs):
## 	inputStrList = []
## 	retList = []
## 	for inp in inputs.keys():
## 		inputStrList.append(inp+":"+str(inputs[inp]["INTV"]))
## 	inputStr = "{"+",".join(inputStrList)+"}"
## 	inputStrList = inputStr.split(",")
## 	#num_elems = len(inputStrList)
## 	#size_elem = len(inputStrList[1])
## 	#num_blocks = math.floor(num_elems/size_elems)
## 
## 	return inputStrList
	
def get_inputString(inputs):
    ret_list = list()
    for name,val in inputs.items():
        ret_list += [name, " = ", str(val["INTV"]), ";"]
    return "".join(ret_list)

def split_gelpia_format(msg):
	#print(msg)
	return msg.split("{")[0]\
								 .split("]")[0]\
								 .split("[")[-1]\
								 .split(",")




def parse_gelpia(msg):
	max_upper = re.search("Maximum: ([^\n]*)", msg).group(1)
	min_lower = re.search("Minimum: ([^\n]*)", msg).group(1)
	return [float(min_lower), float(max_upper)]
	#[max_lb, max_ub] = msgList[1].split("{")[0]\
	#							 .split("]")[0]\
	#							 .split("[")[-1]\
	#							 .split(",")
	# [max_lb, max_ub] = split_gelpia_format(msgList[1])
	# [min_lb, min_ub] = split_gelpia_format(msgList[2])
	# return [float(min_lb), float(max_ub)]
	#return [f_lb, f_ub]


def internal_gelpia(exec_list):
	arg_dict = gelpia.ap.parse_args(exec_list)
	gelpia.append_to_environ("PATH", gelpia.bin_dir)
	rust_ld_lib_addition = path.join(gelpia.base_dir, ".compiled")
	rust_ld_lib_addition += ":" + path.join(gelpia.base_dir, "src/func/target/release/")
	rust_ld_lib_addition += ":" + path.join(gelpia.base_dir, "target/release/deps")
	gelpia.append_to_environ("LD_LIBRARY_PATH", rust_ld_lib_addition)

	inputs = arg_dict['inputs'].values()
	inputs = "|".join(inputs)

	file_id = gelpia.mk_file_hash(arg_dict["rust_function"])
	function_filename = path.join(gelpia.src_dir,
					  "func/src/lib_generated_{}.rs".format(file_id))
	executable = path.join(gelpia.base_dir, 'target/release/cooperative')
	executable_args = ['-c', arg_dict["constants"],
			   '-f', arg_dict["interp_function"],
			   '-i', inputs,
			   "-x", str(arg_dict["input_epsilon"]),
			   "-y", str(arg_dict["output_epsilon"]),
			   "-r", str(arg_dict["rel_output_epsilon"]),
			   "-S", "generated_"+file_id, # Function file suffix
			   "-n", ",".join(arg_dict["inputs"]),
			   "-t", str(arg_dict["timeout"]),
			   "-u", str(arg_dict["update"]),
			   "-M", str(arg_dict["iters"]),
			   "--seed", str(arg_dict["seed"]),]

	with open(function_filename, 'w') as f:
		f.write(arg_dict["rust_function"])

	start = time.time()
	term_time = None
	if arg_dict["timeout"] != 0:
		if arg_dict["grace"] == 0:
			term_time = start + arg_dict["timeout"]*2
		else:
			term_time = start + arg_dict["grace"]
	output = ""
	for line in gelpia.iu.run_async(executable, executable_args, term_time):
		if not line.startswith("lb:"):
			output += line.strip()

	os.remove(function_filename)
	try:
		os.remove(path.join(gelpia.base_dir, ".compiled/libfunc_generated_"+file_id+".so"))
	except:
		pass

	try:
		p = path.join(gelpia.src_dir, "func/target/release/libfunc_generated_"+file_id+".so")
		os.remove(p)
	except:
		pass

	try:
		p = path.join(gelpia.src_dir, "func/target/release/func_generated_"+file_id+".d")
		os.remove(p)
	except:
		pass

	if output:
		try:
			idx = output.find('[')
			output = output[idx:]
			lst = eval(output, {'inf':float('inf')})
			assert(type(lst[-1]) is dict)
			for k in list(lst[-1]):
				if k[0] == "$":
					del lst[-1][k]
		except:
			print("Error unable to parse rust solver's output:",output)
			iu.log(log_level, lambda: iu.green("Parsing time: ")+str(parsing_end-parsing_start))
			sys.exit(-1)

		if arg_dict["dreal"]:
			if type(lst[0]) is list:
				lst[0] = reversed(lst[0])
				lst[0] = [-b for b in lst[0]]
			else:
				lst[0] = -lst[0]

	gelpia_max = lst[0][1]
	return gelpia_max



def invoke_gelpia_bak(symExpr, inputStr):
	## if the expression is a constant, dont bother to call gelpia
	expr_const = 1
	try:
		const_intv = float(str(symExpr))
		print("******** CONSTANT *************")
		return [const_intv, const_intv]
	except:
		#return [1.0,2.0]
		pass
		#print(str(symExpr), " is not constant")

	## apply this for anymore operator mismatches as necessary
	str_expr = re.sub(r'\*\*', "^", str(symExpr))
	str_expr = re.sub(r'-', "- ", str(str_expr))
	#print("expr to gelpia:", str_expr)

	exec_list = ["gelpia", "-f", str_expr, "-i", inputStr]
	#print(" ".join(exec_list))

	upper = internal_gelpia(exec_list)
	lower = internal_gelpia(exec_list + ["--dreal"])

	retval = [float(lower), float(upper)]

	#print("internal_gelpia got ",retval)
	return retval
	# print(" ".join(exec_list))
	# p = sb.Popen(exec_list, stdout=sb.PIPE, stderr=sb.PIPE)
	# s = p.communicate(timeout=timeout)
	# msg = s[0].decode("ASCII")
	# if("error" in msg.lower()):
	# 	print("Error when using gelpia... debug", msg)
	# 	sys.exit()
	# else:
	# 	#print(msg)
	# 	retval = parse_gelpia(msg.splitlines())
	# 	hashed[key] = retval
	# 	return retval
	# print("Timeout when solving->", str_expr)
	# sys.exit()

#@profile
#def invoke_gelpia(symExpr, inputStr):
#	try:
#		const_intv = float(str(symExpr))
#		#print("***** CONSTANT ******")
#		return [const_intv, const_intv]
#	except:
#		pass
#	
#	str_expr = re.sub(r'\*\*', "^", str(symExpr))
#	str_expr = re.sub(r'^-', "- ", str(str_expr))
#	#print(len(str_expr), len(inputStr))
#	
#	#exec_list = ["echo", "-T", "-f", str_expr, "-i", inputStr]
#	exec_list = ["gelpia_mm", "-T", "-f", str_expr, "-i"]
#	exec_list.append(inputStr[0])
#	for i in range(1, len(inputStr)):
#		exec_list.append(", ")
#		exec_list.append(inputStr[i])
#
#
#
#	print("exec_list:", exec_list)
#	Globals.gelpiaID += 1
#	start_time = time.time()
#	p = sb.Popen(exec_list, stdout=sb.PIPE, stderr=sb.PIPE)
#	s = p.communicate(timeout=timeout)
#	msg = s[0].decode("ASCII")
#	end_time = time.time()
#	if("error" in msg.lower()):
#		print("Error when using gelpia... debug", msg)
#		sys.exit()
#	else:
#		#print(msg)
#		retval = parse_gelpia(msg)
#		#hashed[key] = retval
#		return retval
#	print("Timeout when solving->", str_expr)
#	sys.exit()


import symengine as seng
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
	Globals.gelpiaID += 1
	#print("Begining New gelpia query->ID:", Globals.gelpiaID)
	#fout = open("gelpia_"+str(Globals.gelpiaID)+".txt", "w")
	#fout.write(str_expr)
	#fout.close()

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


def invoke_gelpia_herror(symExpr, inputStr, label="Func-> Dur:"):
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
	Globals.gelpiaID += 1
	#print("Begining New gelpia query->ID:", Globals.gelpiaID)
	#fout = open("gelpia_"+str(Globals.gelpiaID)+".txt", "w")
	#fout.write(str_expr)
	#fout.close()

	#print(str_expr)
	start_time = time.time()
	
	max_lower = Value("d", float("nan"))
	max_upper = Value("d", float("nan"))
	#print("ID:",Globals.gelpiaID, "\t Finding max, min\n")
	p = Process(target=gelpia.find_max, args=(str_expr,
	                                          gelpia_epsilons,
	                                          10,
	                                          gelpia_grace,
	                                          gelpia_update,
	                                          10,
	                                          gelpia_seed,
	                                          False,
	                                          gelpia.SRC_DIR,
	                                          gelpia_rust_executable,
	                                          max_lower,
	                                          max_upper))
	p.start()
	min_lower, min_upper = gelpia.find_min(str_expr,
	                                       gelpia_epsilons,
	                                       10,
	                                       gelpia_grace,
	                                       gelpia_update,
	                                       10,
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
	for fsyms in free_syms:
		ret_list += [str(fsyms), " = ", str(Globals.inputVars[fsyms]["INTV"]), ";"]
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
	freeSyms = [i for i in sym_expr.free_symbols]
	freeSyms.sort()
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
		Globals.hashBank[sig] = invoke_gelpia(sym_expr, inputStr)
		g2 = time.time()
		print("Gelpia solve = ", g2 - g1, "opCount =", seng.count_ops(sym_expr))
	else:
		print("MATCH FOUND")
		#Globals.hashBank[sig] = check
		pass

	return Globals.hashBank[sig]


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

def extract_input_dep(free_syms, inputVars=Globals.inputVars):
	ret_list = list()
	for fsyms in free_syms:
		#print(fsyms)
		#print(inputVars.keys())
		#print(inputVars[fsyms])
		ret_list += [str(fsyms), " = ", str(inputVars[fsyms]["INTV"]), ";"]
	return "".join(ret_list)

def generate_signature_tuner(sym_expr, inputVars=Globals.inputVars):

	try:
	    const_intv = float(str(sym_expr))
	    return [const_intv, const_intv]
	except ValueError:
	    pass
	#inputStr = extract_input_dep(list(map(str, sym_expr.free_symbols)), inputVars)
	inputStr = extract_input_dep(sym_expr.free_symbols, inputVars)
	#print("Gelpia input expr ops ->", seng.count_ops(sym_expr))
	return invoke_gelpia(sym_expr, inputStr)
