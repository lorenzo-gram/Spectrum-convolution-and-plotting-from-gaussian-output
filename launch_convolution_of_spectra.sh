#!/bin/bash

python3 convolution_of_spectra.py --emin 1.5 --emax 4.5 --ewid 0.15 --grdid 300 --directories './md*/OUTPUT/QM_data/qmALL.log' --title './md*' --mod 'rep' 
