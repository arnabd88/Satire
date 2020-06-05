

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

GPHOME1="/home/arnab/work/gelpia/"

# use only if $GPHOME is not defined globally else use the global env value
if [[ -z "${GPHOME}$" ]]; then
	GPHOME=$GPHOME1
fi

GPEXE1=$GPHOME/bin/gelpia

GPEXE2=$(eval "which gelpia")

#EXE1 = $(eval "sed -i s/\/\//\//g $GPEXE1")
#EXE2 = $(eval "sed -i s/\/\//\//g $GPEXE2")

EXE1=$(eval "echo ${GPEXE1//\/\//\/}")
EXE2=$(eval "echo ${GPEXE2//\/\//\/}")

if [[ $EXE1 == $EXE2 ]];
then

#find $GPHOME -name "*generated*"

	if [[ -f Results.txt ]]
	then
		echo "Removing old results file"
		rm -rf Results.txt
	fi
	
	for d in $DIRS
	do
		echo $d
		cd $d
		echo "executing batch scipt for " $d
		bash batch_abs.slurm
		python3 ../collect_results.py $d
		echo $PWD
		cat Results.txt >> ../Results.txt
		echo "Cleaning up gelpia generated files"
		find $GPHOME -name "*generated*"
		cd ..
	done
	
	echo "Open Results.txt for summary of the evaluation"
else
	echo "COrrectly set 'GPHOME' to gelpia home diretcory"
fi
exit
