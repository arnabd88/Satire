
import sys

def seidel2d(A, N, fout):
	
	for t in range(1, T+1):
		for i in range(1, N-1):
			for j in range(1, N-1):
				a_lhs = "{a_i_j_t}".format(a_i_j_t = "A_"+str(i)+"_"+str(j)+"_"+str(t))

				a_rhs = "({a_im1_jm1} + {a_im1_j} + {a_im1_jp1} + \
				          {a_i_jm1} + {a_i_j} + {a_i_jp1} + \
						  {a_ip1_jm1} + {a_ip1_j} + {a_ip1_jp1})/9.0 ;".format ( \
						  	a_im1_jm1 = A[i-1][j-1], \
						  	a_im1_j = A[i-1][j], \
						  	a_im1_jp1 = A[i-1][j+1], \
							a_i_jm1 = A[i][j-1], \
							a_i_j = A[i][j], \
							a_i_jp1 = A[i][j+1], \
							a_ip1_jm1 = A[i+1][j-1], \
							a_ip1_j = A[i+1][j], \
							a_ip1_jp1 = A[i+1][j+1] \
						  )
				A[i][j] = a_lhs
				fout.write(a_lhs + " rnd64 = " + a_rhs + "\n")

if __name__ == "__main__":

	N = int(sys.argv[1])
	T = int(sys.argv[2])

	A = [['A_'+str(i)+'_'+str(j) for j in range(0,N)] for i in range(0, N)]

	fout = open("seidel2d_"+str(N)+"_"+str(T)+".txt",'w')

	fout.write("INPUTS {\n")
	for i in range(0,N):
		for j in range(0, N):
			fout.write("\t A_"+str(i)+"_"+str(j)+"\t fl64 : (-1.0, 1.0);\n")
	fout.write("}\n\n")

	fout.write("OUTPUTS {\n")
	fout.write("A_"+str(int(N/2))+"_"+str(int(N/2))+"_"+str(T)+";\n")
	fout.write("}\n")

	fout.write("EXPRS {\n")
	seidel2d(A, N, fout)
	fout.write("}\n")

	fout.close()



