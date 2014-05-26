import sys
import cPickle as pickle

sentences = pickle.load(open('indexed_sentences.p', 'rb'))

with open('greedy_result.txt') as f:
    content = f.readlines()

for idx in content:
    print sentences[int(idx)]
