#!/bin/bash

#PBS -l nodes=1:ppn=1,walltime=120:00:00
#PBS -q default                     #name of the queue (default, laser, etc.)
#PBS -V
#PBS -m ae -M w.abdussalam@hzdr.de      #your email address
#PBS -N tddft_B_h                       #name of job 
#PBS -e tddft_B_h.$PBS_JOBID.err         #name of error file
#PBS -o tddft_B_h.$PBS_JOBID.out         #name of out file

. /etc/profile.modules

HOMEDIR=/bigdata/hplsim/production/nu_urang/aluminum_output/runfiles

cd ${HOMEDIR}
EXEC=sub_job_td.py
PY=python

echo ${HOMEDIR}
hostname
${PY} ${EXEC} 
