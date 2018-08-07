#!/bin/bash

#PBS -l nodes=2:ppn=64,walltime=8:00:00
#PBS -q laser                                         #name of the queue (default, laser, etc.)
#PBS -V
#PBS -m ae -M w.abdussalam@hzdr.de           #your email address
#PBS -N tddft_B_h                            #name of job 
#PBS -e tddft_B_h.$PBS_JOBID.err         #name of error file
#PBS -o tddft_B_h.$PBS_JOBID.out         #name of out file

. /etc/profile.modules
#module purge
module load gcc/4.8.2 
module load libxc/2.0.2
module load python/2.7.10
export GPAW_SETUP_PATH=/bigdata/hplsim/production/gpaw-ase/gpaw-setups-0.9.20000/
module load openmpi/1.8.0 
#module load lapack/3.5.0 
#module load blas/1.0 
#module load fftw/3.3.7
#module load gsl/2.3 

HOMEDIR=/bigdata/hplsim/production/nu_urang/aluminum_output/runfiles
TARGETDIR=/bigdata/hplsim/production/nu_urang/aluminum_output/outfiles
PARAMETERS=(0 0)

cd ${HOMEDIR}
#EXEC=./md_al_fcc.py
#EXEC=./md_al_fcc_par.py
#EXEC=./tddft.py
#EXEC=./tddftlcao.py
#EXEC=./dislocation.py
EXEC=tddft_ehrenfest.py
PAR=mpirun
PY=gpaw-python
NOPAR=(128)

echo ${HOMEDIR}
hostname

#${EXEC} ${PARAMETERS[*]}
#${EXEC} 
${PAR} -np ${NOPAR[*]} ${PY} ${EXEC} ${PARAMETERS[*]}
#mv *txt *traj  ${TARGETDIR}
