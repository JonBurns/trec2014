#!/usr/bin/env python
import sys
import cPickle as pickle 

groups = pickle.load(open('kmeans_groups.p', 'rb'))
groupings = [0] * len(groups)

#text comes in as: [group]\t[list of indexes belonging to it]\t[vector of group]
for line in sys.stdin:
    data = line.strip().split('\t')
    group_num = int(data[0])
    indexes = eval(data[1])
    vector = eval(data[2])
    groups[group_num] = vector
    groupings[group_num] = indexes

pickle.dump(groups, open('kmeans_groups.p', 'wb'))
pickle.dump(groupings, open('kmeans_groupings.p', 'wb'))