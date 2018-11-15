import sys
import numpy as np
import matplotlib.pyplot as plt

source = open(sys.argv[1], 'r')
raw_cvg = source.readlines()

cvg = np.zeros(len(raw_cvg) / 100, dtype=float).tolist()

for i in range(len(raw_cvg)):
    cvg[i % len(raw_cvg) % 200] += float(raw_cvg[i])

for i in range(len(cvg)):
    cvg[i] /= float(len(cvg))

cvg = cvg[10:]



cvg_min = min(cvg)
cvg_max = max(cvg)
cvg_avg = sum(cvg) / float(len(cvg))

font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 10,
        }


plt.plot(cvg)
plt.ylabel('Infeccoes')
plt.xlabel('Geracoes')
plt.text(30, cvg_max, 'max: ' + str(cvg_max), fontdict=font)
plt.text(70, cvg_max, 'min: ' + str(cvg_min), fontdict=font)
plt.text(110, cvg_max, 'avg: ' + str(cvg_avg), fontdict=font)
plt.savefig(sys.argv[1].replace('.txt','.png'))