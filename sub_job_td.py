#! /usr/bin/env python

import os
import sys
import re
import subprocess
import time
import numpy as np

ks = np.arange(170.0, 171.0, 20) 
runs = np.arange(8, 9, 1) 
Ts = np.arange(3500, 3501, 1000)
Njobs_lim = 6
Njobs_sub = 2

def buildSubmit(filename, k, run, T):
    inlines  = file('run_md.sh').readlines()
    outlines = []
    for line in inlines:
        if 'PARAMETERS' in line:
            line = line.replace('PARAMETERS=(0 0 0)', 'PARAMETERS=(%.1f %d %d)' %(k, run, T))
        outlines.append(line)
    file(filename, 'w').writelines(outlines)   

i = 0
for k in ks:
    for run in runs:
        for T in Ts:
            print 'sub_job_par_E%.1f_run%d_T%dK' % (k, run, T)
            filename_submit = 'submit_E%.1f_run%d_T%dK.sh' % (k, run, T)
            buildSubmit(filename_submit, k, run, T)
            os.system('/opt/torque/bin/qsub ' + filename_submit)
#            i+=1
#            wait = True
#            if i % Njobs_sub == 0:
#                while(wait):
#                    return_string = subprocess.Popen("/opt/torque/bin/qstat | grep 'Q' | grep 'abduss38' | wc -l",
#                                                    shell=True, stdout=subprocess.PIPE).communicate()
#                    waiting_jobs = int(np.fromstring(return_string[0], sep='\n')[0])
#                    return_string = subprocess.Popen("/opt/torque/bin/qstat | grep 'R' | grep 'abduss38' | wc -l",
#                                                    shell=True, stdout=subprocess.PIPE).communicate()
#                    running_jobs = int(np.fromstring(return_string[0], sep='\n')[0])
#
#                    # consider also qtop
#                    #subprocess.Popen("qtop | grep 'jobs running of'", shell=True, stdout=subprocess.PIPE).communicate()
#                    jobs_in_queue_total = running_jobs + waiting_jobs
#                    if jobs_in_queue_total < Njobs_lim:
#                        wait = False
#                    else:
#                        print '\n', "Waiting 64 s before continuing job submission ... since total jobs = %d" %(jobs_in_queue_total), '\n'
#                        time.sleep(64)

