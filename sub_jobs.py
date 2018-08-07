#! /usr/bin/env python

import os
import sys
import re
import numpy as np

ks = np.arange(2, 3, 2) 
cuts = np.arange(2, 51, 1)

def buildSubmit(filename, k, cut):
    inlines  = file('run_aluminum.sh').readlines()
    outlines = []
    for line in inlines:
        if 'PARAMETERS' in line:
            line = line.replace('PARAMETERS=(0 0)', 'PARAMETERS=(%i %i)' %(k, cut))
        outlines.append(line)
    file(filename, 'w').writelines(outlines)   

for k in ks:
    for cut in cuts:
	print 'sub_job_par_dir%d_run%d' % (k, cut)
	filename_submit = 'submit_dir%d_run%d.sh' % (k, cut)
	buildSubmit(filename_submit, k, cut)
	os.system('qsub ' + filename_submit)


