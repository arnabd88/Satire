
import sys

def get_sign(index, mid):
	return 'p' if index > mid else 'm' if index < mid else ''


def gen_wave2d_cse():
	
	west = "0.25"
	east = "0.25"
	north = "0.25"
	south = "0.25"
	curr_center = "1.0"
	prev_center = "-1.0"

	w = 2
	T = int(sys.argv[1])
	mid0, mid1 = T*w , T*w

	fout = open("wave2d1_t"+str(T)+".txt", "w")

	## There are 2 arrays to begin with x0 and x1

	for t in range(0, T+1):
		if(t==0):
			fout.write("INPUTS {\n\n")
		# for the first iteration
		for i in range(mid0 - (T-t)*w, mid0+(T-t)*w +1):
			for j in range(mid1 - (T-t)*w, mid1+(T-t)*w +1):

				if t==0:
					inp0 = "x0_{signx}{posx}_{signy}{posy}_{tstamp} fl64 : ({lb}, {ub});\n".format(\
						signx = get_sign(i, mid0), \
						signy = get_sign(j, mid1), \
						posx  = str(abs(mid0-i)), \
						posy  = str(abs(mid1-j)), \
						tstamp = str(t), \
						lb = float(sys.argv[2]), \
						ub = float(sys.argv[3])
					)
					inp1 = "x1_{signx}{posx}_{signy}{posy}_{tstamp} fl64 : ({lb}, {ub});\n".format(\
						signx = get_sign(i, mid0), \
						signy = get_sign(j, mid1), \
						posx  = str(abs(mid0-i)), \
						posy  = str(abs(mid1-j)), \
						tstamp = str(t), \
						lb = float(sys.argv[2]), \
						ub = float(sys.argv[3])
					)
					fout.write(inp0)
					fout.write(inp1)
				else:
					f_lhs = "x0_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
								signx = get_sign(i, mid0), \
								signy = get_sign(j, mid1), \
								posx  = str(abs(mid0-i)),  \
								posy  = str(abs(mid1-j)),  \
								tstamp = str(t) \
					)

					f_west_lhs = "{coeff} * x1_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
								coeff = west, \
								signx = get_sign(i-1, mid0), \
								signy = get_sign(j, mid1), \
								posx  = str(abs(mid0-(i-1))), \
								posy  = str(abs(mid1-j)), \
								tstamp = str(t-1) \
					)

					f_east_lhs = "{coeff} * x1_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
								coeff = east, \
								signx = get_sign(i+1, mid0), \
								signy = get_sign(j, mid1), \
								posx  = str(abs(mid0 - (i+1))), \
								posy  = str(abs(mid1 - j)), \
								tstamp = str(t-1) \
					)

					f_north_lhs = "{coeff} * x1_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
								coeff = north, \
								signx = get_sign(i, mid0), \
								signy = get_sign(j+1, mid1), \
								posx  = str(abs(mid0-i)), \
								posy  = str(abs(mid1-(j+1))), \
								tstamp = str(t-1) \
					)

					f_south_lhs = "{coeff} * x1_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
								coeff = south, \
								signx = get_sign(i, mid0), \
								signy = get_sign(j-1, mid1), \
								posx  = str(abs(mid0-i)), \
								posy  = str(abs(mid1-(j-1))), \
								tstamp = str(t-1) \
					)

					f_center_lhs = "{coeff} * x1_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
								coeff = curr_center, \
								signx = get_sign(i, mid0), \
								signy = get_sign(j, mid1), 
								posx  = str(abs(mid0 - i)), \
								posy  = str(abs(mid1 - j)), \
								tstamp = str(t-1)
					)

					f_center_prev_lhs = "{coeff} * x0_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
								coeff = prev_center, \
								signx = get_sign(i, mid0), \
								signy = get_sign(j, mid1), \
								posx  = str(abs(mid0-i)), \
								posy  = str(abs(mid1-j)), \
								tstamp = str(abs(t-1))
					)

					expr = "{lhs} rnd64 = ({west_lhs} + {east_lhs} + {north_lhs} + {south_lhs} + {center_lhs} + {center_prev_lhs});".format(\
							lhs = f_lhs, \
							west_lhs = f_west_lhs, \
							east_lhs = f_east_lhs, 
							north_lhs = f_north_lhs, \
							south_lhs = f_south_lhs, \
							center_lhs = f_center_lhs, \
							center_prev_lhs = f_center_prev_lhs \
					)
					fout.write(expr+"\n")


		if(t==0):
			fout.write("\n}\n\n")
			fout.write("OUTPUTS {\n\n")
			fout.write("x0_"+str(abs(T*w-mid0))+"_"+str(abs(T*w-mid1))+"_"+str(T)+" ;")
			fout.write("\n}\n\n")
			fout.write("EXPRS {\n\n")
		for i in range(mid0 - (T-t)*w+1, mid0+(T-t)*w-1 +1):
			for j in range(mid1 - (T-t)*w+1, mid1+(T-t)*w-1 +1):
				if t==0:
					pass
				else:
					s_lhs = "x1_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
							signx = get_sign(i, mid0), \
							signy = get_sign(j, mid1), \
							posx  = str(abs(mid0-i)), \
							posy  = str(abs(mid1-j)), \
							tstamp = str(t) \
					)

					s_west_lhs = "{coeff} * x0_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
							coeff = west, \
							signx = get_sign(i-1, mid0), \
							signy = get_sign(j, mid1), \
							posx  = str(abs(mid0-(i-1))), \
							posy  = str(abs(mid1-j)), \
							tstamp = str(t) \
					)

					s_east_lhs = "{coeff} * x0_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
								coeff = east, \
								signx = get_sign(i+1, mid0), \
								signy = get_sign(j, mid1), \
								posx  = str(abs(mid0 - (i+1))), \
								posy  = str(abs(mid1 - j)), \
								tstamp = str(t) \
					)

					s_north_lhs = "{coeff} * x0_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
								coeff = north, \
								signx = get_sign(i, mid0), \
								signy = get_sign(j+1, mid1), \
								posx  = str(abs(mid0-i)), \
								posy  = str(abs(mid1-(j+1))), \
								tstamp = str(t) \
					)

					s_south_lhs = "{coeff} * x0_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
								coeff = south, \
								signx = get_sign(i, mid0), \
								signy = get_sign(j-1, mid1), \
								posx  = str(abs(mid0-i)), \
								posy  = str(abs(mid1-(j-1))), \
								tstamp = str(t) \
					)

					s_center_lhs = "{coeff} * x0_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
								coeff = curr_center, \
								signx = get_sign(i, mid0), \
								signy = get_sign(j, mid1), 
								posx  = str(abs(mid0 - i)), \
								posy  = str(abs(mid1 - j)), \
								tstamp = str(t)
					)

					s_center_prev_lhs = "{coeff} * x1_{signx}{posx}_{signy}{posy}_{tstamp}".format(\
								coeff = prev_center, \
								signx = get_sign(i, mid0), \
								signy = get_sign(j, mid1), \
								posx  = str(abs(mid0-i)), \
								posy  = str(abs(mid1-j)), \
								tstamp = str(abs(t-1))
					)

					expr = "{lhs} rnd64 = ({west_lhs} + {east_lhs} + {north_lhs} + {south_lhs} + {center_lhs} + {center_prev_lhs});".format(\
							lhs = s_lhs, \
							west_lhs = s_west_lhs, \
							east_lhs = s_east_lhs, 
							north_lhs = s_north_lhs, \
							south_lhs = s_south_lhs, \
							center_lhs = s_center_lhs, \
							center_prev_lhs = s_center_prev_lhs \
					)
					fout.write(expr+"\n")
		
	fout.write("\n}\n\n")
	fout.close()




					



if __name__ == "__main__":

	gen_wave2d_cse()
