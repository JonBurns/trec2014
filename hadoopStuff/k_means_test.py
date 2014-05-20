#!/usr/bin/env python

import subprocess
import os

total_iters = 20

for i in range(total_iters):
    print "{0}% complete".format((float(i + 1)/float(total_iters)) * 100)
    callOne = './k_means_mapper.py < dataSet_tokenized.txt > DataFiles/dataSet_clustered' + str(i) + '.txt'
    subprocess.call(callOne, shell = True)
    callTwo = 'sort DataFiles/dataSet_clustered' + str(i) + '.txt > DataFiles/dataSet_clusteredSorted' + str(i) + '.txt'
    subprocess.call(callTwo, shell = True)
    callThree = './k_means_reducer.py < DataFiles/dataSet_clusteredSorted' + str(i) + '.txt > DataFiles/k_meansRed' + str(i) + '.txt'
    subprocess.call(callThree, shell = True)