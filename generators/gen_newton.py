import sys

def newton(n, fout):

	# f = x^3 + x -1
	# fp = 3*x^2 + 1

	x = 'x_0'

	for i in range(n):
		lhs = 'x_'+str(i+1)

		rhs = "{xprev} - (({feval})/({fpeval}));".format( \
					xprev = x, \
					feval = "{xprev}*{xprev}*{xprev} + {xprev} +1".format(xprev = x), \
					fpeval = "3*{xprev}*{xprev} +1".format(xprev = x) \
				)

		fout.write(lhs + " rnd64 = " + rhs + "\n")

		x = lhs


if __name__ == "__main__":
	n = int(sys.argv[1])

	fout = open("newton_"+str(n)+".txt", 'w')

	fout.write("INPUTS {\n")
	fout.write("x_0 fl64 : (1,2);" )
	fout.write("}\n")

	fout.write("OUTPUTS {\n")
	fout.write("x_"+str(n)+";")
	fout.write("}\n")

	fout.write("EXPRS {\n")
	newton(n, fout)
	fout.write("}\n")

	fout.close()
