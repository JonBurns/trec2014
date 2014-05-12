import os
import sys 

path = 'ROUGE/DUC-2007/docs/'
path2 = 'ROUGE/DUC-2007/'

lines = os.listdir(path)

i = 1

with open('./runAll.sh', 'w') as f:
    f.write('#!/bin/bash' + '\n')
    while i < len(lines):
        cluster = lines[i]
        cluster1 = cluster[:-1]
        f.write('{ echo ' + '\'' + cluster + '\'' + '; } >> timingInfo.txt' + '\n')
        f.write('{ time  python BasicSummerizer.py ' + cluster + ' >> ' + path2 + 'SYSTEM/' + cluster1 + '/' + cluster1 + '.' + sys.argv[1] + '.system; } 2>> timingInfo.txt' + '\n')
        i += 1

    f.write('cd ROUGE; ./duc2007.prepare.pl' + '\n')
    f.write('cd ROUGE-EVAL; ./runROUGE.pl' + '\n')
    f.write('cd ../../; python getResults.py ' + sys.argv[1] + '\n')
    f.write('subl results.txt' + '\n')