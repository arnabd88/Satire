
import sys

def cholesky(A, N, fout):

	for i in range(0, N):
		x = A[i][i]

		for j in range(0, i):
			x = x + "-" + A[i][j]+"*"+A[i][j]
		p = "1.0/sqrt(" + x + ")"

		for j in range(i+1, N):
			x = A[i][j]
			for k in range(0, i-1):
				x = x + "-" + A[j][k] + "*" + A[i][k]
			A[j][i] = x + "*" + p

			e_lhs = "{a_j_i_i}".format(a_j_i_i = "A_"+str(j)+"_"+str(i)+"_"+str(i))

			e_rhs = "{a_j_i_rhs}".format(a_j_i_rhs = A[j][i])

			A[j][i] = e_lhs

			fout.write(e_lhs + " rnd64 = " + e_rhs + "\n")

if __name__ == "__main__":

	N = int(sys.argv[1])

	A = [['A_'+str(i)+'_'+str(j)+'_f' for j in range(0,N)] for i in range(0,N)]

	fout = open("cholesky_"+str(N)+".txt", 'w')

	fout.write("INPUTS {\n")
	for i in range(0,N):
		for j in range(0, N):
			fout.write("\t A_"+str(i)+"_"+str(j)+"_f\t fl64: (1.0, 2.0);\n")
	fout.write("}\n\n")

	fout.write("EXPRS {\n")
	cholesky(A, N, fout)
	fout.write("}\n")

	fout.write("OUTPUTS {\n")
	fout.write(A[N-1][N-2]+";\n")
	fout.write("}\n")

	fout.close()
