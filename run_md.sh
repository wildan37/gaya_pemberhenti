#!/bin/bash

#PBS -l nodes=4:ppn=64,walltime=36:00:00
#PBS -q laser                   #name of the queue (default, laser, etc.)
#PBS -V
#PBS -m ae -M wildan.abdussalam@mailbox.tu-dresden.de      #your email address
#PBS -N tddft_B_h                       #name of job 
#PBS -e tddft_B_h.$PBS_JOBID.err         #name of error file
#PBS -o tddft_B_h.$PBS_JOBID.out         #name of out file

. /etc/profile.modules
module purge
module load infiniband/1.0.0
module load gcc/4.8.2 
module load libxc/2.0.2
#module load libxc/4.0.4
#module load python/3.6.2
module load python/3.4.3
#export GPAW_SETUP_PATH=/opt/pkg/devel/python/3.4.3/lib/python3.4/site-packages/paw-dataset/gpaw-setups-0.9.20000/
export GPAW_SETUP_PATH=/bigdata/hplsim/production/gpaw-ase/gpaw-setups-0.9.20000
module load openmpi/1.8.0 
module load scalapack/2.0.2
module load fftw/3.3.7

HOMEDIR=/bigdata/hplsim/production/nu_urang/aluminum_output/runfiles
TARGETDIR=/bigdata/hplsim/production/nu_urang/aluminum_output/outfiles
PARAMETERS=(0 0 0)

cd ${HOMEDIR}
#EXEC=./md_al_fcc.py
#EXEC=./md_al_fcc_par.py
#EXEC=./tddft.py
#EXEC=./tddftlcao.py
#EXEC=./dislocation.py
EXEC=tddft_ehrenfest.py
PAR=mpirun
PY=gpaw-python
NOPAR=(256)

echo ${HOMEDIR}
hostname

#${EXEC} ${PARAMETERS[*]}
#${EXEC} 
${PAR} -np ${NOPAR[*]} ${PY} ${EXEC} ${PARAMETERS[*]}
#mv *txt *traj  ${TARGETDIR}
