
import Globals

import symengine as seng
import ops_def as ops
import utils
import logging
import math
from gtokens import *

log = logging.getLogger(__name__)

class AST(object):

	__slots__ = ['depth', 'f_expression', 'children',\
	'parents', 'noise', 'rnd', 'name']

	def __init__(self):
		self.depth = 0
		self.f_expression = None
		self.children = ()
		self.parents = () #set()
		self.noise = (0,0)
		self.rnd = 1.0
		self.name = None

	#@staticmethod
	def set_expression(self, fexpr):
		self.f_expression = fexpr

	#@staticmethod
	def eval(obj):
		return obj.f_expression

	@staticmethod
	def rec_eval(obj):
		return obj.eval(obj)

	@staticmethod
	def simplify(lexpr):
		#if not Globals.simplify or (seng.count_ops(lexpr) > 30000):
		#	return lexpr
		#else:
		#	lexpr2 = seng.expand(lexpr)
		#	op1 = seng.count_ops(lexpr)
		#	op2 = seng.count_ops(lexpr2)
		#	if (op2 - op1 > 1000):
		#		Globals.simplify = False
		#	return lexpr2 if(seng.count_ops(lexpr2) < seng.count_ops(lexpr)) else lexpr

		##else:
		##	lexpr2 = seng.expand(lexpr)


		if(seng.count_ops(lexpr) > 30000):
			return lexpr
		else:
			return seng.expand(lexpr)
		return lexpr

	@staticmethod
	def rec_build_expression(obj):
		return obj.build_expression(obj)

	@staticmethod
	def get_noise(obj):
		return (seng.expand(obj.f_expression)) if obj.f_expression is not None else 0

	def set_rounding(self, rnd_type):
		self.rnd = ops._FP_RND[rnd_type]

	def get_rounding(self):
		return self.rnd * 1.0

import bigfloat as bf
class Num(AST):
	__slots__ = ['token']
	def __init__(self, token):
		super().__init__()
		self.token = token
		self.f_expression = self.eval(self)
		self.rnd = 0.0

	@staticmethod
	def eval(obj):
		return float(obj.token.value)

	@staticmethod
	def build_expression(obj):
		return str(obj.token.value)

	@staticmethod
	def get_noise(obj):
		if float(obj.token.value).is_integer and float(obj.token.value) == obj.token.value:
			return 0

		if bf.sub(bf.BigFloat(obj.token.value, bf.precision(113)),bf.BigFloat(obj.token.value, bf.precision(50)), bf.precision(1024)) == 0:
			return 0
		v = math.log(abs(obj.token.value),2)
		if (v - math.floor(v) != 0.0):
			if(obj.token.value <= 0):
				return -pow(2,math.floor(v))
			else:
				return pow(2,math.floor(v))
		return 0.0 #obj.token.value 

class FreeVar(AST):
	__slots__ = ['token']
	def __init__(self, token):
		super().__init__()
		self.token = token


	@staticmethod
	def eval(obj, round_mode="fl64"):
		name = str(obj.token.value)
		obj.depth = 0
		#obj.set_rounding(round_mode)
		intv = Globals.inputVars.get(obj.token.value, None)
		if intv is not None and (intv["INTV"][0]==intv["INTV"][1]):
			return intv["INTV"][0]
		else:
			return seng.var(name)

	@staticmethod
	def build_expression(obj):
		return str(obj.token.value)


	@staticmethod
	def set_noise(obj, valueTup):
		obj.noise = valueTup


	@staticmethod
	def get_noise(obj, sound=False):
		return obj.noise if sound else \
		       obj.noise[0] if obj.noise is not None\
			   else 0

	def mutate_to_abstract(self, tvalue, tid):
		self.token.value = tvalue
		self.token.type = tid

