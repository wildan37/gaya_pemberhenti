#!/usr/bin/python

import numpy as np
from ase.units import Hartree, Bohr
from ase.calculators.emt import EMT
from ase.build import bulk
from gpaw.utilities import h2gpts
from gpaw import GPAW, PW, FermiDirac, MethfesselPaxton
from ase.visualize import view
import random as rd
from ase import Atom
from ase.parallel import paropen
from ase.build import fcc100
from gpaw.external import ConstantPotential
import sys
import ase.io as io

if len(sys.argv) < 3:
    sys.exit('Usage: database-name' % sys.argv[0])

#if not os.path.exist(sys.argv[1]):
#    sys.exit('error:database %s was not found!' %sys.argv[1]

Nparams = 2
k = np.zeros(Nparams)
for i in range(0, Nparams):
    k[i] = int(sys.argv[i+1])

#m = k[0]
#n = k[1]
#a = 6.246666  # fcc lattice parameter
Temp = k[0]
rd.seed(k[1])
r = rd.random() * 0.77
k2 = k[1] + 100
rd.seed(k2)
r1 = rd.random() * 0.77
Natoms = 12
Nproj = 1
Ntot = Natoms + Nproj
print (k, r, r1)
ef = Temp/11604.52500617
name = 'boron_tetra_h_lsnap_T%dK_run%d' %(k[0], k[1])
filename = name + '.txt' 
f = open (filename, "w")
name_input = 'boron_tetra_h_lsnap_T%dK' %(k[0])
bulk = io.read(name_input + '.xyz')
bulk.append ( Atom('H', (0.9, r1, r) ) )
cell = [[2.454000, -1.416818, 4.188530],
        [0.000000,  2.833635, 4.188530],
        [-2.454000,-1.416818, 4.188530]
        ]
print(Temp, ef)
#cell = [[a, 0, 0],
#        [0, a, 0],
#        [0, 0, a]
#        ]

#bulk.center ( vacuum = 5.0, axis = 2)
bulk.pbc = (True, True, True)
bulk.set_cell(cell, scale_atoms=True)

#print(bulk.positions)

conv_fast = {'energy' : 1.0, 'density' : 1.0, 'eigenstates' : 1.0}
conv_par = {'energy' : 0.001, 'density' : 1e-3, 'eigenstates' : 1e-7}
const_pot = ConstantPotential(1.0)

calc = GPAW( gpts = h2gpts(0.1, bulk.get_cell(), idiv=16),
	     xc = 'LDA',
	     occupations = FermiDirac (width=ef),
	     txt = name + '.txt',
	     nbands = 30,
	     charge = 1,
	     convergence=conv_fast,
	     external=const_pot,
             kpts = {'gamma' : True},
	     parallel = {'band' : None,
			 'kpt' : None,
			 'domain' : None,
			 'order' : 'kdb'}
            )

bulk.set_calculator (calc)
energy = bulk.get_potential_energy ()
calc.write(name + '.gpw', 'all')
print ('Energy =', energy*Hartree, 'Ha')
f.write ("%d %d %.6e\n" %(k[0], k[1], energy*Hartree))
f.close()
