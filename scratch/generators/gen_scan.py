
import math
import sys

def scan(x):

	n = len(x)
	depth = int(math.log(n,2))

	## upsweep
	for d in range(1, depth+1):
		pd = 2**d

		for i in range(2**(d-1) -1, n, pd):
			_offset = 2**(d-1)
			x[i+_offset] += x[i]

	## Downsweep
	for d in range(depth, 1, -1):
		pd = 2**(d-1)
		
		for i in range(2**(d-1)-1, n-1, pd):
			_offset = 2**(d-2)
			x[i+_offset] += x[i]

	return x


def scanStr(X, fout):
	
	n = len(X)
	depth = int(math.log(n,2))
	
	## upsweep
	for d in range(1, depth+1):
		pd = 2**d

		for i in range(2**(d-1) -1, n, pd):
			off = 2**(d-1)
			lhs = "{x_up_dep_indoff}".format(x_up_dep_indoff = "X_UP_"+str(d)+"_"+str(i)+"P"+str(off))
			rhs = "({x_up_dep_indoff} + {x_up_dep_ind});".format( \
									x_up_dep_indoff = X[i+off], \
									x_up_dep_ind = X[i] \
									)
			fout.write(lhs +" rnd64 = "+ rhs+"\n")

			X[i+off] = "{lhs_expr}".format(lhs_expr=lhs)

	## Downsweep
	for d in range(depth, 1, -1):
		pd = 2**(d-1)

		for i in range(2**(d-1)-1, n-1, pd):
			off = 2**(d-2)
			lhs = lhs = "{x_dw_dep_indoff}".format(x_dw_dep_indoff = "X_DW_"+str(d)+"_"+str(i)+"P"+str(off))
			rhs = "({x_dw_dep_indoff} + {x_dw_dep_ind});".format( \
									x_dw_dep_indoff = X[i+off], \
									x_dw_dep_ind = X[i] \
									)
			fout.write(lhs +" rnd64 = "+ rhs+"\n")

			X[i+off] = "{lhs_expr}".format(lhs_expr=lhs)



if __name__ == "__main__":
	x = [i for i in range(-10,22,1)]

	print(scan(x))

	d = int(sys.argv[1])
	n = 2**d
	X = ['x_'+str(i) for i in range(n)]

	fout = open("Scan_"+str(n)+".txt", 'w')

	## print inputs
	fout.write("INPUTS {\n")
	for i in range(n):
		fout.write(X[i]+"  fl64 \t: \t(0,1) ;\n")
	fout.write("}\n\n")

	fout.write("EXPRS {\n")
	scanStr(X, fout)
	fout.write("}\n\n")

	fout.write("OUTPUTS {\n")
	for i in range(n):
		fout.write(X[i]+";\n")
	fout.write("}")
	print(X)
	fout.close()
