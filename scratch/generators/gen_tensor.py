

import sys
import re

# M=blocksize only controls the free dimensions
def gen_tensor_data(NA, NB, a_filename, b_filename, M, numBlocks, nameTag):

	fp_a_str = open(a_filename, "r").read()#.split(' ')# .remove('\n')
	fp_a_str = re.sub(r'\,', "", fp_a_str)
	fp_a = fp_a_str.split(' ')
	fp_a.remove('\n')

	fp_b_str = open(b_filename, "r").read()#.split(' ')# .remove('\n')
	fp_b_str = re.sub(r'\,', "", fp_b_str)
	fp_b = fp_b_str.split(' ')
	fp_b.remove('\n')

	A_start_locs = [((10+M*i)*NA[3]*NA[2]*NA[1] + (10+M*i)*NA[3]*NA[2] ) for i in range(numBlocks)]
	B_start_locs = [( (10+M*i)*NB[3] + (10+M*i)) for i in range(numBlocks)]
	print(A_start_locs)
	print(B_start_locs)
	for num in range(numBlocks):
		outfile = nameTag+"_"+str(num)+".txt"
		fout = open(outfile, 'w')
		astart,bstart = A_start_locs[num], B_start_locs[num]

		SA = [[[[0]*NA[3] for i in range(NA[2])] for j in range(M)] for k in range(M)]
		SB = [[[[0]*M for i in range(M)] for j in range(NB[1])] for k in range(NB[0])]

		## collect A:
		## Track the interval range per free variable
		A_intv = [[[0.0,0.0] for i in range(M)] for j in range(M)]
		print("A -> ", len(SA), len(SA[0]), len(SA[0][0]), len(SA[0][0][0]))
		for i in range(0, M):
			for j in range(0, M):
				for k in range(0,NA[2]):
					for w in range(0, NA[3]):
						SA[i][j][k][w] = float(fp_a[astart + (i*NA[3]*NA[2]*NA[1] + j*NA[3]*NA[2] + k*NA[3] + w)])
						A_intv[i][j][0] = min(A_intv[i][j][0], SA[i][j][k][w])
						A_intv[i][j][1] = max(A_intv[i][j][1], SA[i][j][k][w])
						#print(i,j,k,w,"-->", SA[i][j][k][w])

		## collect B:
		B_intv = [[[0.0,0.0] for i in range(M)] for j in range(M)]
		print("B -> ", len(SB), len(SB[0]), len(SB[0][0]), len(SB[0][0][0]))
		for i in range(0, NB[0]):
			for j in range(0, NB[1]):
				for k in range(0, M):
					for w in range(0, M):
						#print(bstart, (i*NB[3]*NB[2]*NB[1] + j*NB[3]*NB[2] + k*NB[3] + w))
						SB[i][j][k][w] = float(fp_b[bstart + (i*NB[3]*NB[2]*NB[1] + j*NB[3]*NB[2] + k*NB[3] + w)])
						B_intv[k][w][0] = min(A_intv[k][w][0], SB[i][j][k][w])
						B_intv[k][w][1] = max(A_intv[k][w][1], SB[i][j][k][w])
						#print(i,j,k,w,"-->", SB[i][j][k][w])

		## write the inputs from A and B
		fout.write("INPUTS  {\n\n")
		#A
		for i in range(0, M):
			for j in range(0, M):
				for k in range(0,NA[2]):
					for w in range(0, NA[3]):
						Ainp = "A_{iv}_{jv}_{kv}_{wv} fl64 : ({lb}, {ub});".format( \
							iv = i, jv = j, kv = k, wv = w, lb = str(A_intv[i][j][0]), ub = str(A_intv[i][j][1]) \
						)
						fout.write(Ainp+"\n")
		#B
		for i in range(0, NB[0]):
			for j in range(0, NB[1]):
				for k in range(0,M):
					for w in range(0, M):
						Binp = "B_{iv}_{jv}_{kv}_{wv} fl64 : ({lb}, {ub});".format( \
							iv = i, jv = j, kv = k, wv = w, lb = str(B_intv[k][w][0]), ub = str(B_intv[k][w][1]) \
						)
						print(Binp+"\n")
						fout.write(Binp+"\n")
		fout.write("}\n")

		#C
		fout.write("OUTPUTS {\n\n")
		for i in range(0,M):
			for j in range(0, M):
				for K in range(0, M):
					for w in range(0, M):
						Cout = "C_{iv}_{jv}_{kv}_{wv} ;".format( \
							iv = i, jv = j, kv = k, wv = w) 
						fout.write(Cout+"\n")
		fout.write("}\n\n")

		#Exprs
		fout.write("EXPRS {\n\n")
		for i in range(0,M):
			for j in range(0, M):
				for k in range(0, M):
					for w in range(0, M):
						c_rhs = '+'.join(['+'.join(["A_{iv}_{jv}_{pv}_{qv} * B_{pv}_{qv}_{kv}_{wv}".format(\
									iv = i, \
									jv = j, \
									kv = k, \
									wv = w, \
									pv = p, \
									qv = q
								) for p in range(NA[3])]) for q in range(NA[2])])
						#print(c_rhs)

						c_lhs = "C_{iv}_{jv}_{kv}_{wv} ".format( \
							iv = i, jv = j, kv = k, wv = w)
						fout.write(c_lhs+" rnd64 = "+c_rhs+";\n")
								

		fout.write("}\n")
				

		## for the data, scan along one lower dimension of A and replace with an interval




if __name__ == "__main__":
	NA = [35,35,35,35]
	NB = [35,35,29,29]
	a_filename = sys.argv[1] ## A -> 35x35x35x35
	b_filename = sys.argv[2] ## B -> 35x35x29x29

	M = int(sys.argv[3])     ## generator block sizes
	num = int(sys.argv[4])   ## number of blocks to be extracted

	nameTag = sys.argv[5]

	gen_tensor_data(NA, NB, a_filename, b_filename, M, num, nameTag)

