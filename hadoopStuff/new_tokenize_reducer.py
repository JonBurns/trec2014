#!/usr/bin/env python
import sys
import cPickle as pickle 

listy = []
words_and_idxs = []
cur_col = 0
max_words = 0
first = True

for line in sys.stdin:
    data = line.split('\t')
    marker = data[0] 
    max_words = int(data[1])
    data = data[2:-1]

    listy.append([0] * max_words)
    values = {}

    for item in data:
        row, value = item.split(' ')
        listy[cur_col][int(row)] = float(value)
    
    print '{0}\t{1}'.format(str(cur_col), repr(listy[cur_col]))
    words_and_idxs.append('{0}\t{1}'.format(str(cur_col), marker.strip()))
    cur_col += 1
    #print '{0}\t{1}'.format(str(cur_col), marker.strip())


pickle.dump(listy, open('vectorized_sentences.p', 'wb'))
pickle.dump(listy, open('indexed_sentences.p', 'wb'))

