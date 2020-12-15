#!/bin/bash
#SBATCH --time=72:00:00
#SBATCH --partition=soc-kp
#SBATCH --account=soc-kp
#SBATCH -N 1 
#SBATCH -J CG_Pores-abs-serial-sim
#SBATCH -o CG-Pores-abs-serial-sim.log
#SBATCH -e CG-Pores-abs-serial-sim.log
#set CC=/uufs/chpc.utah.edu/sys/installdir/gcc/5.4.0/bin/gcc
#set CXX=/uufs/chpc.utah.edu/sys/installdir/dcc/5.4.0/bin/g++
source /uufs/chpc.utah.edu/common/home/u1014840/local_python3.8



# ino Abs
python3 ../../src/satire.py \
        --std \
		--file CG_Pores_noError_K20_N30_E0.0.txt \
		--logfile CG_Pores_noError_K20_N30_E0.0_abs-serial_noAbs.pylog \
		--outfile CG_Pores_noError_K20_N30_E0.0_abs-serial_noAbs.out

## Abs window : (10,20)
#python3 ../../src/satire.py \
#        --std \
#		--file CG_Pores_noError_K20_N30_E0.0.txt \
#		--logfile CG_Pores_noError_K20_N30_E0.0_abs-serial_10_20.pylog \
#		--outfile CG_Pores_noError_K20_N30_E0.0_abs-serial_10_20.out \
#		--enable-abstraction \
#		--mindepth 10 \
#		--maxdepth 20
#
## Abs window : (15,25)
#python3 ../../src/satire.py \
#        --std \
#		--file CG_Pores_noError_K20_N30_E0.0.txt \
#		--logfile CG_Pores_noError_K20_N30_E0.0_abs-serial_15_25.pylog \
#		--outfile CG_Pores_noError_K20_N30_E0.0_abs-serial_15_25.out \
#		--enable-abstraction \
#		--mindepth 15 \
#		--maxdepth 25
#
## Abs window : (20,40)
#python3 ../../src/satire.py \
#        --std \
#		--file CG_Pores_noError_K20_N30_E0.0.txt \
#		--logfile CG_Pores_noError_K20_N30_E0.0_abs-serial_20_40.pylog \
#		--outfile CG_Pores_noError_K20_N30_E0.0_abs-serial_20_40.out \
#		--enable-abstraction \
#		--mindepth 20 \
#		--maxdepth 40
#
