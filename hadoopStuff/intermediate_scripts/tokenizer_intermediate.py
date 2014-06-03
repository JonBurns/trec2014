#!/usr/bin/env python
import sys
import cPickle as pickle 
import numpy

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

# idx_sent = [0] * (highest_idx + 1)
vect_sent = [0] * (highest_idx + 1)
# len_sent = [0] * (highest_idx + 1)

idx_sent = numpy.empty(highest_idx + 1, dtype = "S500")
#vect_sent = numpy.empty(highest_idx + 1)
len_sent = numpy.empty(highest_idx + 1)

for key in indexed_sentences:
    idx_sent[int(key)] = indexed_sentences[key]
    vect_sent[int(key)] = vectorized_sentences[key]
    len_sent[int(key)] = len(indexed_sentences[key])
    print '{0}\t{1}'.format(str(key), repr(vect_sent[int(key)]))
    

vect_sent = numpy.array(vect_sent)    
pickle.dump(vect_sent, open('vectorized_sentences.p', 'wb'))
pickle.dump(idx_sent, open('indexed_sentences.p', 'wb'))
pickle.dump(len_sent, open('sentence_lengths.p', 'wb'))