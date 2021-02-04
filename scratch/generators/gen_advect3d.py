import sys

# double a[nx+10][ny+10][nz+10];
# double af[nx+10][ny+10][nz+10];
# double ab[nx+10][ny+10][nz+10];
# double al[nx+10][ny+10][nz+10];
# double athird[nx+10][ny+10][nz+10];
# double uxl[nx+10][ny+10][nz+10];
# double uzf[nx+10][ny+10][nz+10];
# double uyb[nx+10][ny+10][nz+10];
#define f60 0.2 
#define f61 0.5
#define f62 0.3

#define halfdtbydx 0.5
#define thirddtbydz 0.3
#define thirddtbydx 0.3
#define thirddtbydy 0.3



def advect3d(A, uxl, uzf, uyb, N, fout):

	AB = [[['0' for k in range(N+10)] \
	                                       for j in range(N+10)] \
										   for i in range(N+10)]

	for j in range(4, N+9-2 +1):
		for i in range(4, N+9-3 +1):
			for k in range(4, N+9-3 +1):
				ab_rhs = """(0.2 * ({a_jm1_i_k} + {a_j_i_k}) + 0.5 * \
				          ({a_jm2_i_k} + {a_jp1_i_k}) + 0.3 * ({a_jm3_i_k} \
						  + {a_jp2_i_k})) * 0.3 * {uyb_j_i_k};""".format (\
						  	a_jm1_i_k = A[j-1][i][k], \
							a_j_i_k   = A[j][i][k], \
							a_jm2_i_k = A[j-2][i][k], \
							a_jp1_i_k = A[j+1][i][k], \
							a_jm3_i_k = A[j-3][i][k], \
							a_jp2_i_k = A[j-2][i][k], \
							uyb_j_i_k = uyb[j][i][k]  \
						  	)

				ab_lhs = "AB_"+str(j)+"_"+str(i)+"_"+str(k)
				AB[j][i][k] = ab_lhs
				#print(ab_lhs + " rnd64 = " + ab_rhs + "\n")
				fout.write(ab_lhs + " rnd64 = " + ab_rhs + "\n")


	AL = [[['0' for k in range(N+10)] \
	                                       for j in range(N+10)] \
										   for i in range(N+10)]

	for j in range(4, N+9-3 +1):
		for i in range(4, N+9-2 +1):
			for k in range(4, N+9-3 +1):
				al_rhs = """(0.2 * ({a_j_im1_k} + {a_j_i_k}) + 0.5 * \
				           ({a_j_im2_k} + {a_j_ip1_k}) + 0.3 * ({a_j_im3_k} \
						   + {a_j_ip2_k})) * 0.3 * {uxl_j_i_k}; """.format ( \
						   	a_j_im1_k = A[j][i-1][k], \
							a_j_i_k   = A[j][i][k], \
							a_j_im2_k = A[j][i-2][k], \
							a_j_ip1_k = A[j][i+1][k], \
							a_j_im3_k = A[j][i-3][k], \
							a_j_ip2_k = A[j][i+2][k], \
							uxl_j_i_k = uxl[j][i][k]  \
						   )

				al_lhs = "AL_"+str(j)+"_"+str(i)+"_"+str(k)
				AL[j][i][k] = al_lhs
				#print(al_lhs + " rnd64 = " + al_rhs + "\n")
				fout.write(al_lhs + " rnd64 = " + al_rhs + "\n")


	AF = [[['0' for k in range(N+10)] \
	                                       for j in range(N+10)] \
										   for i in range(N+10)]

	for j in range(4, N+9-3 +1):
		for i in range(4, N+9-3 +1):
			for k in range(4, N+9-2 +1):
				af_rhs = """(0.2 * ({a_j_i_km1} + {a_j_i_k}) + 0.5 * \
				           ({a_j_i_km2} + {a_j_i_kp1}) + 0.3 * ({a_j_i_km3} \
						   + {a_j_i_kp2})) * 0.3 * {uzf_j_i_k}; """.format ( \
						   	a_j_i_km1 = A[j][i][k-1], \
							a_j_i_k   = A[j][i][k], \
							a_j_i_km2 = A[j][i][k-2], \
							a_j_i_kp1 = A[j][i][k+1], \
							a_j_i_km3 = A[j][i][k-3], \
							a_j_i_kp2 = A[j][i][k+2], \
							uzf_j_i_k = uzf[j][i][k]  \
						   )

				af_lhs = "AF_"+str(j)+"_"+str(i)+"_"+str(k)
				AF[j][i][k] = af_lhs
				#print(af_lhs + " rnd64 = " + af_rhs + "\n")
				fout.write(af_lhs + " rnd64 = " + af_rhs + "\n")
				

	ATHIRD = [[['0' for k in range(N+10)] \
	                                       for j in range(N+10)] \
										   for i in range(N+10)]

	for j in range(4, N+9-3 +1):
		for i in range(4, N+9-3 +1):
			for k in range(4, N+9-3 +1):
				ath_rhs = """{a_j_i_k} + ({al_j_ip1_k} - {al_j_i_k}) \
				          + ({ab_jp1_i_k} - {ab_j_i_k}) + ({af_j_i_kp1} - {af_j_i_k}) ;""".format( \
						  a_j_i_k    = A[j][i][k], \
						  al_j_ip1_k = AL[j][i+1][k], \
						  al_j_i_k   = AL[j][i][k], \
						  ab_jp1_i_k = AB[j+1][i][k], \
						  ab_j_i_k   = AB[j][i][k], \
						  af_j_i_kp1 = AF[j][i][k+1], \
						  af_j_i_k   = AF[j][i][k]  \
						  )

				ath_lhs = "ATHIRD_"+str(j)+"_"+str(i)+"_"+str(k)
				ATHIRD[j][i][k] = ath_lhs
				#print(ath_lhs + " rnd64 = " + ath_rhs + "\n")
				fout.write(ath_lhs + " rnd64 = " + ath_rhs + "\n")



