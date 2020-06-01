import sys
import math as m
import copy

#1024 -> 512
#512 -> 256
#256 -> 128
#128 -> 64
#64  -> 32
#32 -> 16
#16 -> 8
#8 -> 4
#4 -> 2
#2 -> 1


def serial_reduction(N):
	
	A = [i for i in range(N)]

	print("serial sum:", sum(A))
	return sum(A)

def parallel_reduction(N, nthreads):

	A = [i for i in range(N)]
	stages = int(m.log(N,2))
	assert(2**stages == N)

	for n in range(0, stages):

		B = copy.deepcopy(A)
		size = 2**(stages-n-1)
		#A = A[0:size]
		step = pow(2,n)
		jump = pow(2,n+1)
		#print(n, step, jump)
		#print(A)
		for i in range(0,size):
			A[i*jump] += A[i*jump + step]
			#print(i*jump, i*jump + step)

	print("Parallel-red:", A[0])
	return A

def parallel_reduction_symbolic(N, fout):
	 
	stages = int(m.log(N,2))
	assert(2**stages==N)

	A = ["A_{ID}".format(ID=i) for i in range(N)]
	fout.write("INPUTS {\n\n")
	for i in range(N):
		fout.write("{Ai}\t fl64 : (-1.0, 1.0) ;\n".format(Ai=A[i]))
	fout.write("}\n")

	fout.write("OUTPUTS {\n\n")
	fout.write("A_{stage}_{ID} ;\n".format(stage=stages-1, ID=0))
	fout.write("}\n")
	

	fout.write("EXPRS {\n\n")
	for n in range(0, stages):
		step = 2**n
		jump = 2**(n+1)
		size = 2**(stages-n-1)

		for i in range(0,size):
			lhs = "A_{stage}_{ID}".format(stage=n, ID=i*jump)
			rhs = "{expr0} + {expr1}".format( expr0 = A[i*jump], expr1 = A[i*jump + step])
			fout.write("{lhs} rnd64 = {rhs} ;\n".format(lhs=lhs, rhs=rhs))
			A[i*jump] = lhs
	fout.write("}\n")

def serial_symbolic(N, fout):

	A = ["A_{ID}".format(ID=i) for i in range(N)]
	stage = 0

	fout.write("INPUTS {\n\n")
	for i in range(N):
		fout.write("{Ai}\t fl64 : (-1.0, 1.0) ;\n".format(Ai=A[i]))
	fout.write("}\n")

	fout.write("OUTPUTS {\n\n")
	fout.write("A_{stage}_{ID} ;\n".format(stage=stage, ID=N-1))
	fout.write("}\n")
	
	fout.write("EXPRS {\n\n")
	for i in range(N-1):
		lhs = "A_{stage}_{ID}".format(stage=stage, ID=i+1)
		rhs = "{expr0} + {expr1} ;\n".format(expr0 = A[i], expr1 = A[i+1])
		fout.write("{lhs} rnd64 = {rhs} ;\n".format(lhs=lhs, rhs=rhs));
		A[i+1] = lhs
	fout.write("}\n")
	

if __name__ == "__main__":
	N=int(sys.argv[1])
	serial_reduction(N)

	fout = open("Reduction_"+str(N)+".txt", 'w')
	fchain = open("ChainSum_"+str(N)+".txt", 'w')
	parallel_reduction(N,2)
	parallel_reduction_symbolic(N, fout)
	serial_symbolic(N, fchain)
	fout.close()
	fchain.close()
	
	
