#!/usr/bin/env python

import sys
import cPickle as pickle
import time

for line in sys.stdin:
    data = line.strip().split('\t')
    print '{0}\t{1}'.format(data[1], data[2])