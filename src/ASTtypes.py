
import globals

import symengine as seng
import ops_def as ops
import utils
import logging

log = logging.getLogger(__name__)

class AST(object):

	__slots__ = ['depth', 'f_expression', 'children',\
	'parents', 'noise', 'rnd']

	def __init__(self):
		self.depth = 0
		self.f_expression = None
		self.children = ()
		self.parents = ()
		self.noise = (0,0)
		self.rnd = 1.0

	@staticmethod
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
		if(seng.count_ops(lexpr) > 30000):
			return lexpr
		else:
			return seng.expand(lexpr)
		return lexpr

	@staticmethod
	def get_noise(obj):
		return (seng.expand(obj.f_expression)) if self.f_expression is not None else 0

	def set_rounding(self, rnd_type):
		self.rnd = ops._FP_RND[rnd_type]

	def get_rounding(self):
		return self.rnd

class Num(AST):
	__slots__ = ['token']
	def __init__(self, token):
		super().__init__()
		self.token = token
		self.f_expression = self.eval(self)
		self.rnd = 0.0
	
	@staticmethod
	def eval(obj):
		return obj.token.value

	@staticmethod
	def get_noise(obj):
		return 0

class FreeVar(AST):
	__slots__ = ['token']
	def __init__(self, token):
		super().__init__()
		self.token = token

		
	@staticmethod
	def eval(obj, round_mode="fl64"):
		name = str(obj.token.value)
		obj.depth = 0
		obj.set_rounding(round_mode)
		intv = globals.inputVars.get(name, None)
		if intv is not None and (intv[0]==intv[1]):
			return intv[0]
		else:
			return seng.var(name)


	@staticmethod
	def get_noise(obj, sound=False):
		return obj.noise if sound else \
		       abs(obj.noise[0]) if obj.noise is not None\
			   else 0

	def mutate_to_abstract(self, value, tid):
		self.token.value = tvalue
		self.token.type = tid

class Var(AST):
	__slots__ = ['token']
	def __init__(self, token):
		super().__init__()
		self.token = token
		
	@staticmethod
	def eval(obj, round_mode="fl64"):
		name = str(obj.token.value)
		obj.set_rounding(round_mode)
		node_lhs = globals.symTable.get(name, None)
		if node_lhs is None:
			return obj.token.value
		else:
			return node_lhs.f_expression
			#return node_lhs.eval()

class TransOp(AST):
	__slots__ = ['token']
	def __init__(self, right, token):
		super().__init__()
		self.token = token
		self.depth = right.depth+1
		self.children = (right,)
		right.parents += (self,)

	@staticmethod
	def eval(obj):
		lexpr = ops._FOPS[obj.token.type]([obj.children[0].f_expression])
		obj.depth = obj.children[0].depth+1
		obj.rnd = obj.children[0].rnd
		return obj.simplify(lexpr)
		#return seng.expand(lexpr)

	@staticmethod
	def rec_eval(obj):
		lexpr = ops._FOPS[obj.token.type]([obj.children[0].rec_eval(obj.children[0])])
		obj.depth = obj.children[0].depth+1
		obj.rnd = obj.children[0].rnd
		return obj.simplify(lexpr)

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

	@staticmethod
	def eval(obj):
		lexpr = ops._FOPS[obj.token.type]([child.f_expression for child in obj.children])
		if (seng.Abs(obj.children[0].f_expression)==1.0 or \
		seng.Abs(obj.children[1].f_expression)==1.0):
			obj.rnd = 0.0
		else:
			obj.rnd = max([min([child.rnd for child in obj.children]), 1.0])


		return obj.simplify(lexpr)

	@staticmethod
	def rec_eval(obj):
		ch_lexpr = [child.rec_eval(child) for child in obj.children]
		lexpr = ops._FOPS[obj.token.type](ch_lexpr)
		if (seng.Abs(ch_lexpr[0])==1.0 or \
		seng.Abs(ch_lexpr[1])==1.0):
			obj.rnd = 0.0
		else:
			obj.rnd = max([min([child.rnd for child in obj.children]), 1.0])


		return obj.simplify(lexpr)


	def get_rounding(self):
		return self.rnd * ops._ALLOC_ULP[self.token.type]
	
