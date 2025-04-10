# Spectrum-convolution-and-plotting-from-gaussian-output

This python code is useful to plot the result of a tddft calculation performed by Gaussian.\\
It works with either one output file or more output files. In both cases, the script will plot a gaussian function around each excitation (whose intensity is proportional to the oscillator strength) energy and sum up all the gaussian functions.\\
If more than one output files are provided, it will perform a convolution of the spectra (simply summing up the spectra from each output file).

## How to launch the code?

The code can be launched directly on the command line or, for the laziest like me, it is possible to write a simple .sh script so that every time you need to use the script you can simply modify the .sh :) An example is given here "launch_convolution_of_spectra.sh".\\

