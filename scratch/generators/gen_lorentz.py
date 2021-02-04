
import sys

s = [[0,0,0] for i  in range(8001)]

s[0] = ['x', 'y', 'z']

dt = 0.005
a = 10.0
r = 28.0
b = 2.666667

n = int(sys.argv[1])

fout = open("lorentz_"+str(n)+".txt", 'w')


fout.write("INPUTS {\n")
fout.write('x fl64 \t:\t (0.5,1);\n')
fout.write('y fl64 \t:\t (0.5,1);\n')
fout.write('z fl64 \t:\t (0.5,1);\n')
fout.write("}\n")

fout.write("OUTPUTS {\n")
fout.write("x_"+str(n)+"_0;\n")
fout.write("x_"+str(n)+"_1;\n")
fout.write("x_"+str(n)+"_2;\n")
fout.write("}\n")

fout.write("EXPRS {\n")
for i in range(n):

	lhs0 = 'x_'+str(i+1)+'_0'
	rhs0 = "({s_i_0} + {a}*({s_i_1} - {s_i_0})*{dt});".format( \
			s_i_0 = s[i][0], \
			a = str(a), \
			s_i_1 = s[i][1], \
			dt = dt )

	s[i+1][0] = lhs0

	lhs1 = 'x_'+str(i+1)+'_1'
	rhs1 = "({s_i_1} + ({r}*{s_i_0} - {s_i_1} - {s_i_0}*{s_i_2})*{dt});".format( \
			s_i_0 = s[i][0], \
			s_i_1 = s[i][1], \
			s_i_2 = s[i][2], \
			r = r, \
			dt = dt )
	s[i+1][1] = lhs1

	lhs2 = 'x_'+str(i+1)+'_2'
	rhs2 = "({s_i_2} + ({s_i_0}*{s_i_1} - {b}*{s_i_2})*{dt});".format( \
			s_i_0 = s[i][0], \
			s_i_1 = s[i][1], \
			s_i_2 = s[i][2], \
			b = b, \
			dt = dt )
	s[i+1][2] = lhs2
			
	fout.write(lhs0+" rnd64 = "+rhs0+"\n")
	fout.write(lhs1+" rnd64 = "+rhs1+"\n")
	fout.write(lhs2+" rnd64 = "+rhs2+"\n")

fout.write("}\n")

fout.close()
