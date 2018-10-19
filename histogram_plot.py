# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
import sys

source = open(sys.argv[1], 'r')
raw_values = []
max_length = 0
max_height = 0

for line in source.readlines():
    str_values = line.split(',')

    for value in str_values:
        int_value = int(value)
        raw_values.append(int_value)
        if int_value > max_length:
            max_length = int_value

histogram = np.zeros(max_length + 1, dtype=int).tolist()

for value in raw_values:
    histogram[value] += 1

for value in histogram:
    if value > max_height:
        max_height = value

for i, value in enumerate(histogram):
    if value > 1400:
        print i,',',

#plot
plt.bar(range(len(histogram)), height = histogram)
# plt.xticks(range(70), [str(i) for i in range(70)])

#plt.xticks(y_pos, objects)
plt.xlabel('Individuo')
plt.ylabel('Vezes Selecionado')
plt.title('GASIR - Genetic Algorithm for SIR Model')
plt.show()