#!/usr/bin/env python
import sys
import cPickle as pickle 
import numpy

#text is coming in as [idx]\t[sum_of_vector]
#we want a list such that cs[idx] = sum_of_vector

highest_idx = 0

sum_of_vectors = {}

for line in sys.stdin:
    data = line.strip().split('\t')
    if len(data) != 2:
        break
    idx = int(data[0])
    sum_of_vec = float(data[1])
    sum_of_vectors[idx] = sum_of_vec

    if idx > highest_idx:
        highest_idx = idx

list_of_sums = numpy.empty(highest_idx + 1)


for key in sum_of_vectors:
    list_of_sums[int(key)] = sum_of_vectors[key]

pickle.dump(list_of_sums, open('corpus_sums.p', 'wb'))