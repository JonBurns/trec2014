import cPickle as pickle
import os
from os import listdir
from os.path import isfile, join
import sys
import re
from tokenizers import *

from sklearn.feature_extraction.text import TfidfVectorizer

path = '../ROUGE/DUC-2007/docs/D0701A'

def file_setup(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))] #Directory Taken as Command Line Argument

    docs = []
    for filename in onlyfiles:
        if re.match("^(APW|NYT|XIE)", filename):
            f = open(os.path.join(path, filename), 'r')
            docs.append(f.read())

    return docs


docs = file_setup(path)

vectorizer = TfidfVectorizer(input = 'content', ngram_range = (1, 2), stop_words = 'english', tokenizer = LemmaTokenizer(), norm = 'l2', smooth_idf = True)
vectorizer.fit(docs)

pickle.dump(vectorizer, open('vectorizer.p', 'wb'))