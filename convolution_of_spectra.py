import argparse    # command line arguments parser
import sys         # System-specific parameters and functions
import os          # filesystem utilities
import shutil      # filesystem utilities
import numpy as np
import math
import glob        # to find directories matching a pattern
import matplotlib.pyplot as plt
##############################################################################################
parser = argparse.ArgumentParser(
    description="Utility to convolute spectra from gaussian tddft output(s) yielding both the convoluted spectrum and vertical bars corresponding to each excitation energy",
    epilog="The script convolutes the UV spectrum with a Gaussian function, from the results obtained from an ensemble of vertical excitations, each of them convoluted with a Gaussian function",
    )


parser.add_argument("-dir", "--directories", required=True, metavar='DIR', dest="directories_list",
                     type=str, help="path of the directories containing the .log file")
parser.add_argument("-tit", "--title", required=True, metavar='TIT', dest="title_list",
                     type=str, help="path of the directories whose name has to be used to differentiate different tddft calculations (e.g. md001, md002,...")
parser.add_argument("-emin", "--emin", default=0.1, metavar='EMIN', dest="emin",
                    type=float, help="minimum energy in the spectrum")
parser.add_argument("-emax", "--emax", default=10.0, metavar='EMAX', dest="emax",
                    type=float, help="maximum energy in the spectrum")
parser.add_argument("-ew", "--ewid", default=0.15,  metavar='EWID', dest="ew",
                    type=float, help="broadening in energy domain (eV)")
parser.add_argument("-g", "--grdid", default=300,  metavar='GRID', dest="grid",
                    type=int, help="number of grid points of the spectrum")
parser.add_argument("-m", "--mod", default='height',  metavar='HEIGHT', dest="mode",
                    type=str, help="how to scale the vertical bars: rep means to multiply the oscillator strength times the number of spectra in the convolution, height means that the highest bar needs to have half of the maximum height of the convoluted spectrum")



args = parser.parse_args()

log_files = glob.glob(args.directories_list)
titles = glob.glob(args.title_list)

#######################################################################################################

#Individuate the block of gaussian output that bears the information about the excited states. 
#The first line of the block starts with "Excited State" and the first line following the block starts with "SavETr"

excited_state=[]
wavelength=[]
f=[]
nature=[]

for log_file in log_files:
    gaussian_output=open(log_file,'r')
    extracted=[]
    v=0
    for line in gaussian_output:
        splitted=line.split()   
        if len(splitted)>2 and splitted[0]=='Excited' and splitted[1]=='State':
            v=1
        if len(splitted)>1 and splitted[0]=='SavETr:':
            v=0
        if v==1:
            extracted.append(splitted)
            
########################################################################################################
#excited_state_i is a list with an index of the excited state found in the ith log file, e.g.[1,2,3] if 3 excited states are present
#wavelength_i is a list with the wavelengths of the excitations found in the ith log file
#f_i is a list of the oscillator strengths of the excitations found in the ith log file
#nature_i is a list of the most important A->B orbital transition, one for each excited state found in the ith log file

    excited_state_i=[]
    wavelength_i=[]
    f_i=[]
    nature_i=[]


    t=0
    for i in range(len(extracted)):
        if len(extracted[i])>2 and extracted[i][0]=='Excited' and extracted[i][1]=='State':
            t=t+1
            excited_state_i.append(t)
            wavelength_i.append(float(extracted[i][6]))
            f_i.append(float(extracted[i][8][2:]))

    
    s=0
    for i in range(len(extracted)):
        if len(extracted[i])>2 and extracted[i][0]=='Excited' and extracted[i][1]=='State':
            s=1
            nature_state_i_weight=0
        if s==1 and len(extracted[i])>2 and len(extracted[i][1])>3 and extracted[i][1][:2]=='->': #if the basis set is DZ, the format of g16 output is "orb1 ->orb2"
            if abs(float(extracted[i][2]))>nature_state_i_weight:
                nature_state_i_weight=abs(float(extracted[i][2]))
                nature_state_i=f'{extracted[i][0]}{extracted[i][1]}'
            try:
                float(extracted[i+1][0])
            except IndexError:
                s=0
                nature_i.append(nature_state_i)
            except ValueError:
                s=0
                nature_i.append(nature_state_i) #extract only the highest contribution to the nature
        elif s==1 and len(extracted[i])>2 and len(extracted[i][1])<3 and extracted[i][1][:2]=='->': #if the basis set is TZ, the format of g16 output is "orb1 -> orb2"
            if abs(float(extracted[i][3]))>nature_state_i_weight:
                nature_state_i_weight=abs(float(extracted[i][3]))
                nature_state_i=f'{extracted[i][0]}{extracted[i][1]}{extracted[i][2]}'
            try:
                float(extracted[i+1][0])
            except IndexError:
                s=0
                nature_i.append(nature_state_i)
            except ValueError:
                s=0
                nature_i.append(nature_state_i)        
