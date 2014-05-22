#!/usr/bin/env python

import sys
import scipy.sparse

import cPickle as pickle

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = pickle.load(open('query_vectorizer.p', 'rb'))


for line in sys.stdin:
    listy = []
    data = vectorizer.transform([line])
    data = data.tocoo()

    for i,j,v in zip(data.row, data.col, data.data):
        listy.append(str(j) + ' ' + str(v))

    sys.stdout.write('{0}\t{1}\t'.format(line.strip(), data.shape[1]))
    for item in listy:
        sys.stdout.write(item)
        sys.stdout.write('\t')
    sys.stdout.write('\n')