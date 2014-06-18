#!/usr/bin/env python

import sys
import cPickle as pickle 
import numpy


for line in sys.stdin: #Each line will be 'sent_idx\tvector'
    line = line.split('\t')
    idx = line[0]
    vector = eval(line[1])
    sum_vect = 0.0
    for i in vector:
        sum_vect += int(i)
    print '{0}\t{1}'.format(idx, sum_vect)

