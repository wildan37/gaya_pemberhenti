#! /usr/bin/env python

import os
import sys
import re
import numpy as np

ks = np.arange(10.0, 51.0, 20) 
runs = np.arange(21, 31, 1) 

def buildSubmit(filename, k, run):
    inlines  = file('run_md.sh').readlines()
    outlines = []
    for line in inlines:
        if 'PARAMETERS' in line:
            line = line.replace('PARAMETERS=(0 0)', 'PARAMETERS=(%.1f %d)' %(k, run))
        outlines.append(line)
    file(filename, 'w').writelines(outlines)   

for k in ks:
    for run in runs:
        print 'sub_job_par_E%.1f_run%d' % (k, run)
        filename_submit = 'submit_E%.1f_run%d.sh' % (k, run)
        buildSubmit(filename_submit, k, run)
        os.system('qsub ' + filename_submit)
