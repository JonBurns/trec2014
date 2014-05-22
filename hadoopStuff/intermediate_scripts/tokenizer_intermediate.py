#!/usr/bin/env python
import sys
import cPickle as pickle 

#text is coming in as [idx]\t[sentence]\t[vector]

indexed_sentences = {}
vectorized_sentences = {}
highest_idx = 0
for line in sys.stdin:
    data = line.strip().split('\t')
    idx = int(data[0])
    sentence = data[1]
    vector = eval(data[2])
    indexed_sentences[idx] = sentence
    vectorized_sentences[idx] = vector
    if idx > highest_idx:
        highest_idx = idx

idx_sent = [0] * (highest_idx + 1)
vect_sent = [0] * (highest_idx + 1)

for key in indexed_sentences:
    idx_sent[int(key)] = indexed_sentences[key]
    vect_sent[int(key)] = vectorized_sentences[key]
    print '{0}\t{1}'.format(str(key), vect_sent[int(key)])

pickle.dump(vect_sent, open('vectorized_sentences.p', 'wb'))
pickle.dump(idx_sent, open('indexed_sentences.p', 'wb'))