if __name__ == "__main__":

	N = int(sys.argv[1])

	A = [[['A_'+str(i)+'_'+str(j)+'_'+str(k) for k in range(N+10)] \
	                                       for j in range(N+10)] \
										   for i in range(N+10)]

	uxl = [[['uxl_'+str(i)+'_'+str(j)+'_'+str(k) for k in range(N+10)] \
	                                       for j in range(N+10)] \
										   for i in range(N+10)]

	uzf = [[['uzf_'+str(i)+'_'+str(j)+'_'+str(k) for k in range(N+10)] \
	                                       for j in range(N+10)] \
										   for i in range(N+10)]

	uyb = [[['uyb_'+str(i)+'_'+str(j)+'_'+str(k) for k in range(N+10)] \
	                                       for j in range(N+10)] \
										   for i in range(N+10)]

	
	fout = open("advect3d_"+str(N)+".txt", 'w')

	fout.write("INPUTS {\n\n")
	intv_diff = 9.0 ;
	for i in range(N+10):
		for j in range(N+10):
			for k in range(N+10):
				fl = float(i+j+k)/float(N+N+N)
				fu = float(i+j+k+1)/float(N+N+N)
				lb = str(1.0 + fl*intv_diff)
				ub = str(1.0 + fu*intv_diff)
				fout.write(A[i][j][k]+"\t fl64 : ({lb}, {ub});\n".format(lb=lb, ub=ub))
				fout.write(uxl[i][j][k]+"\t fl64 : ({lb}, {ub});\n".format(lb=lb, ub=ub))
				fout.write(uzf[i][j][k]+"\t fl64 : ({lb}, {ub});\n".format(lb=lb, ub=ub))
				fout.write(uyb[i][j][k]+"\t fl64 : ({lb}, {ub});\n".format(lb=lb, ub=ub))
	fout.write("}\n\n")

	fout.write("OUTPUTS {\n\n")
	for j in range(4,N):
		for i in range(4,N):
			for k in range(4,N):
				fout.write("  ATHIRD_{j}_{i}_{k} ;\n".format(j=j, i=i, k=k))
	fout.write("}\n\n")

	fout.write("EXPRS {\n\n")
	advect3d(A, uxl, uzf, uyb, N, fout)
	fout.write("}\n\n")
	fout.close()

	
