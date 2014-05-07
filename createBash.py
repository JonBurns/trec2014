import os

path = 'ROUGE/DUC-2007/docs/'
path2 = 'ROUGE/DUC-2007/'

lines = os.listdir(path)

i = 1

with open('./runAll.sh', 'w') as f:
	f.write('#!/bin/bash' + '\n')
	while i < len(lines):
		cluster = lines[i]
		cluster1 = cluster[:-1]
		f.write('python BasicSummerizer.py ' + cluster + ' >> ' + path2 + 'SYSTEM/' + cluster1 + '/' + cluster1 + '.max-reward-with-nsw.system' + '\n')
		i += 1
