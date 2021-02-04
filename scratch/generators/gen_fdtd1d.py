
import sys


def fdtd1d(E, H, N, T, fout):

	for t in range(1,T+1):
		
		for i in range(1,N):
			e_lhs = "{e_i_t}".format(e_i_t = "E_"+str(i)+"_"+str(t))

			e_rhs = "({e_i} - 0.5*({h_i} - {h_im1}));".format( \
						e_i = E[i], \
						h_i = H[i], \
						h_im1 = H[i-1] \
					  )

			E[i] = e_lhs

			fout.write(e_lhs + " rnd64 = " + e_rhs + "\n")

		for i in range(0,N):
			h_lhs = "{h_i_t}".format(h_i_t = "H_"+str(i)+"_"+str(t))

			h_rhs = "({h_i} - 0.7*({e_ip1} - {e_i}));".format( \
						h_i = H[i], \
						e_ip1 = E[i+1], \
						e_i = E[i] \
					 )

			H[i] = h_lhs

			fout.write(h_lhs + " rnd64 = " + h_rhs + "\n")


if __name__ == "__main__":

	N = int(sys.argv[1])
	T = int(sys.argv[2])

	E = ['E_'+str(i)+'_0' for i in range(0,N+1)]
	H = ['H_'+str(i)+'_0' for i in range(0,N)]

	fout = open("fdtd1d_"+str(N)+"_"+str(T)+".txt",'w')

	fout.write("INPUTS {\n")

	block_cnt = 0
	for i in range(0, N+1):
		
		lb = '0.0' #str(float(i-block_cnt)/N)
		ub = '1.0' #str(float(i-block_cnt+20)/N)
		block_cnt += 1
		
		fout.write("\t E_"+str(i)+"_0\t fl64 :  ("+lb+" , "+ub+");\n")
		if(i < N):
			fout.write("\t H_"+str(i)+"_0\t fl64:  ("+lb+" , "+ub+");\n")

		if block_cnt==5:
			block_cnt = 0

	fout.write("}\n\n")
		
	fout.write("OUTPUTS {\n")
	#fout.write("E_"+str(int(N/2))+"_"+str(T)+";\n")
	fout.write("H_"+str(int(N/2))+"_"+str(T)+";\n")
	fout.write("}\n")

	fout.write("EXPRS {\n")
	fdtd1d(E, H, N, T, fout)
	fout.write("}\n")

	fout.close()



