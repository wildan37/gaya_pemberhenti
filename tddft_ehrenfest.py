#!/usr/bin/python

import numpy as np
import os, time
from ase.units import Hartree, Bohr, _amu, _me, AUT
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

if len(sys.argv) < 3:
    sys.exit('Usage: database-name' % sys.argv[0])

#Timestep and duration of simulation in attosecond
en = float(sys.argv[1])
run = int(sys.argv[2])
#name = 'aluminum_h'
name = 'boron_tetra_h'
Ekin = en*1e3
timestep = 1.0 * np.sqrt (10e3/Ekin)
duration = 6e2
ekin_str = '_ek' + str(float(Ekin/1000)) + 'k_run' + str(run) 
amu_to_aumass = _amu/_me
strbody = name + ekin_str
input_file = name + '.gpw'
traj_file = strbody + '.traj'
filename = strbody + '.txt'
f = open (filename,"w")
Natoms = 13
Nkord = 3
p_bands = 2
dom_dc = (2, 2, 8)
print(en, run)
#number of iterations and integer divisor to update states every 0.02 fs
ndiv = int(np.ceil(0.02e3 / timestep))
niter = ndiv * int (np.ceil(duration / (ndiv * timestep) ) )

parallel = { 'band' : p_bands, 'domain' : None}
tdcalc = TDDFT (input_file, solver = 'CSCG', 
                propagator= 'EFSICN', parallel=parallel)

##Projectile part
proj_idx = Natoms - 1
v = np.zeros ((Natoms, 3))                            #set all velocity to zero
Mproj = tdcalc.atoms.get_masses()[proj_idx]
Ekin *= Mproj
Ekin = Ekin / Hartree

Mproj *= amu_to_aumass
v[proj_idx, 0] = -np.sqrt ( ( 2 * Ekin) / Mproj ) * Bohr / AUT
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
                %(T, xproj[m], ep, epot, rate, ekin, etot, epow[m], sp)) #all in  eV

        spc = SinglePointCalculator (spa, energy=epot, forces=F_av)
        spa.set_calculator(spc)
        traj.write(spa)
        m+=1
    evv.propagate(timestep)

traj.close()
f.close()