class Var(AST):
	__slots__ = ['token']
	def __init__(self, token):
		super().__init__()
		self.token = token

	@staticmethod
	def eval(obj, round_mode="fl64"):
		#name = str(obj.token.value)
		obj.set_rounding(round_mode)
		node_lhs = Globals.symTable.get(obj.token.value, None)
		if node_lhs is None:
			return obj.token.value
		else:
			return node_lhs.f_expression
			#return node_lhs.eval()

	@staticmethod
	def build_expression(obj):
		return str(obj.token.value)

class TransOp(AST):
	__slots__ = ['token']
	def __init__(self, right, token):
		super().__init__()
		self.token = token
		self.depth = right.depth+1
		self.children = (right,)
		right.parents += (self,)
		#right.parents.append(self)

	@staticmethod
	def eval(obj):
		lexpr = ops._FOPS[obj.token.type]([obj.children[0].f_expression])
		obj.depth = obj.children[0].depth+1
		#obj.rnd = obj.children[0].rnd
		obj.rnd = max([max([child.rnd for child in obj.children]), obj.rnd, 1.0])
		lexpr =  obj.simplify(lexpr)
		#print(seng.count_ops(lexpr), obj.depth)
		return lexpr
		#return seng.expand(lexpr)

	@staticmethod
	def rec_eval(obj):
		lexpr = ops._FOPS[obj.token.type]([obj.children[0].rec_eval(obj.children[0])])
		obj.depth = obj.children[0].depth+1
		obj.rnd = obj.children[0].rnd
		return obj.simplify(lexpr)

	@staticmethod
	def rec_build_expression(obj, use_name=True):
		if use_name:
			if obj.name is not None:
				return str(obj.name)
		if obj.token.type == COT:
			return  "1/tan((double)" + obj.children[0].rec_build_expression(obj.children[0]) + ")"
		else:
			return ops._CPPOPS[obj.token.type]([obj.children[0].rec_build_expression(obj.children[0])])

	def get_rounding(self):
		return self.rnd * ops._ALLOC_ULP[self.token.type]

class BinOp(AST):
	__slots__ = ['token']
	def __init__(self, left, token, right):
		super().__init__()
		self.token = token
		self.children = (left,right,)
		self.depth = max(left.depth, right.depth)+1
		left.parents += (self,)
		right.parents += (self,)
		#left.parents.add(self)
		#right.parents.add(self)

	@staticmethod
	def eval(obj):
		lexpr = ops._FOPS[obj.token.type]([child.f_expression for child in obj.children])
		obj.rnd = max([min([child.rnd for child in obj.children]), obj.rnd])
		if ((seng.Abs(obj.children[0].f_expression)==1.0 or \
		seng.Abs(obj.children[1].f_expression)==1.0) and obj.token.type==MUL):
			obj.rnd = 0.0
		else:
			#print("Before overwrite:", obj.rnd)
			obj.rnd = max([max([child.rnd for child in obj.children]), obj.rnd, 1.0])
			#print("After overwrite:", obj.rnd)


		lexpr =  obj.simplify(lexpr)
		#print(seng.count_ops(lexpr), obj.depth)
		return lexpr
		#return obj.simplify(lexpr)

	@staticmethod
	def rec_eval(obj):
		ch_lexpr = [child.rec_eval(child) for child in obj.children]
		lexpr = ops._FOPS[obj.token.type](ch_lexpr)
		if (seng.Abs(ch_lexpr[0])==1.0 or \
		seng.Abs(ch_lexpr[1])==1.0):
			obj.rnd = 0.0
		else:
			obj.rnd = max([max([child.rnd for child in obj.children]), 1.0])


		return obj.simplify(lexpr)

	@staticmethod
	def rec_build_expression(obj, use_name=True):
		if use_name:
			if obj.name is not None:
				return str(obj.name)
		ch_lexpr = [child.rec_build_expression(child) for child in obj.children]
		return ops._CPPOPS[obj.token.type](ch_lexpr)

	def get_rounding(self):
		return self.rnd * ops._ALLOC_ULP[self.token.type]

