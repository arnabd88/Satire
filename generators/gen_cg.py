
import sys
import copy

if __name__ == "__main__":
	filename = sys.argv[1]
	N = int(sys.argv[2])
	outfile = "CG_"+str(N)+".txt"
	fout = open(outfile, 'w')

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


	
	## Print the inputs ##
	fout.write("INPUTS {\n")
	for i in range(N):
		for j in range(N):
			val = A[i][j]
			var = "A_{idx}_{jdy}".format(idx=i, jdy=j)
			if val == 0:
				fout.write("\t"+var+"\t fl64 : ("+str(val)+" , "+str(val)+");\n")
			else:
				fout.write("\t"+var+"\t fl64 : ("+str(val-0.5)+" , "+str(val+0.5)+");\n")
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

	r1tr1 = "+".join(["{R1id}*{R1id}".format(R1id = R[1][i]) for i in range(N)])
	r0tr0 = "+".join(["{R0id}*{R0id}".format(R0id = R[0][i]) for i in range(N)])

	rhs_beta = "({numer})/({denom})".format(numer=r1tr1, denom=r0tr0)
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
	k = 2



	print(dumpStr)

	fout.write(dumpStr)

	fout.write("}\n\n")

	fout.close()
