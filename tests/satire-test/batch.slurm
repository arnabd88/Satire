#!/bin/bash
#SBATCH --time=72:00:00
#SBATCH --partition=soc-kp
#SBATCH --account=soc-kp
#SBATCH -N 1 
#SBATCH -J satern-serial-sim
#SBATCH -o satern-serial-sim.log
#SBATCH -e err-satern-serial-sim.log
#set CC=/uufs/chpc.utah.edu/sys/installdir/gcc/5.4.0/bin/gcc
#set CXX=/uufs/chpc.utah.edu/sys/installdir/dcc/5.4.0/bin/g++

FILES="exp1x.txt\
	   exp1x_32.txt\
	   carbonGas.txt\
	   x_by_xy.txt\
	   verhulst.txt\
	   turbine3.txt\
	   turbine2.txt\
	   turbine1.txt\
	   triangle.txt\
	   test05_nonlin1_test2.txt\
	   test05_nonlin1_r4.txt\
	   test02_sum8.txt\
	   test01_sum3.txt\
	   sum.txt\
	   sqrt_add.txt\
	   sqroot.txt\
	   sphere.txt\
	   sine.txt\
	   sineOrder3.txt\
	   sec4_example.txt\
	   rigidBody2.txt\
	   predatorPrey.txt\
	   nonlin2.txt\
	   nonlin1.txt\
	   logexp.txt\
	   jetEngine.txt\
	   intro_example.txt\
	   i4.txt\
	   hypot32.txt\
	   himmilbeau.txt\
	   exp1x_log.txt\
	   bspline3.txt\
	   delta4.txt\
	   delta.txt\
	   doppler1.txt\
	   doppler2.txt\
	   doppler3.txt\
	   hypot.txt\
	   kepler0.txt\
	   kepler1.txt\
	   kepler2.txt\
	   rigidBody1.txt\
	   test04_dqmom9.txt\
	   test06_sums4_sum1.txt\
	   test06_sums4_sum2.txt"

set -x

cd "all_compatable_fpbench"

for d in $FILES
do
	for trial in {1..20}
	do
	   python3 ../../../src/satern.py --file ${d} --std --sound --logfile ${d}_${trial}.log --outfile ${d}_${trial}.out
	done
done
cd ..
