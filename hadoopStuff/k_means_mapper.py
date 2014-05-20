#!/usr/bin/env python

import sys
import cPickle as pickle

from sklearn.metrics.pairwise import pairwise_distances

groups = pickle.load(open('kmeans_groups.p', 'rb'))

for line in sys.stdin: #for each sentence
    line = line.split('\t')
    idx = line[0]
    vector = eval(line[1])
    lowest = 1000
    lowest_idx = 0
    for group_num in range(len(groups)):
        distance = pairwise_distances(groups[group_num], vector)[0][0]
        if distance < lowest:
            lowest = distance
            lowest_idx = group_num
    
    print '{0}\t{1}'.format(lowest_idx, idx)

    # sys.stdout.write('{0}\t{1}\t'.format(line.strip(), data.shape[1]))
    # for item in listy:
    #     sys.stdout.write(item)
    #     sys.stdout.write('\t')
    # sys.stdout.write('\n')