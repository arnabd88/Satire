from gtokens import *
from lexer import Slex
from ASTtypes import *
#import sympy as sym
import ops_def as ops

#import utils
import copy
import sys

import globals
import time


class Sparser(object):

	tokens = Slex.tokens

	__slots__ = ['lexer', 'current_token', 'logger']
	#__slots__ = ['lexer', 'current_token', 'expr_lhs', 'expr_rhs', 'logger']

	#def __new__(cls, lexer):
	#	print("Creating Parser Instance ....")
	#	return super(Sparser, cls, lexer).__new__()

	def __init__(self, lexer):
		self.lexer  = lexer
		self.current_token = None

	def error(self):
		raise Exception('Invalid Syntax while parsing')

	def consume(self, token_type):
		#print(self.current_token.type, token_type, self.current_token.value)
		if self.current_token.type == token_type:
			self.current_token = self.lexer.get_next_token()
		else:
			self.error()

	def addDepthInfo(self, node):
		#pass
		globals.depthTable[node.depth] = globals.depthTable.get(node.depth, set())
		globals.depthTable[node.depth].add(node)
	
	def expr(self):
		"""
		expr	:	term ((PLUS | MINUS) term)*
		"""
		node = self.term()

		while self.current_token.type in (PLUS, MINUS):
			token = self.current_token
			self.consume(token.type)
			#node = self.CommonLut(BinOp(left=node, token=token, right=self.term()), token)
			node = BinOp(left=node, token=token, right=self.term())
			self.addDepthInfo(node)
			#print( node.depth, type(node).__name__, len(set(globals.depthTable[node.depth])) , len(globals.depthTable[node.depth]))

		return node


	def term(self):
		""" term : factor ((MUL | DIV) factor)* """
		node = self.factor()

		while self.current_token.type in (MUL, DIV):
			token = self.current_token
			self.consume(token.type)
			#node = self.CommonLut(BinOp(left=node, token=token, right=self.factor()), token)
			node = BinOp(left=node, token=token, right=self.factor())
			self.addDepthInfo(node)
			#print( node.depth, type(node).__name__, len(set(globals.depthTable[node.depth])) , len(globals.depthTable[node.depth]))

		return node


	def CheckSymTable(self, node, token):
		
		if globals.symTable.__contains__(token.value):
			return globals.symTable.__getitem__(token.value)
		else:
			globals.symTable.__setitem__(token.value, node)
			self.addDepthInfo(node)
			return node

	# Do the commonLut for Num/Constants and var to lookup the symbol table
	def CheckSymTable1(self, node, token):
		t1 = time.time()
		node_exists = globals.symTable.get(token.value)
		t2 = time.time()
		#print("lookup time = ", t2-t1, token.value, node.depth, node_exists.depth if node_exists is not None else 0)
		#globals.symTable[str(token.value)] = node
		#return node
		if node_exists is None:
			globals.symTable.__setitem__(token.value, node)
			self.addDepthInfo(node)
			#print( node.depth, type(node).__name__, len(set(globals.depthTable[node.depth])) ,\
			#len(globals.depthTable[node.depth]), node.rec_eval(node), token.value)
			return node
		else:
			globals.symTable.__setitem__(token.value, node_exists)
			#globals.symTable[str(token.value)] = node_exists
			## extra check for binops
			#if( type(node).__name__ == 'BinOp'):
			#	if node_exists.parents.__contains__(node):
			#		node_exists.parents.remove(node)
			#	for child in node_exists.children:
			#		if child.parents.__contains__(node):
			#			child.parents.remove(node)
			#del node
			return node_exists
		
		


	def factor(self):
		"""
			factor	:	PLUS factor
					|	MINUS factor | INTEGER | FLOAT 
					|	LPAREN expr RPAREN
					|	sqrt/sin/cos/log/exp/tan/cot/sec/cosh/sinh(expr)	|	ID
		"""
		token = self.current_token
		if token.type in (INTEGER, FLOAT):
			self.consume(token.type)
			#node = self.CommonLut(Num(token), token)
			#node = self.CheckSymTable(Num(token), token)
			#if not globals.constTable.__contains__(token.value):
			#	globals.constTable[token.value] = Num(token)
			# globals.constTable[token.value] = globals.constTable.get(token.value, Num(token))
			# return globals.constTable[token.value]
			return Num(token)
		elif token.type in (SQRT,SIN,COS,LOG,TAN,COT,SINH,COSH,EXP):
			self.consume(token.type)
			#node = self.CommonLut(TransOp(self.factor(), token), token)
			node = TransOp(self.factor(), token)
			self.addDepthInfo(node)
			#print( node.depth, type(node).__name__, len(set(globals.depthTable[node.depth])) , len(globals.depthTable[node.depth]))
			return node
		elif token.type == LPAREN:
			self.consume(LPAREN)
			node = self.expr()
			self.consume(RPAREN)
			self.addDepthInfo(node)
			#print( node.depth, type(node).__name__, len(set(globals.depthTable[node.depth])) , len(globals.depthTable[node.depth]))
			return node
		else:
			node = Var(token)
			self.consume(ID)
			node = self.CheckSymTable(node, token)
			return node



	def program(self):
		""" program : INPUTS OUTPUTS EXPRS """
		print("Inside Program")
		self.parse_input()
		self.parse_output()
		self.parse_expr()

	def parse_expr(self):
		"""exprs { expr_list } """
		self.consume(EXPRS)
		self.consume(SLPAREN)
		self.expr_list()
		self.consume(SRPAREN)

	def expr_list(self):
		""" expr_list : expr | ; | empty """
		self.assign_expr()

		while self.current_token.type == SEMICOLON :
			self.consume(SEMICOLON)
			self.assign_expr()

	def assign_expr(self):
		""" assign_expr : ID ASSIGN expr """
		if self.current_token.type == ID:
			name = str(self.current_token.value)
			nameToken = self.current_token
			self.consume(ID)  # var name
			rnd = str(self.current_token.value)
			self.consume(FPTYPE)  # rounding mode
			self.consume(ASSIGN)
			node = self.expr()
			node.set_rounding(rnd)
			node_exists = globals.symTable.get(nameToken.value, None)
			if node_exists is not None:
				self.error()
			globals.symTable[nameToken.value] = node

			#node_exists = globals.csetbl.get(node.f_expression, None)
			#if node_exists is None:
			#	self.error()
			#else:
			#	node_exists.set_rounding(rnd)
			#	#print(name, " : ", node_exists.depth, " : ", seng.count_ops(node_exists.f_expression))
			#	globals.lhstbl[name] = node_exists			## update roots from here


	def parse_output(self):
		""" outputs	{	outputs list } """
		self.consume(OUTPUTS)
		self.consume(SLPAREN)
		self.output_list()
		self.consume(SRPAREN)


	def output_list(self):
		""" output_list : output | ; | empty """
		self.output()

		while( self.current_token.type == SEMICOLON ):
			self.consume(SEMICOLON)
			self.output()

	def output(self):
		while self.current_token.type == ID:
			name = str(self.current_token.value)
			self.consume(ID)
			globals.outVars.append(name)

	def parse_input(self):
		""" input { interval_list } """
		self.consume(INPUTS)
		self.consume(SLPAREN)
		self.interval_list()
		self.consume(SRPAREN)

	def interval_list(self):
		""" interval_list : interval | ; | empty """

		self.interval()

		while(self.current_token.type == SEMICOLON):
			self.consume(SEMICOLON)
			self.interval()

	def interval(self):
		while self.current_token.type == ID:
			var_token = self.current_token
			name = str(self.current_token.value)
			self.consume(ID)
			fptype = str(self.current_token.value)
			self.consume(FPTYPE)
			self.consume(COLON)
			self.consume(LPAREN)
			#n = self.expr()
			#left = n.rec_eval(n)
			left = self.current_token.value
			self.consume(FLOAT)
			self.consume(COMMA)
			#n = self.expr()
			right = self.current_token.value
			#right = n.rec_eval(n)
			#print(left, ":", right)
			self.consume(FLOAT)
			self.consume(RPAREN)
			
			# create the input symbols here
			# and update the csetbl for symbol lookup to be used later
			symVar = FreeVar(var_token)
			symVar.set_rounding(fptype)
			#symVar.set_expression(symVar, symVar.eval(symVar))
			#globals.csetbl[symVar.f_expression] = globals.csetbl.get(symVar.f_expression, symVar)
			#if(left==right):
			#	print("Compressing")
			#	symVar.f_expression = left
			globals.symTable[var_token.value] = symVar
			globals.inputVars[var_token.value] = {"INTV" : [left, right]}


	def parse(self, text):
		self.lexer.create_token_generator(text)
		self.current_token = self.lexer.get_next_token()#current_token()
		self.program()
		print("Num LHS exprs ->", len(globals.symTable.keys()))
		print("Const expr ->", len(globals.constTable.keys()))
		#for k,v in globals.symTable.items():
		#	print(k)
		print("MaxDepth ->", max(list(globals.depthTable.keys())+[0]))
		#print("Num Unique nodes ->", len(globals.csetbl.keys()))


if __name__ == "__main__":
	
	start_parse_time = time.time()
	text = open(sys.argv[1], 'r').read()
	lexer = Slex()
	parser = Sparser(lexer)
	parser.parse(text)
	end_parse_time = time.time()
	num_unique_nodes = 0
	for k,v in globals.depthTable.items():
		print("Depth:", k, "\t: Num-Nodes: ", len(v))
		num_unique_nodes += len(v) if k!=0 else 0
	print("Num Unique Nodes = ", num_unique_nodes)

	print("Parsing time -> ", end_parse_time - start_parse_time)



