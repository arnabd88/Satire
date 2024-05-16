
import sys

def cholesky(A, N, fout):

	# symmetric inputs
	for i in range(0, N):
		for j in range(0, i):
			e_lhs = A[i][j]
			e_rhs = A[j][i]
			fout.write(f"{e_lhs} rnd64 = {e_rhs};\n")

	for i in range(0, N):
		x = A[i][i]

		e_lhs = f"L_{i}_{i}"
		p = f'1/({e_lhs})'

		x_sum = '-'.join(f'({A[i][j]}*{A[i][j]})' for j in range(0,i))
		e_rhs =  f"sqrt({A[i][i]} - {x_sum})" if x_sum else f"sqrt({A[i][i]})"

		fout.write(f"{e_lhs} rnd64 = {e_rhs};\n")

		for j in range(i+1, N):
			x = A[i][j]
			for k in range(0, i):
				x = x + "-" + A[j][k] + "*" + A[i][k]
			A[j][i] = "(" + x + ")*" + p

			e_lhs = f"L_{j}_{i}"

			e_rhs = A[j][i]

			A[j][i] = e_lhs

			fout.write(f"{e_lhs} rnd64 = {e_rhs};\n")

if __name__ == "__main__":

	N = int(sys.argv[1])

	A = [[f'A_{i}_{j}' for j in range(0,N)] for i in range(0,N)]

	fout = open("cholesky_"+str(N)+".txt", 'w')

	fout.write("INPUTS {\n")
	for i in range(0,N):
		for j in range(i, N):
			x = 2*N - 2*abs(i-j) + i+j
			xmin = x - 0.25
			xmax = x + 0.25
			fout.write(f"\t A_{i}_{j}\t fl64: ({xmin}, {xmax});\n")
	fout.write("}\n\n")

	fout.write("OUTPUTS {\n")
	for i in range(0,N):
		for j in range(i,N):
			fout.write(f"L_{j}_{i};\n")
	fout.write("}\n")

	fout.write("EXPRS {\n")
	cholesky(A, N, fout)
	fout.write("}\n")

	fout.close()
