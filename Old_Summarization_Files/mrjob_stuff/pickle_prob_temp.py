import cPickle as pickle
import sys

fname = str(sys.argv[1])

with open(fname, 'r') as f:
    content = f.readlines()



query = {}

for sentence in content:
    data = sentence.strip().split('\t')
    key = data[0].replace('\"', '')
    value = float(data[1])
    query[key] = value

pickle.dump(query, open('qidx.p', 'wb'))