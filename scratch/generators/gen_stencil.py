# stencil basic spec
# A[i,t] = 0.25 * A[i-1, t] + A[i, t] + A[i+1, t]

import  sys

def get_sign(index, mid):
	return 'p' if index > mid else 'm' if index < mid else ''

def gen_stencil_cse():
	cm1 = str(0.25) # negative offset
	c = str(0.5) # center
	cp1 = str(0.25) # positive offset
	
	T=int(sys.argv[1])
	mid = T
	A = [[None]*(2*T+1) for i in range(2)]

	fout = open("h1_cse_t"+str(T)+".txt", 'w')

	for t in range(1, T+1):
		for i in range(mid-(T-t), mid+(T-t)+1):
			print(t, i)
			lhs = "x{sign}{pos}_{tstamp}".format(sign=get_sign(i, mid), pos=str(abs(mid-i)), tstamp=str(t))
			l_rhs = cm1+ "*" + "x{lsign}{pos}_{tstamp}".format(lsign=get_sign(i-1, mid), \
			    pos=str(abs(mid - (i-1))), tstamp=str(t-1))
			c_rhs = c+ "*" + "x{csign}{pos}_{tstamp}".format(csign=get_sign(i, mid), \
			    pos=str(abs(mid-i)), tstamp=str(t-1))
			r_rhs = cp1+ "*" + "x{rsign}{pos}_{tstamp}".format(rsign=get_sign(i+1, mid), \
			    pos=str(abs(mid-(i+1))), tstamp=str(t-1))
			fout.write(lhs+"  =  ("+l_rhs+ " + " +c_rhs+ " + " +r_rhs+ ");\n")

	fout.close()
	

def gen_stencil_tree():
	cm1 = str(0.25) # negative offset
	c = str(0.5) # center
	cp1 = str(0.25) # positive offset
	
	T=int(sys.argv[1])
	mid = T
	
	#A = [[None]*(2*T+1) for i in range(0, T+1)]
	A = [[None]*(2*T+1) for i in range(2)]
	
	# fill A with required string symbols at the base
	for i in range(mid-T, mid+0):
		A[0][i] = "xm"+str(abs(i-mid))
	for i in range(mid+1, mid+T+1):
		A[0][i] = "xp"+str(abs(i-mid))
	
	A[0][mid] = "x"
	print(A[0])
	
	for t in range(1, T+1):
		for i in range(mid-(T-t), mid+(T-t)+1):
			print(t, i)
			A[t%2][i] = "(" +cm1+ "*" +A[(t-1)%2][i-1]+  " + " \
			              +c+   "*" +A[(t-1)%2][i]+    " + " \
			              +cp1+ "*" +A[(t-1)%2][i+1]+    " )" 
	
	
	print(A[T%2][mid].__sizeof__())
	print(A[T%2][mid])



if __name__ == "__main__":
	#gen_stencil_tree()
	gen_stencil_cse()
	pass
