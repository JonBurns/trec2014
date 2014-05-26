#!/usr/bin/env python

import sys
import scipy.sparse

import cPickle as pickle

from sklearn.feature_extraction.text import CountVectorizer

import subprocess

from nltk.corpus import wordnet as wn
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

nltk.data.path.append('./nltk_data')

cmd = 'unzip nltk_data.zip'

retcode = subprocess.check_output(cmd, shell = True)

###FOR PICKLE###

def nouns_and_verbs(sentence):
    verbs_nouns = [word for word in word_tokenize(sentence) if nltk.pos_tag([word])[0][1][0] == 'N' or nltk.pos_tag([word])[0][1][0] == 'V']
    return verbs_nouns

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

#Now also includes hypernyms (Hopefully)
def get_synset(token):
    syn_sets = wn.synsets(token)
    nested_lemmas = [s.lemmas for s in syn_sets]
    lemmas = []
    for lemma_list in nested_lemmas:
        for lemma in lemma_list:
            lemmas.append(lemma.name.replace('_', ' '))

    if len(syn_sets) > 1:
        holder_for_hypers = syn_sets[0].hypernyms()
        for hyp in holder_for_hypers:
            for lemma in hyp.lemmas:
                lemmas.append(lemma.name.replace('_', ' '))


    #This is code for if we want the hypernames of every word in the syn_set
    #Warning: if this is done then 'dog' could be replaced with 'fellow'
    # holder_for_hypers = [syn.hypernyms() for syn in syn_sets]
    # for nested_hyp in holder_for_hypers:
    #     for hyp in nested_hyp:
    #         for lemma in hyp.lemmas:
    #             print "hyp: {0}".format(lemma.name)
    #             lemmas.append(lemma.name.replace('_', ' '))

    return list(set(lemmas)) #Using nested lemmas means lots of duplicated, this removes them

class QuerySynsetExpandingTokenizer(object):
    def __init__(self):
        self.first_run = True

    def __call__(self, doc):
        if self.first_run:
            self.query = doc
            self.query_tokens = [t for t in word_tokenize(doc)]

            self.query_set = set(self.query_tokens)
            self.first_run = False
            return self.query_tokens
        else:
            nouns_verbs = nouns_and_verbs(doc)
            tokens = [t for t in word_tokenize(doc)]
            syns = {}
            for nv in nouns_verbs:
                syns[nv] = get_synset(nv)

            # Replace tokens with synonyms if they occur in the query
            for token in tokens:
                if token in nouns_verbs:
                    overlap = self.query_set.intersection(set(syns[token]))
                    if len(overlap):
                        token = list(overlap)[0]
        return tokens

        
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