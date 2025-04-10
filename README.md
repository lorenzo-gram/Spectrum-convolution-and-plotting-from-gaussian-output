# Spectrum-convolution-and-plotting-from-gaussian-output

This python code is useful to plot the result of a tddft calculation performed by Gaussian.
It works with either one output file or more output files. In both cases, the script will plot a gaussian function around each excitation (whose intensity is proportional to the oscillator strength) energy and sum up all the gaussian functions.
If more than one output files are provided, it will perform a convolution of the spectra (simply summing up the spectra from each output file).

## How to launch the code?

The code can be launched directly on the command line or, for the laziest like me, it is possible to write a simple .sh script so that every time you need to use the script you can simply modify the .sh :) An example is given here "launch_convolution_of_spectra.sh".

The code is launched with:

python3 convolution_of_spectra.py --emin 1.5 --emax 4.5 --ewid 0.15 --grdid 300 --directories './md*/OUTPUT/QM_data/qmALL.log' --title './md*' --mod 'rep' 

where:
* --emin specifies the minimum energy to be plotted (in eV)
* --emax specifies the maximum energy to be plotted (in eV)
* --ewid 0.15 specifies the standard deviation of each gaussian function (in eV)
* --grdid specifies the number of points in the plot of the spectrum
* --directories specifies (in python string format) the path to the .log file(s)
* --title specifies the path where you find the directories that will give the name to each different gaussian calculation (in this case md001, md002, md003,...)
* --mod specifies how to plot the vertical bars (because just using the oscillator strength will result in ugly too short vertical bars when more than one gaussian calculation are performed):
  * 'rep' will multiply the oscillator strength of each bar times the number of gaussian calculations performed
  * 'height' will force the highest oscillator strength to be half of the maximum height of the convoluted spectrum and rescales the others accordingly.
