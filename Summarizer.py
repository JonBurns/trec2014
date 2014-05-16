from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from tokenizers import *

from algorithms import greedy
    
from nltk import word_tokenize
import nltk.data

import os
from os import listdir
from os.path import isfile, join

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import pairwise_kernels
from sklearn.cluster import KMeans

import sys
import re
from itertools import groupby
import math

from functools import partial 

from rewards import l1, r1

alpha_passed = 12
beta_passed = .5
lambda_passed = 6
r_passed = 0

iter_sys = 2
while iter_sys < len(sys.argv):
    if iter_sys == 2:
        alpha_passed = int(sys.argv[2])
    if iter_sys == 3:
        beta_passed = float(sys.argv[3])
    if iter_sys == 4:
        lambda_passed = int(sys.argv[4])
    if iter_sys == 5: 
        r_passed = float(sys.argv[5])
    iter_sys += 1
    
# def reward(s, sim_matrix, corpus_sums, groups, rqj):
#     return l1(s, sim_matrix, corpus_sums) + (6 * r1(s, corpus_sums, groups, rqj))

def reward(s, l1, r1, lambda_var = 6):
    return l1(s) + (lambda_var * r1(s))


def file_setup(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))] #Directory Taken as Command Line Argument

    docs = []
    for filename in onlyfiles:
        if re.match("^(APW|NYT|XIE)", filename):
            f = open(os.path.join(path, filename), 'r')
            docs.append(f.read())

    return docs

def split_into_sentences(docs, use_splitter = False):
    sentences = []
    if not use_splitter:
        for doc in docs:
            for sentence in doc.split('\n'):
                if len(sentence) > 25 and not re.match(".*``.*", sentence) and not re.match(".*''.*", sentence): 
                    sentences.append(sentence)
        return list(set(sentences))

    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    for doc in docs:
        for sentence in sent_detector.tokenize(doc.strip()):
            if len(sentence) > 25 and not re.match(".*``.*", sentence) and not re.match(".*''.*", sentence): 
                sentences.append(sentence)
    return list(set(sentences))


def create_groups(clusters):
    c1 = []
    for x in range(len(clusters)):
        c1.append([x, clusters[x]])

    c1.sort(key = lambda x: x[1])

    return [map(lambda x: x[0], g) for k, g in groupby(c1, lambda x: x[1])]


def contraction_filter(sentence):
    to_replace = {' n\'t' : 'n\'t',' \'s' : ''}
    for i, j in to_replace.iteritems():
        sentence = sentence.replace(i, j)

    return sentence

def replace_all(sentence):
    to_replace = {' ,' : ',', ' .' : '.', ' ?' : '?', ' !' : '!', '$ ' : '$'}
    for i, j in to_replace.iteritems():
        sentence = sentence.replace(i, j)

    return sentence

if __name__ == '__main__':
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), ('ROUGE/DUC-2007/docs/' + sys.argv[1]))
    with open('ROUGE/smart_common_words.txt') as f:
        new_stop_words = f.read().splitlines()

    docs = file_setup(path)
    docs = [contraction_filter(doc) for doc in docs]
    sentences = split_into_sentences(docs)

    vectorizer = TfidfVectorizer(input = 'content', ngram_range = (1, 2), stop_words = new_stop_words, tokenizer = LemmaTokenizer(), norm = 'l2', smooth_idf = True, max_features=200) #Add Stemming 
    vectorizer.fit(docs)
    q_vectorizer = CountVectorizer(input = 'content', ngram_range = (1, 2), stop_words = new_stop_words, tokenizer=QuerySynsetExpandingTokenizer())
    with open(path + '/query.txt') as f:
        q_vectorizer.fit(f.readlines())

    tfidf = vectorizer.transform(sentences)
    query_matrix = q_vectorizer.transform(sentences)
    rqj = []
    for i in range(query_matrix.shape[0]):
        rqj.append(query_matrix[i].sum())

    sim_matrix = pairwise_kernels(tfidf.todense(), metric = 'cosine')

    kcluster = KMeans(init = 'k-means++', n_init = 10, n_clusters = len(sentences)/5) #n-clusters is K
    clusters = kcluster.fit_predict(tfidf.todense())

    groups = create_groups(clusters) #[map(lambda x: x[0], g) for k, g in groupby(c1, lambda x: x[1])]

    corpus_sums = []

    for i in range(sim_matrix.shape[0]):
        corpus_sums.append(sim_matrix[i].sum())

    lengths = []

    for sentence in sentences:
        lengths.append(len(word_tokenize(sentence)))

    reward_l1 = partial(l1, sim_matrix = sim_matrix, corpus_sums = corpus_sums, alpha_numer = alpha_passed)
    reward_r1 = partial(r1, corpus_sums = corpus_sums, groups = groups, rqj = rqj, beta = beta_passed)

    filled_reward = partial(reward, l1 = reward_l1, r1 = reward_r1, lambda_var = lambda_passed)
    idxs = greedy(sim_matrix, filled_reward, lengths, r=r_passed)

    for idx in idxs:
        print replace_all(sentences[idx])
