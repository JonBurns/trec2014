#!/usr/bin/env python

import sys

import cPickle as pickle 
from sklearn.metrics.pairwise import pairwise_kernels

listy = []
cur_col = 0
max_words = 0
first = True

for line in sys.stdin:
    if first:
        max_words = int(line)
        first = False;
        continue

    listy.append([0] * max_words)
    values = {}

    data = line.split('\t')
    marker = data[0] 
    data = data[1:-1]

    for item in data:
        row, value = item.split(' ')
        listy[cur_col][int(row)] = float(value)
    
    cur_col += 1
    print '{0}\t{1}'.format(str(cur_col), marker.strip())

sim_matrix = pairwise_kernels(listy, metric = 'cosine')

pickle.dump(sim_matrix, open('sim_matrix.p', 'wb'))

