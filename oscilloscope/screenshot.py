#!/usr/bin/env python3
"""
Takes a screeshot of the current oscilloscope screen and saves it to the folder under the name given by the user.
"""
import matplotlib.pyplot as plt

from oscilloscope import dso1kb
import os

dso=dso1kb.Dso('/dev/ttyACM2')

dso.write(':DISP:OUTP?\n')
dso.getBlockData()
dso.ImageDecode(1)

plt.imshow(dso.im)
saveName = str(input('Enter the name the screenshot will be saved under: '))
# requires a screenshots folder in the outer directory
plt.savefig(f'screenshots/{saveName}.png')
