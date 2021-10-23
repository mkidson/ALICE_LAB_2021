import dso1kb
import numpy as np
import matplotlib.pyplot as plt

dso=dso1kb.Dso('10.10.0.20:3001', True)
dso.getRawData(True, 1)
fwave1 = []
fwave1 = dso.convertWaveform(1, 1)
dso.getRawData(True, 2)
fwave2 = []
fwave2 = dso.convertWaveform(2, 1)
dso.getRawData(True, 3)
fwave3 = []
fwave3 = dso.convertWaveform(3, 1)

tArr = np.arange(0,len(fwave1))
plt.plot(tArr, fwave1, label='ch1')
plt.plot(tArr, fwave2, label='ch2')
plt.plot(tArr, fwave3, label='ch3')
plt.legend()
plt.savefig('testplot.png')