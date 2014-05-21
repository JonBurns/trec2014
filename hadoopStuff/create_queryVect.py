import cPickle as pickle
import os
from os import listdir
from os.path import isfile, join
import sys
from tokenizers import *

from sklearn.feature_extraction.text import CountVectorizer

path = '../ROUGE/DUC-2007/docs/D0701A'



q_vectorizer = CountVectorizer(input = 'content', ngram_range = (1, 2), stop_words = 'english', tokenizer=QuerySynsetExpandingTokenizer())
with open(path + '/query.txt') as f:
    q_vectorizer.fit(f.readlines())

pickle.dump(q_vectorizer, open('query_vectorizer.p', 'wb'))