#!/usr/bin/env python

import sys

listy = []
cur_col = 0
max_words = 0
first = True

for line in sys.stdin:
    if first:
        max_words = int(line)
        first = False;
        continue

    print max_words
    listy.append([0] * max_words)
    values = {}

    data = line.split('\t')
    marker = data[0] 
    data = data[1:-1]

    for item in data:
        row, value = item.split(' ')
        listy[cur_col][int(row)] = float(value)
    
    for i in listy[cur_col]:
        if i != 0:
            print 'Yay'
    cur_col += 1
    print '_____________________________________________________'

