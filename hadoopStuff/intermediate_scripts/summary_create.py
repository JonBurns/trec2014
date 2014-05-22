#!/usr/bin/env python

import cPickle as pickle 
import sys

summary = []
for line in sys.stdin:
    idx = int(line)
    summary.append(idx)
pickle.dump(summary, open('summary.p', 'wb'))