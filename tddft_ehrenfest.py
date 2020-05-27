#!/usr/bin/python

import numpy as np
import os, time
from ase.units import Hartree, Bohr, _amu, _me, AUT, kB
from ase import Atoms
from ase.parallel import paropen
from gpaw.mpi import world
from ase.io.trajectory import PickleTrajectory, Trajectory
from ase.calculators.singlepoint import SinglePointCalculator
from gpaw.tddft import TDDFT
from gpaw.tddft.ehrenfest import EhrenfestVelocityVerlet
import matplotlib.pyplot as plt
from ase.visualize.plot import plot_atoms
import sys
import random as rd

if len(sys.argv) < 4:
    sys.exit('Usage: database-name' % sys.argv[0])

#Timestep and duration of simulation in attosecond
en = float(sys.argv[1])
run = int(sys.argv[2])
T = int(sys.argv[3])
#name = 'aluminum_h'
name = 'boron_beta_h_lsnap_T%dK'%(T)
Ekin = en*1e3
timestep = 1.0 * np.sqrt (10e3/Ekin)

if en > 51 : 
    duration = 2e2
    ndiv = int(np.ceil(0.01e3 / timestep))
else : 
    duration = 4e2
    ndiv = int(np.ceil(0.02e3 / timestep))

ekin_str = '_ek' + str(float(Ekin/1000)) + 'k_run' + str(run) 
amu_to_aumass = _amu/_me
strbody = name + ekin_str
input_file = name + '_run' + str(run) + '.gpw'
traj_file = strbody + '.traj'
filename = strbody + '.txt'
f = open (filename,"w")
Natoms = 106
Nkord = 3
p_bands = 2
print(en, run)
#number of iterations and integer divisor to update states every 0.02 fs
#ndiv = int(np.ceil(0.01e3 / timestep))
niter = ndiv * int (np.ceil(duration / (ndiv * timestep) ) )
#parallel = { 'band' : p_bands, 'domain' : None, 'sl_auto' : True}
#parallel = { 'band' : p_bands, 'domain' : None, 'sl_default' : (4, 4, 64)}
parallel = { 'band' : p_bands, 'domain' : None}
tdcalc = TDDFT (input_file, solver = 'CSCG', 
                propagator= 'EFSICN', parallel=parallel)

##Projectile part
proj_idx = Natoms - 1
v = np.zeros ((Natoms, 3))                            #set all velocity to zero
Mproj = tdcalc.atoms.get_masses()[proj_idx]

#Mat = []
#vat = np.zeros([12, 3])
#for i in range(0,12):
#    Mat.append(tdcalc.atoms.get_masses()[i]*amu_to_aumass)

#ekin projectile
Ekin *= Mproj
Ekin = Ekin / Hartree
Mproj *= amu_to_aumass
v[proj_idx, 0] = -np.sqrt ( ( 2 * Ekin) / Mproj ) * Bohr / AUT

#ekin_atoms
#Ekint = 1.5 * len(Mat) * kB * T
##np.random.seed(run)
#for i in range(0,12):
#    for j in range(0,3):
#        vat[i,j] = rd.uniform (0,1) / (3* Mat[i])**0.5
#        v[i,j] = vat[i,j]
#
#world.broadcast(vat, 0)
#ekint = 0.5 * np.dot(Mat, np.sum(vat**2, axis=1)) 
#vat *= (Ekint/ekint)**0.5
#for i in range(0,12):
#    for j in range(0,3):
#        v[i,j] = vat[i,j]

tdcalc.atoms.set_velocities(v)

evv = EhrenfestVelocityVerlet(tdcalc)
traj = Trajectory (traj_file, 'w', tdcalc.get_atoms())
t0 = time.time()
m = 0
epow = np.zeros(niter)
xproj = np.zeros(niter)
sp = 0
for i in range(niter):

    Ekin_p = 0.5 *evv.M[proj_idx] * (evv.v[proj_idx, 0]**2 \
                                    + evv.v[proj_idx, 1]**2 \
                                    + evv.v[proj_idx, 2]**2 )

    if i % ndiv == 0:
        spa = tdcalc.get_atoms()
        F_av = evv.F * Hartree / Bohr
        epot = tdcalc.get_td_energy() * Hartree
        ekin = tdcalc.atoms.get_kinetic_energy()
        rate = 60 * ndiv / (time.time() - t0)
        T = i * timestep
        ep = Ekin_p * Hartree
        etot = ekin + epot
        epow [m]  = etot - ep
        xproj[m] = spa[proj_idx].x
        if m > 0:
            sp = abs((epow[m] - epow[m-1])/(xproj[m] - xproj[m-1]))
        else:
            sp = 0

        f.write("%.6e,%.3lf,%.6e,%.6e,%.6e,%.6e,%.6e,%.6e,%.6e\n" 
                %(T, xproj[m], ep, epot, v[proj_idx, 0], ekin, etot, epow[m], sp)) #all in  eV

        spc = SinglePointCalculator (spa, energy=epot, forces=F_av)
        spa.set_calculator(spc)
        traj.write(spa)
        m+=1
    evv.propagate(timestep)

traj.close()
f.close()
