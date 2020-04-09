
import numpy as np
import cmath as cm
import copy
import sys

def omega(k, j):
	w = cm.exp(complex(0, -1.0*j*2*np.pi/pow(2,k)))
	return w


def reverse(n, j):
	reverse_num = 0
	for i in range(0, n):
		temp = (j & (1 << i))
		if(temp):
			reverse_num |= ( 1 << (n-1-i))

	return reverse_num

def OneStep(x, k, n, fout):
	N = pow(2, n)
	block_size = int(pow(2, k))
	num_blocks = int(N/block_size)
	y = copy.deepcopy(x)

	dumpStr = ''

	for block_number in range(0, num_blocks):
		first_index = block_number * block_size
		for j in range(0, int(block_size/2)):
			j1 = j + first_index
			j2 = j1 + int(block_size/2)

			wkj = omega(k, j)
			wkj_r , wkj_i = wkj.real , wkj.imag
			### eval yj1 ###
			#xj2_r, xj2_i = x[j2][0], x[j2][1]
			#xj1_r, xj1_i = x[j1][0], x[j1][1]

			#yj1_r = xj1_r + (wkj_r*xj2_r - wkj_i*xj2_i)
			#yj1_i = xj1_i + (wkj_i*xj2_r + wkj_r*xj2_i)

			#yj2_r = xj1_r - (wkj_r*xj2_r - wkj_i*xj2_i)
			#yj2_i = xj1_i - (wkj_i*xj2_r + wkj_r*xj2_i)

			uniqueId = "{level}_{blkNum}".format(
								level = k, \
								blkNum = block_number \
							)

			yj1_r_lhs = "X_{iden}_{index}_real".format( index=str(j1), iden = uniqueId )
			yj1_i_lhs = "X_{iden}_{index}_imag".format( index=str(j1), iden = uniqueId )

			yj2_r_lhs = "X_{iden}_{index}_real".format( index=str(j2), iden = uniqueId )
			yj2_i_lhs = "X_{iden}_{index}_imag".format( index=str(j2), iden = uniqueId )

			yj1_r_rhs = "({xj1_real} + (({wkj_real})*({xj2_real}) - ({wkj_imag})*({xj2_imag})));".format( \
							wkj_real = str(wkj.real), \
							wkj_imag = str(wkj.imag), \
							xj1_real = x[j1][0], \
							xj2_real = x[j2][0], \
							xj2_imag = x[j2][1] \
							)

			yj1_i_rhs = "({xj1_imag} + (({wkj_imag})*({xj2_real}) + ({wkj_real})*({xj2_imag})));".format( \
							wkj_real = str(wkj.real), \
							wkj_imag = str(wkj.imag), \
							xj1_imag = x[j1][1], \
							xj2_real = x[j2][0], \
							xj2_imag = x[j2][1] \
							)

			yj2_r_rhs = "({xj1_real} - (({wkj_real})*({xj2_real}) - ({wkj_imag})*({xj2_imag})));".format( \
							wkj_real = str(wkj.real), \
							wkj_imag = str(wkj.imag), \
							xj1_real = x[j1][0], \
							xj2_real = x[j2][0], \
							xj2_imag = x[j2][1] \
							)

			yj2_i_rhs = "({xj1_imag} - (({wkj_imag})*({xj2_real}) + ({wkj_real})*({xj2_imag})));".format( \
							wkj_real = str(wkj.real), \
							wkj_imag = str(wkj.imag), \
							xj1_imag = x[j1][1], \
							xj2_real = x[j2][0], \
							xj2_imag = x[j2][1] \
							)

			dumpStr += yj1_r_lhs+" = "+yj1_r_rhs+"\n"
			dumpStr += yj1_i_lhs+" = "+yj1_i_rhs+"\n"
			dumpStr += yj2_r_lhs+" = "+yj2_r_rhs+"\n"
			dumpStr += yj2_i_lhs+" = "+yj2_i_rhs+"\n"

			y[j1] = [yj1_r_lhs, yj1_i_lhs]
			y[j2] = [yj2_r_lhs, yj2_i_lhs]

	fout.write(dumpStr+"\n")

	return y



def fftStr( n, fout):

	N = pow(2, n)
	x = []
	fout.write("INPUTS {\n")
	for i in range(0,N):
		xi_r = "x"+str(i)
		xi_i = str(0.0)
		x.append([xi_r, xi_i])
		fout.write(xi_r+" : (-1,1);\n")
	fout.write("}\n\n")
	

	y = copy.deepcopy(x)

	for j in range(0, N):
		y[j] = x[reverse(n,j)]
	for k in range(1, n+1):
		y = OneStep(y, k, n, fout)

	dumpStr = ''
	fout.write("OUTPUTS {\n")
	for yf in y:
		dumpStr += "{out_real} ;\n".format(out_real = yf[0])
	fout.write(dumpStr+"\n}\n")



if __name__ == "__main__":
	n = int(sys.argv[1])
	N = pow(2,n)
	fout = open("fft_"+str(N)+"pt.txt", 'w')
	fftStr(n, fout)

	fout.close()
