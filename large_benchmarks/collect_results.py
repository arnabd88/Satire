

import sys
import glob

fout = open("Results.txt", 'w')

configs = ['noAbs', '10_20', '15_25', '20_40']
Message = {'noAbs' : 'Without Abstraction ', \
		   '10_20' : 'Abstraction window (10,20) ',\
		   '15_25' : 'Abstraction window (15,25) ',\
		   '20_40' : 'Abstraction window (20,40) ' }

BenchmarkNames = {'poisson2d0' : 'P0', \
				  'poisson2d1_t32' : 'P1', \
				  'poisson2d2_t32' : 'P2', \
				  'convecdiff2d0' : 'C0', \
				  'convecdiff2d1_t32' : 'C1', \
				  'convecdiff2d2_t32' : 'C2', \
				  'heat2d0_t32' : 'H0', \
				  'heat2d1_t32' : 'H1', \
				  'heat2d2_t32' : 'H2', \
				  'advect3d' : 'Advection3D', \
				  'fdtd1d_t64' : 'FDTD', \
				  'lorentz20' : 'lorenz20', \
				  'lorentz40' : 'lorenz40', \
				  'lorentz70' : 'lorenz70', \
				  'matmul64' : 'Matrix Multiplication - 64x64', \
				  'matmul128' : 'Matrix Multiplication - 128x128', \
				  'FFT_1024' : 'FFT_1024', \
				  'FFT_4096pt' : 'FFT_4096', \
				  'Scan_1024' : 'Scan_1024(Prefix sum)', \
				  'Scan_4096' : 'Scan_4096(Prefix Sum)', \
				  'CG_Arc' : 'Conjugate gradient (ARC130)', \
				  'CG_Pores' : 'COnjugate gradient (Pores)', \
				  'var_ccsd_type2_0' : 'Tensor Contraction-type0', \
				  'var_ccsd_type2_1' : 'Tensor Contraction-type1', \
				  'ccsd_type2_0' : 'Tensor Contraction-type0 (Degenerate Intervals)', \
				  'ccsd_type2_1' : 'Tensor Contraction-type1 (Degenerate Intervals)' }

test_name = sys.argv[1]
print(test_name)
fout.write(test_name+"\n")
file_list = list(glob.iglob('*'))

pylog_dict = dict()
outlog_dict = dict()
#print(file_list)
pylog_dict['10_20'] = list(filter( lambda x: 'pylog' in x and '10_20' in x, file_list))
pylog_dict['15_25'] = list(filter( lambda x: 'pylog' in x and '15_25' in x, file_list))
pylog_dict['20_40'] = list(filter( lambda x: 'pylog' in x and '20_40' in x, file_list))
pylog_dict['noAbs'] = list(filter( lambda x: 'pylog' in x and 'noAbs' in x, file_list))

outlog_dict['10_20'] = list(filter(lambda x: 'out' in x and '10_20' in x , file_list))
outlog_dict['15_25'] = list(filter(lambda x: 'out' in x and '15_25' in x , file_list))
outlog_dict['20_40'] = list(filter(lambda x: 'out' in x and '20_40' in x , file_list))
outlog_dict['noAbs'] = list(filter(lambda x: 'out' in x and 'noAbs' in x , file_list))
#print(pylog_dict)
BenchName = BenchmarkNames.get(test_name, test_name)
print("****** Benchmark :", BenchName, "**************")
fout.write("****** Benchmark : {bench} **************\n".format(bench=BenchName))
for conf in configs:
	if (len(pylog_dict[conf]) == 0):
		print(Message[conf], "did not execute \n")
		fout.write("{message} -- did not execute \n".format(message=Message[conf]))
	else:
		pylogname = pylog_dict[conf][0]
		outlogname = outlog_dict[conf][0]
		#print(pylogname, outlogname)
		logfile = open(pylogname, 'r').read().splitlines()
		outfile = open(outlogname, 'r').read().splitlines()
		AST_DEPTH = list(filter(lambda x: "AST_DEPTH" in x, logfile))
		ABSOLUTE_ERROR = list(filter(lambda x: "ABSOLUTE_ERROR" in x, outfile))
		EXECUTION_TIME = list(filter(lambda x: "Full time" in x, outfile))

		error = max(list(map(lambda x : float(x.split(':')[1]), ABSOLUTE_ERROR)))

		print("\t",Message[conf], "->", "execution time :", EXECUTION_TIME[0])
		print("\t",Message[conf], "->", "absolute error :", error)
		fout.write("\t {message} -->  execution time = {exec_time}\n".format(message=Message[conf], exec_time=EXECUTION_TIME[0]))
		fout.write("\t {message} -->  absolute error = {abs_err}\n\n\n".format(message=Message[conf], abs_err=error))


fout.close()
