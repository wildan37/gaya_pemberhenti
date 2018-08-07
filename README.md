This code is aimed at calculating a stopping power of ions on the target employing a TDDFT-Ehrenfest method. Here we provide an example of a proton which penetrates an ensamble of fcc and tetrahedral Borons. This calculations are performed using ase-python gpaw environment which can be installed in the following link: https://wiki.fysik.dtu.dk/ase/install.html. As we are dealing with a many-body system, parallel computation are necessary. The required modules are the following:

1. gcc
2. libxc/2.0.2
3. python - gpaw
4. openmpi

To calculate the stopping power, one needs to calculate ground state of the target as well as ions using Density functional theory method (dft_real_inputfile.py). We used a .xyz input files (bor_fcc and bor_real are for fcc and tetrahedral lattice sturctures, respectively. In addition to input, the ion is added separately from the input file. The ground-state result (.gpw) will be used as an initial condition for calculating energies (see tddft_ehrenfest.py), e.g., kinetic energy of target, potential energy of target, total energy of target and kinetic energy of an ion. 

As the stopping power is defined as S(x) = dE/dX, where E = total energy of target - kinetic energy of an ion and dX denotes the different vector positions of an ion, one needs to obtain the kinetic as well as kinetic enenergies of target for total energy of target. For the stopping power dependant on either velocity or kinetic energy of ions, one needs to plot E as the function of them and take a slope by means of linear regression. To check the validity of simulation please open the following link https://www-nds.iaea.org/stopping/stopping_timg.html where you can find experimental data of stopping power. 

Please beware that the calcuation has to be repeated with different initial position of ion to obtain desirable statistics. This will require many nodes with separated-submitted jobs. The number of nodes differ as DFT possesses do not require many nodes as TDDFT-Ehrenfest as it saturates for certain number of nodes. For the sake efficiency, therefore, we separated DFT and TDDFT files. Specifically, we mentioned the number of nodes for DFT on run_aluminum.sh and TDDFT-Ehrenfest on run_md.sh. sub_jobs.py and sub_job_td.py are the files for efficiently submitting jobs of DFT and TDDFT, respectively. 

Have fun and feel free to ask me should you have questions.
