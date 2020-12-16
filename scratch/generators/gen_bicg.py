import sys
	
def	bicg(N, A, s, q, p , r, fout):

	for i in range(0, N):
		
		for j in range(0, N):

			s[j] = s[j] + "+" + r[i] + "*" + A[i][j] 
			q[i] = q[i] + "+" + p[j] + "*" + A[i][j]

			sj_lhs = "{sj_lhs_i}".format(sj_lhs_i = "s_j"+str(j)+"_i"+str(i))
			sj_rhs = s[j]

			qi_lhs = "{qi_lhs_j}".format(qi_lhs_j = "q_i"+str(i)+"_j"+str(j))
			qi_rhs = q[i]

			s[j] = sj_lhs 
			q[i] = qi_lhs

			fout.write(sj_lhs + " rnd64 = " + sj_rhs + ";\n")
			fout.write(qi_lhs + " rnd64 = " + qi_rhs + ";\n")
		

if __name__ == "__main__":
	
	N = int(sys.argv[1])

	A = [['A_'+str(i)+'_'+str(j) for j in range(0,N)] for i in range(0, N)]
	s = ['s_'+str(j) for j in range(0,N)] 
	q = ['q_'+str(i) for i in range(0,N)] 
	p = ['p_'+str(j) for j in range(0,N)] 
	r = ['r_'+str(i) for i in range(0,N)] 

	fout = open("bicg_"+str(N)+"_"+".txt", 'w')

	fout.write("INPUTS {\n");
	for i in range(0,N):
		for j in range(0, N):
			fout.write("\t A_"+str(i)+"_"+str(j)+"\t fl64 : (0.0001, 1.0);\n")

	for i in range(0,N):
		fout.write("\t r_"+str(i)+ "\t fl64 : (1.0, 2.0); \n")
		fout.write("\t p_"+str(i)+ "\t fl64 : (1.0, 2.0); \n")
		fout.write("\t s_"+str(i)+ "\t fl64 : (0.0, 0.0); \n")
		fout.write("\t q_"+str(i)+ "\t fl64 : (0.0, 0.0); \n")
	fout.write("}\n");


	fout.write("OUTPUTS {\n")
	fout.write("}\n")

	fout.write("EXPRS {\n")
	bicg(N, A, s, q, p , r, fout)
	fout.write("}\n")



