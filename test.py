import dso1kb
dso=dso1kb.Dso("10.10.0.20:3001")
dso.getRawData(True, 1)
fwave = []
fwave = dso.convertWaveform(1, 1)
# print(fwave)
f = open('testData.csv', 'w')
f.write(fwave)
f.close()

