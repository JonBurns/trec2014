#!/usr/bin/env python

import sys
import scipy.sparse

import cPickle as pickle

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = pickle.load(open('vecotrizer.p', 'rb'))

temp = vectorizer.transform(['temp'])
print temp.shape[1]

for line in sys.stdin:
    listy = []
    data = vectorizer.transform([line])
    data = data.tocoo()

    for i,j,v in zip(data.row, data.col, data.data):
        listy.append(str(j) + ' ' + str(v))

    sys.stdout.write('marker\t')
    for item in listy:
        sys.stdout.write(item)
        sys.stdout.write('\t')
    sys.stdout.write('\n')