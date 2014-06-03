#!/usr/bin/env python

import sys
import cPickle as pickle 
from sklearn.metrics.pairwise import pairwise_kernels
import numpy

vector = pickle.load(open('vectorized_sentences.p', 'rb'))

sim_matrix = pairwise_kernels(vector, metric = 'cosine')

i = 0
for row in sim_matrix:
    sys.stdout.write('{0}\t'.format(str(i)))
    for item in row:
         sys.stdout.write(str(item))
         sys.stdout.write(' ')
    sys.stdout.write('\n')
    i += 1


pickle.dump(sim_matrix, open('sim_matrix.p', 'wb'))

