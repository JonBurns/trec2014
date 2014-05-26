#!/usr/bin/env python
import sys
#import cPickle as pickle 

listy = []
words_and_idxs = []
cur_col = 0
max_words = 0
first = True

for line in sys.stdin:
    #print line
    data = line.split('\t')
    marker = data[0] 
    max_words = int(data[1])
    data = data[2:-1]

    listy.append([0] * max_words)
    values = {}

    for item in data:
        row, value = item.split(' ')
        listy[cur_col][int(row)] = float(value)
    
    print '{0}\t{1}\t{2}'.format(str(cur_col), marker.strip(), repr(listy[cur_col]))
    #print '{0}\t{1}'.format(str(cur_col), marker.strip())
    #words_and_idxs.append('{0}\t{1}'.format(str(cur_col), marker.strip()))
    cur_col += 1
    #print '{0}\t{1}'.format(str(cur_col), marker.strip())


