#!/bin/bash
#SBATCH --time=72:00:00
#SBATCH --partition=soc-kp
#SBATCH --account=soc-kp
#SBATCH -N 1 
#SBATCH -J emp-dqmom
#SBATCH -o emp-dqmom.log
#SBATCH -e err-emp-dqmom.log
#set CC=/uufs/chpc.utah.edu/sys/installdir/gcc/5.4.0/bin/gcc
#set CXX=/uufs/chpc.utah.edu/sys/installdir/dcc/5.4.0/bin/g++


set -x

bash run.sh

./dqmom 1000000 > dqmom-emp.log
