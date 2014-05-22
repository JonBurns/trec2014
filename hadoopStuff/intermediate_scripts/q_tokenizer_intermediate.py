#!/usr/bin/env python
import sys
import cPickle as pickle 

#text is coming in as [idx]\t[sentence]\t[vector]


vectorized_sentences = {}
highest_idx = 0

for line in sys.stdin:
    data = line.strip().split('\t')
    idx = int(data[0])
    q_vector = eval(data[1])
    vectorized_sentences[idx] = q_vector
    if idx > highest_idx:
        highest_idx = idx

vect_sent = [0] * (highest_idx + 1)

for key in vectorized_sentences:
    vect_sent[int(key)] = vectorized_sentences[key]

pickle.dump(vect_sent, open('q_vectorized_sentences.p', 'wb'))