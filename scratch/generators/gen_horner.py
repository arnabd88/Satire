import sys
import random
import copy


def polynom(N, B, fout):

	A = copy.deepcopy(B)

	fout.write("INPUTS {\n\n")
	fout.write("\t x fl64 : (-1.0, 1.0) ;\n")
	fout.write("}\n")

	Acc = []

	fout.write("OUTPUTS {\n\n")
	fout.write("\t Final ;\n")
	fout.write("}\n")

	fout.write("EXPRS {\n\n")
	
	for n in range(N,0,-1):
		
		lhs = "S_{ND}".format(ND=n)
		rhs = "({coeff}*{polyn})".format(coeff = A[n], polyn = "( "+" * ".join(["x" for i in range(n)])+" )")
		fout.write("{lhs} rnd64 = {rhs} ;\n".format(lhs=lhs, rhs=rhs))
		Acc.append(lhs)

	fout.write("Final rnd64 = {a0} + {acc} ;\n".format(a0=A[0], acc="+".join(Acc)))

	fout.write("}\n")



def horner(N, B, fout):

	A = copy.deepcopy(B)

	fout.write("INPUTS {\n\n")
	fout.write("\t x fl64 : (-1.0, 1.0) ;\n")
	fout.write("}\n")
	

	fout.write("OUTPUTS {\n\n")
	fout.write("\t S_{ND} ;\n".format(ND=0))
	fout.write("}\n")

	fout.write("EXPRS {\n\n")
	
	for n in range(N, 0,-1):
		
		print(n, A)
		lhs = "S_{ND}".format(ND=n-1)
		rhs = "({a_nm1} + x*{a_n})".format(a_nm1 = A[n-1], a_n = A[n])
		fout.write("{lhs} rnd64 = {rhs} ;\n".format(lhs=lhs, rhs=rhs))
		A[n-1] = lhs

	fout.write("}\n")




if __name__ == "__main__":
	
	N = int(sys.argv[1])

	fpoly = open("f_polynomial_"+str(N)+".txt", 'w')
	fhorner = open("f_horner_"+str(N)+".txt", 'w')

	B = [random.uniform(-10.0, 10.0) for i in range(N+1)]
	print(len(B))

	horner(N, B, fhorner)
	polynom(N, B, fpoly)

	fpoly.close()
	fhorner.close()
