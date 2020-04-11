
from gtokens import *
#import sympy as sym
import symengine as seng
from sly import Lexer

class Slex(Lexer):


	tokens = { INPUTS, OUTPUTS, EXPRS, \
				INTEGER, FLOAT, PLUS, \
				MINUS, MUL, DIV, SQRT, SIN, COS, \
				LOG, EXP, TAN, COT, COSH, SINH, IDEN, ASSIGN, LPAREN, RPAREN, SLPAREN, \
				SRPAREN, COLON, SEMICOLON, COMMA, ID, \
				FPTYPE }


	ignore = ' \t'
	ignore_comment = r'\#.*'
	# regular exprs
	PLUS		=	r'\+'	
	MUL			=	r'\*'	
	DIV			=	r'\/'	
	ASSIGN		=	r'\='	
	LPAREN		=	r'\('	
	RPAREN		=	r'\)'	
	SLPAREN		=	r'\{'	
	SRPAREN		=	r'\}'
	COLON		=	r'\:'
	SEMICOLON	=	r'\;'
	COMMA		=	r'\,'


	ID			=	r'[a-zA-Z][a-zA-Z0-9_]*'
	ID['INPUTS'] = INPUTS
	ID['OUTPUTS'] = OUTPUTS
	ID['EXPRS'] = EXPRS
	ID['sqrt'] = SQRT
	ID['sin']	= SIN
	ID['cos']	= COS
	ID['log']	= LOG
	ID['exp']	= EXP
	ID['tan']	= TAN
	ID['cot']	= COT
	ID['cosh']	= COSH
	ID['sinh']	= SINH
	ID['rnd16'] = FPTYPE
	ID['rnd32'] = FPTYPE # 'rnd64', 'fl16', 'fl32', 'fl64'] = FPTYPE
	ID['rnd64'] = FPTYPE
	ID['fl16']  = FPTYPE
	ID['fl32']  = FPTYPE
	ID['fl64']  = FPTYPE


	##--- some class attributes ----
	##--- we will have only one lexer instance ---
	pos = 0
	token_list = []
	current_token = None
	tok = None


	def ID(self, t):
		if t.type not in (INPUTS, OUTPUTS, EXPRS):
			#t.value = sym.symbols(t.value)
			t.value = seng.var(t.value)
		return t

	#@_(r'[\-]?\d+\.\d+[e\-\d+]?')
	@_(r'[\-]?\d+\.\d+([eE][-+]?\d+)?')
	#@_(r'[+-]?[0-9]+\.[0-9]+')
	def FLOAT(self, t):
		t.value = float(t.value)
		#t.value = t.value
		#print("value -> ", t.value)
		return t

	@_(r'[\-]?\d+([eE][-+]?\d+)?')
	def INTEGER(self, t):
		t.value = float(t.value)
		t.type = FLOAT
		return t
	
	# needs to be defined later after lexing the negative numbers
	MINUS		=	r'\-'	

	@_(r'\n+')
	def ignore_newline(self, t):
		self.lineno = t.value.count('\n')

	def error(self, t):
		print('Line %d: Bad character %r' % (self.lineno, t.value[0]))

	def create_token_generator(self, text):
		self.tok = self.tokenize(text)

	def get_current_token(self):
		return self.current_token

	def get_next_token(self):
		try:
			return self.tok.__next__()
		except StopIteration:
			return None



if __name__ == "__main__":
	import sys
	text = open(sys.argv[1], 'r').read()
	lexer = Slex()

	tok = lexer.tokenize(text)
	
	cnt = 0
	while(1):
		try:
			x = tok.__next__()
			print(x)
			cnt += 1
		except StopIteration:
			print(None)
			break
	print('Token count =', cnt)	

