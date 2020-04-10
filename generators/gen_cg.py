
import sys
import copy

if __name__ == "__main__":
	filename = sys.argv[1]
	N = int(sys.argv[2])
	tagname = sys.argv[3]
	err = float(sys.argv[4])


	## Read-in the A matrix
	A = [[0]*N for i in range(N)]
	b = [0]*N
	lines = open(filename, 'r').read().splitlines()
	for i in range(0,N*N):
		line = lines[i]
		[row,col,val] = line.split(':')
		A[int(row)][int(col)] = float(val)
	for i in range(N*N, N*N+N):
		line = lines[i]
		[row, val] = line.split(':')
		b[int(row)] = float(val)


	

	dumpStr = ""
	k = 0
	R = [[0]*N for i in range(2)]
	P = [[0]*N for i in range(2)]
	for i in range(0, N):
		rhs_matvec_i = "b_{idx}".format(idx=i) + "-" + "+".join(["A_{idx}_{jdy}*x_{kid}_{jdy}".format(kid=str(k), idx=str(i), jdy=j) for j in range(N)])
		lhs_matvec_i = "r_{kid}_{idx}".format(kid=str(k), idx=i)
		R[0][i] = lhs_matvec_i ;
		dumpStr += lhs_matvec_i + " rnd64 = " + rhs_matvec_i + ";\n"

	## alpha = r^T r
	rhs_RTR = "+".join(["{Ri}*{Ri}".format(Ri = R[0][i]) for i in range(N)])
	lhs_RTR = "rtr_{kid}".format(kid=k)
	dumpStr += lhs_RTR + " rnd64 = " + rhs_RTR + ";\n"

	rhs_AR = [0]*N

	for i in range(0, N):
		rhs_AR_i = "+".join(["A_{idx}_{jdy} * {Ri}".format(idx = str(i), jdy = str(j), Ri = R[0][i]) for j in range(N)])
		lhs_AR_i = "AR_{kid}_{idx}".format(kid=str(k), idx=i)

		rhs_AR[i] = lhs_AR_i
		dumpStr += lhs_AR_i + " rnd64 = " + rhs_AR_i + ";\n"

	rhs_RAR = "+".join(["{Ri}*{ARi}".format(Ri = R[0][i], ARi = rhs_AR[i]) for i in range(N)])
	lhs_RAR = "rar_{kid}".format(kid=k)
	dumpStr += lhs_RAR + " rnd64 = " + rhs_RAR + ";\n"

	rhs_alpha = "({numer})/({denom})".format(numer = lhs_RTR, denom = lhs_RAR)
	lhs_alpha = "alpha_{kid}".format(kid = k)
	dumpStr += lhs_alpha + " rnd64 = " + rhs_alpha + ";\n"

	for i in range(N):
		rhs_x = "x_{kid}_{idx} + {alpha}*{Rid}".format(alpha = lhs_alpha, kid = k, idx = i, Rid = R[0][i])
		lhs_x = "x_{kpid}_{idx}".format(kpid = str(k+1), idx = str(i))
		dumpStr += lhs_x + " rnd64 = " + rhs_x + ";\n"

	## update next residue r1

	for i in range(0, N):
		rhs_next_residue = "{Rid} - {alpha}*{ARi}".format(Rid=R[0][i], alpha=lhs_alpha, ARi = rhs_AR[i])
		lhs_next_residue = "r_{kpid}_{idx}".format(kpid = k+1, idx= i)
		R[1][i] = lhs_next_residue

		dumpStr += lhs_next_residue + " rnd64 = " + rhs_next_residue + ";\n"

	rhs_r1tr1 = "+".join(["{R1id}*{R1id}".format(R1id = R[1][i]) for i in range(N)])
	lhs_r1tr1 = "r1tr1_{kid}".format(kid=k)
	dumpStr += lhs_r1tr1 + " rnd64 = " + rhs_r1tr1 + ";\n"
	rhs_r0tr0 = "+".join(["{R0id}*{R0id}".format(R0id = R[0][i]) for i in range(N)])
	lhs_r0tr0 = "r0tr0_{kid}".format(kid=k)
	dumpStr += lhs_r0tr0 + " rnd64 = " + rhs_r0tr0 + ";\n"


	rhs_beta = "({numer})/({denom})".format(numer=lhs_r1tr1, denom=lhs_r0tr0)
	lhs_beta = "beta_{kid}".format(kid=k)
	dumpStr += lhs_beta + " rnd64 = " + rhs_beta + ";\n"

	P = copy.deepcopy(R)

	for i in range(0, N):
		rhs_next_p = "{R1id} + {beta}*{p0id}".format(R1id = R[1][i], beta=lhs_beta, p0id=P[0][i])
		lhs_next_p = "p_{kpid}_{idx}".format(kpid = k+1, idx=i)
		P[1][i] = lhs_next_p
		dumpStr += lhs_next_p + " rnd64 = " + rhs_next_p + ";\n"

	#################### Next Iteration ###################
	P[0] = P[1]
	R[0] = R[1]
	k = 1

	rhs_RTR = "+".join(["{Ri}*{Ri}".format(Ri = R[0][i]) for i in range(N)])
	lhs_RTR = "rtr_{kid}".format(kid=k)
	dumpStr += lhs_RTR + " rnd64 = " + rhs_RTR + ";\n"

	rhs_AP = [0]*N

	for i in range(0, N):
		rhs_AP_i = "+".join(["A_{idx}_{jdy} * {Pi}".format(idx = str(i), jdy = str(j), Pi = P[0][i]) for j in range(N)])
		lhs_AP_i = "AP_{kid}_{idx}".format(kid=str(k), idx=i)

		rhs_AP[i] = lhs_AP_i
		dumpStr += lhs_AP_i + " rnd64 = " + rhs_AP_i + ";\n"

	rhs_PAP = "+".join(["{Pi}*{APi}".format(Pi = P[0][i], APi = rhs_AP[i]) for i in range(N)])
	lhs_PAP = "pap_{kid}".format(kid=k)
	dumpStr += lhs_PAP + " rnd64 = " + rhs_PAP + ";\n"


	rhs_alpha = "({numer})/({denom})".format(numer = lhs_RTR, denom = lhs_PAP)
	lhs_alpha = "alpha_{kid}".format(kid = k)
	dumpStr += lhs_alpha + " rnd64 = " + rhs_alpha + ";\n"

	for i in range(N):
		rhs_x = "x_{kid}_{idx} + {alpha}*{Rid}".format(alpha = lhs_alpha, kid = k, idx = i, Rid = R[0][i])
		lhs_x = "x_{kpid}_{idx}".format(kpid = str(k+1), idx = str(i))
		dumpStr += lhs_x + " rnd64 = " + rhs_x + ";\n"

	## update next residue r1

	for i in range(0, N):
		rhs_next_residue = "{Rid} - {alpha}*{APi}".format(Rid=R[0][i], alpha=lhs_alpha, APi = rhs_AP[i])
		lhs_next_residue = "r_{kpid}_{idx}".format(kpid = k+1, idx= i)
		R[1][i] = lhs_next_residue

		dumpStr += lhs_next_residue + " rnd64 = " + rhs_next_residue + ";\n"

	rhs_r1tr1 = "+".join(["{R1id}*{R1id}".format(R1id = R[1][i]) for i in range(N)])
	lhs_r1tr1 = "r1tr1_{kid}".format(kid=k)
	dumpStr += lhs_r1tr1 + " rnd64 = " + rhs_r1tr1 + ";\n"
	rhs_r0tr0 = "+".join(["{R0id}*{R0id}".format(R0id = R[0][i]) for i in range(N)])
	lhs_r0tr0 = "r0tr0_{kid}".format(kid=k)
	dumpStr += lhs_r0tr0 + " rnd64 = " + rhs_r0tr0 + ";\n"
	#r1tr1 = "+".join(["{R1id}*{R1id}".format(R1id = R[1][i]) for i in range(N)])
	#r0tr0 = "+".join(["{R0id}*{R0id}".format(R0id = R[0][i]) for i in range(N)])

	rhs_beta = "({numer})/({denom})".format(numer=lhs_r1tr1, denom=lhs_r0tr0)
	lhs_beta = "beta_{kid}".format(kid=k)
	dumpStr += lhs_beta + " rnd64 = " + rhs_beta + ";\n"

	for i in range(0, N):
		rhs_next_p = "{R1id} + {beta}*{p0id}".format(R1id = R[1][i], beta=lhs_beta, p0id=P[0][i])
		lhs_next_p = "p_{kpid}_{idx}".format(kpid = k+1, idx=i)
		P[1][i] = lhs_next_p
		dumpStr += lhs_next_p + " rnd64 = " + rhs_next_p + ";\n"

	#################### Next Iteration ###################
	#  P[0] = P[1]
	#  R[0] = R[1]
	#  k = 2

	outfile = "CG_"+tagname+"_K"+str(k+1)+"_N"+str(N)+".txt"
	fout = open(outfile, 'w')

	## Print the inputs ##
	fout.write("INPUTS {\n")
	for i in range(N):
		for j in range(N):
			val = A[i][j]
			var = "A_{idx}_{jdy}".format(idx=i, jdy=j)
			if val == 0:
				fout.write("\t"+var+"\t fl64 : ("+str(val)+" , "+str(val)+");\n")
			else:
				fout.write("\t"+var+"\t fl64 : ("+str(val-err)+" , "+str(val+err)+");\n")
		bval = str(b[i])
		bvar = "b_{idx}".format(idx=i)
		fout.write("\t"+bvar+"\t fl64 : ("+bval+" , "+bval+");\n")
		bvar = "x_0_{idx}".format(idx=i)
		fout.write("\t"+bvar+"\t fl64 : (0.0 , 0.0);\n")
			
	fout.write("}\n\n")


	fout.write("OUTPUTS {\n\n")
	fout.write("}\n\n")

## print the matvec operation between A and x

	fout.write("EXPRS {\n\n")
	fout.write(dumpStr)
	fout.write("}\n\n")

	fout.close()

	print(dumpStr)


