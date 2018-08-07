#!/usr/bin/python

import pandas as pd
import numpy as np
import sys
import os, time

if len(sys.argv) < 3:
    sys.exit('Usage: database-name' % sys.argv[0])

en  = float(sys.argv[1])
Ndata = int(sys.argv[2])

name = 'boron_fcc_tidu_h'
ekin_str = '_ek' + str(en) + 'k_Nrun' + str(Ndata)
strbody = name + ekin_str
filename = strbody + '.txt'
f = open(filename, "w")

m = 0
a = {}
b = {}
for i in range(1, Ndata + 1):
    a[m] = pd.read_table('boron_fcc_tidu_h_run%d_ek%.1fk_run%d.txt' %(i, en, i), sep=',', header = None)
    b[m] = pd.DataFrame(a[m])
    m+=1

Nrow = 30
Ncol = 9

for j in range(0, Nrow):
    for k in range(0, Ncol):
        Sum = 0.0
        for i in range(0, Ndata) :
            Sum += b[i].iloc[j, k]

        ave = Sum / Ndata
        if k < Ncol - 1: f.write("%lf," %(ave))
        else : f.write("%lf" %(ave))
    f.write("\n")
f.close()
