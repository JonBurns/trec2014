#!/usr/bin/env python

import sys
import cPickle as pickle
import time

from sklearn.metrics.pairwise import pairwise_distances

groups = pickle.load(open('kmeans_groups.p', 'rb'))

for line in sys.stdin: #for each sentence
    start_time_t = time.time()
    line = line.split('\t')
    idx = line[0]
    vector = eval(line[1])
    lowest = sys.maxint
    lowest_idx = 0

    list_of_times = []
    for group_num in range(len(groups)):
        start_time = time.time()
        distance = pairwise_distances(groups[group_num], vector)[0][0]
        elapsed_time = time.time() - start_time
        list_of_times.append(elapsed_time)
        if distance < lowest:
            lowest = distance
            lowest_idx = group_num
    
    elapsed_time_t = time.time() - start_time_t
    #print '{0}\t{1}'.format(lowest_idx, idx)
    total = 0
    for a_time in list_of_times:
        total += a_time
    print '{0}\t{1}\t{2}'.format(lowest_idx, idx, str(elapsed_time_t - total))

    # sys.stdout.write('{0}\t{1}\t'.format(line.strip(), data.shape[1]))
    # for item in listy:
    #     sys.stdout.write(item)
    #     sys.stdout.write('\t')
    # sys.stdout.write('\n')