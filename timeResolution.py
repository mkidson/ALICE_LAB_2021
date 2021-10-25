#!/usr/bin/env python3
"""
Program designed to be able to take a number of events from just the scintillators in order to make time resolution measurements.
It takes both the run number of number of events as arguments when running the program, and should cancel the run if a run of that number already exists, just to avoid writing over data.

NB: needs the scope to be triggering off one of the channels with scintillators (ch1 or ch2)
"""

import dso1kb
import datetime
import os
import argparse
import numpy as np


# ------------------------------------------------------------------------
# generate a parser for the command line arguments. required so a run number can be passed to the file.
parser = argparse.ArgumentParser(description='Send triggers for a synchronized data run.')
parser.add_argument('run', help='the current TRD run')
parser.add_argument('n_events', help='number of events to be taken')
parser.add_argument('--printargs', action='store_true',
                    help='print arguments and exit')

args = parser.parse_args()
# ------------------------------------------------------------------------


if args.printargs:
    print(args)
    exit(0)

# Connects to the oscilloscope over USB
dso=dso1kb.Dso('/dev/ttyACM1')

# Makes a new directory for the data. You will need to change the path to this for when you save data. This checks if the run exists and if it does, exits, else it creates a directory for the data and carries on
if os.system(f'test -d ~/prac2021/data/timeResolutionData/run_{args.run}') == 0:
    print('That run already exists, change run number to avoid writing over data')
    exit(0)
else:
    os.system(f'mkdir ~/prac2021/data/timeResolutionData/run_{args.run}')
# similar thing for TRD data 

trig_count = []
i = 0
k = 0
while i <= (int(args.n_events)):
    k += 1
    trig_count.append(int(os.system('trdbox reg-read 0x102').read()[:2]))
    if trig_count[k] != trig_count[k-1]:
        i += 1
        print(i)
        now = datetime.datetime.now()
        nowString = now.strftime('%Y.%m.%d.%H.%M.%S')

        dso.getRawData(True, 1)
        dso.getRawData(True, 2)
        dso.getRawData(True, 3)

        waveform = []

        # The convertWaveForm function takes the raw data from the dso object, formats it as a list of floats, and then returns that list
        waveform.append(dso.convertWaveform(1, 1))
        waveform.append(dso.convertWaveform(2, 1))
        waveform.append(dso.convertWaveform(3, 1))
        dso.resetChList()

        waveform = np.array(waveform)
        np.savetxt(f'/home/trd/prac2021/data/timeResolutionData/run_{args.run}/{i}.csv', waveform, header=nowString, delimiter=',')
    else:
        pass