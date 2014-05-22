#!/usr/bin/env python

import sys
import cPickle as pickle 

sim_matrix = pickle.load(open('sim_matrix.p', 'rb'))

for line in sys.stdin:
    data = line.split('\t', 1)
    idx = int(data[0])
    sum_vec = sim_matrix[idx].sum()

    print '{0}\t{1}'.format(str(idx), str(sum_vec))