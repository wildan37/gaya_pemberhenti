#!/bin/bash

#PBS -l nodes=1:ppn=32,walltime=01:00:00
#PBS -q laser                                         #name of the queue (default, laser, etc.)
#PBS -V
#PBS -m ae -M w.abdussalam@hzdr.de           #your email address
#PBS -N ground_B8_H                            #name of job 
#PBS -e ground_B8_H.$PBS_JOBID.err         #name of error file
#PBS -o ground_B8_H.$PBS_JOBID.out         #name of out file

. /etc/profile.modules
module purge
module load gcc/4.8.2 
module load libxc
module load python/3.6.2
export GPAW_SETUP_PATH=/bigdata/hplsim/production/gpaw-ase/gpaw-setups-0.9.20000/
module load openmpi/1.8.0 
module load lapack/3.5.0 
module load blas/1.0 
#module load fftw/3.3.7
#module load gsl/2.3 

HOMEDIR=/bigdata/hplsim/production/nu_urang/aluminum_output/runfiles
TARGETDIR=/bigdata/hplsim/production/nu_urang/aluminum_output/outfiles
PARAMETERS=(0 0)

cd ${HOMEDIR}
EXEC=dft_real_inputfile_beta.py
PAR=mpirun
PY=gpaw-python
NOPAR=(32)

echo ${HOMEDIR}
hostname

${PAR} -np ${NOPAR[*]} ${PY} ${EXEC} ${PARAMETERS[*]}
#mv *txt *gpw ${TARGETDIR}
