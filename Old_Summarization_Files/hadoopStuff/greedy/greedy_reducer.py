#!/usr/bin/env python

import cPickle as pickle 

import sys

old_key = None #index
summary = pickle.load(open('summary.p', 'rb'))

highest_idx = -1
highest_score = 0

for line in sys.stdin:
    data = line.strip().split('\t')
    idx = int(data[0])
    
    value = float(data[1])
    if value > highest_score:
        highest_idx = idx
        highest_score = value

if highest_idx != -1:
    summary.append(highest_idx)

for idx in summary:
    print idx