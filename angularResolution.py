#!/usr/bin/env python3
"""
Program designed to be able to take a number of events from just the scintillators in order to make measurements for both time resolution and angular resolution.
It takes both the run name and number of events as arguments when running the program, and should cancel the run if a run with that name already exists, just to avoid writing over data.

NB: needs the scope to be triggering off the trigger from the TRDbox

Author: Miles Kidson
"""

from oscilloscopeRead import scopeRead
import datetime
import time
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

# Creates a Reader object. 
scope = scopeRead.Reader('ttyACM2')

# Makes a new directory for the data. You will need to change the path to this for when you save data. This checks if the run exists and if it does, exits, else it creates a directory for the data and carries on

if os.path.isdir(f'/home/trd/prac2021/data/angularResolutionData/run_{args.run}'):
    print('That run already exists, change run number to avoid writing over data')
    exit(0)
else: 
    os.mkdir(f'/home/trd/prac2021/data/angularResolutionData/run_{args.run}')

# This loop continuously checks if the TRDbox has sent a trigger by checking if the registry corresponding to number of triggers has changed. It relies heavily on the form of the output of trdbox reg-read, so it might need to be modified to accomodate in the event that that changes
trig_count_1 = int(os.popen('trdbox reg-read 0x102').read().split('\n')[0])
os.system('trdbox unblock')
trig_count_2 = 0
i = 0
t1 = time.time()
while i < (int(args.n_events)):
    trig_count_2 = int(os.popen('trdbox reg-read 0x102').read().split('\n')[0])

    if trig_count_2 != trig_count_1:
        i += 1
        print(i)
        now = datetime.datetime.now()
        nowString = now.strftime('%Y.%m.%d.%H.%M.%S')

        waveform = scope.getData([1,2,3])

        # Saves the data as a csv containing the data from each channel in a separate line, separated by commas. The time of the event is also saved as the header. To extract the data just do data = np.genfromtxt(filename, delimiter=',', skip_header=1)
        np.savetxt(f'/home/trd/prac2021/data/angularResolutionData/run_{args.run}/{i}.csv', waveform, header=nowString, delimiter=',')
        trig_count_1 = trig_count_2

        os.system('trdbox unblock')
    else:
        pass

t2 = time.time()
print('Time taken:', t2-t1)

f = open(f'/home/trd/prac2021/data/angularResolutionData/run_{args.run}/timeTaken.txt', 'w')
f.write(str(t2-t1))