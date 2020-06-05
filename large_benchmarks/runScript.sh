DIRS="FFT_1024\
	lorentz20\
	poisson2d0\
	poisson2d1_t32\
	poisson2d2_t32\
	convecdiff2d0\
	convecdiff2d1_t32\
	convecdiff2d2_t32\
	heat2d0_t32\
	heat2d1_t32\
	heat2d2_t32\
	advect3d\
	fdtd1d_t64\
	lorentz20\
	lorentz40\
	lorentz70\
	matmul64\
	matmul128\
	FFT_1024\
	FFT_4096pt\
	MD\
	chainSum\
	poly-eval\
	horner\
	reduction\
	Scan_1024\
	Scan_4096\
	CG_Arc\
	CG_Pores\
	var_ccsd_type2_0\
	var_ccsd_type2_1\
	ccsd_type2_0\
	ccsd_type2_1"

DIRS="horner\
	 reduction\
	 poly-eval"

set -x

for d in $DIRS
do
	echo $d
	cd $d
	echo "executing batch scipt for " $d
	bash batch_abs.slurm
	python3 ../collect_results.py $d
	echo $PWD
	cd ..
done
exit
