import dso1kb_1
import numpy as np
import matplotlib.pyplot as plt

dso=dso1kb_1.Dso("10.10.0.20:3001")
dso.getRawData(True, 1)
fwave = []
fwave = dso.convertWaveform(1, 1)

tArr = np.arange(0,len(fwave))
plt.plot(tArr, fwave)
plt.savefig('testplot.png')