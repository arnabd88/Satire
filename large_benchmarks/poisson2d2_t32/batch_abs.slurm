#!/bin/bash
#SBATCH --time=72:00:00
#SBATCH --partition=soc-kp
#SBATCH --account=soc-kp
#SBATCH -N 1 
#SBATCH -J poisson2d2_t32_abs-serial-sim
#SBATCH -o poisson2d2_t32-abs-serial-sim.log
#SBATCH -e poisson2d2_t32-abs-serial-sim.log
#set CC=/uufs/chpc.utah.edu/sys/installdir/gcc/5.4.0/bin/gcc
#set CXX=/uufs/chpc.utah.edu/sys/installdir/dcc/5.4.0/bin/g++
source /uufs/chpc.utah.edu/common/home/u1014840/local_python3.8


# Abs window : (10,20)
python3 ../../src/satern.py \
        --std \
		--compress \
		--file poisson2d2_t32.txt \
		--logfile poisson2d2_t32_abs-serial_10_20.pylog \
		--outfile poisson2d2_t32_abs-serial_10_20.out \
		--enable-abstraction \
		--mindepth 10 \
		--maxdepth 20

# Abs window : (15,25)
python3 ../../src/satern.py \
        --std \
		--compress \
		--file poisson2d2_t32.txt \
		--logfile poisson2d2_t32_abs-serial_15_25.pylog \
		--outfile poisson2d2_t32_abs-serial_15_25.out \
		--enable-abstraction \
		--mindepth 15 \
		--maxdepth 25

# Abs window : (20,40)
python3 ../../src/satern.py \
        --std \
		--compress \
		--file poisson2d2_t32.txt \
		--logfile poisson2d2_t32_abs-serial_20_40.pylog \
		--outfile poisson2d2_t32_abs-serial_20_40.out \
		--enable-abstraction \
		--mindepth 20 \
		--maxdepth 40