##########################################################################################################

    excited_state.append(excited_state_i)
    wavelength.append(wavelength_i)
    f.append(f_i)
    nature.append(nature_i)
    
    gaussian_output.close()
    
#excited_state is a list with a sublist for each log file (the sublists are all the excited_state_i, one for each log file)
#wavelength is a list with a sublist for each log file (the sublists are all the wavelength_i, one for each log file)
#f is a list with a sublist for each log file (the sublists are all the f_i, one for each log file)
#nature is a list with a sublist for each log file (the sublists are all the nature_i, one for each log file)

#######################################################################################################

bars=open('bars.dat','w')

for i in range(len(titles)):
    bars.write(f'{titles[i]:>30}')
    for j in range(len(excited_state[i])):
        bars.write('\t\t')
        bars.write(f'{excited_state[i][j]:>3}{wavelength[i][j]:>8.2f}{f[i][j]:>8}{nature[i][j]:>10}')
        
    bars.write('\n')

bars.close()                

#In the output file bars.dat each line correspond to a .log file. Each line has the title, the index of the excited state, its wavelength, its oscillator strength and its nature.


####################################################################################################
########################################PLOTTING##################################################
# Parameters
energy_min = args.emin   # Starting energy (eV) ####################
energy_max = args.emax   # Ending energy (eV)   #######################
n_points = args.grid        # Number of points in the spectral grid ######################
gaussian_width =args.ew   # Gaussian width (standard deviation in eV) #####################


# Prepare spectral grid
spectral_grid = np.linspace(energy_min, energy_max, n_points)
spectral_grid_nm = [1239.8/ev for ev in spectral_grid]
spectrum = np.zeros_like(spectral_grid)

#gaussian
flat_wavelengths = [w for sublist in wavelength for w in sublist]
flat_wavelengths_eV = [1239.8/wl for wl in flat_wavelengths]
flat_f = [i for sublist in f for i in sublist]

for center, intensity in zip(flat_wavelengths_eV, flat_f):
    line_profile = (
        1.0 / (gaussian_width * math.sqrt(2.0 * math.pi)) *
        np.exp(-((spectral_grid - center) ** 2) / (2.0 * gaussian_width ** 2))
    )
    spectrum += intensity * line_profile 
plt.figure(figsize=(8, 5))
# Plot convoluted spectrum
plt.plot(spectral_grid_nm, spectrum, color='black', linewidth=2, label='Convoluted Spectrum')


# Number of sublists
n_sets = len(wavelength)

# Number of lines per sublist
n_lines = len(wavelength[0])

# Set up colors for each line position
colors = plt.cm.viridis_r([i / n_lines for i in range(n_lines)])

# Plotting
for i in range(n_lines):
    for j in range(n_sets):
        x = wavelength[j][i]
        if args.mode=='rep':
            y = f[j][i] * n_sets 
        if args.mode=='height':
            y= f[j][i] * max(spectrum)/max(flat_f)/2
        plt.vlines(x, 0, y, color=colors[i], label=f'S0 -> S{i+1}' if j == 0 else "")



plt.xlabel('wavelength (nm)')
plt.ylabel('f')
plt.legend()
plt.tight_layout()
plt.show()
plt.savefig("convoluted_spectrum.png", dpi=300, bbox_inches='tight')

#It plots the convoluted spectrum along with the vertical bars. Each excited state has its own color.
####################################################################################################
spectrum_file=open('spectrum_gaussian.dat','w')
spectrum_file.write('       energy(eV)    wavelength(nm)    intensity\n\n')
for i in range(len(spectral_grid)):
    spectrum_file.write(f'{spectral_grid[i]:>16.4f}{spectral_grid_nm[i]:16.4f}{spectrum[i]:16.4f}\n')
spectrum_file.close()
#In the output file spectrum_gaussian.dat it writes the points of the convoluted spectrum
