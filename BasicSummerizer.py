from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

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

from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

#new_stop_words = set('.').union(set(',')).union(set('\"')).union(ENGLISH_STOP_WORDS)

#new_stop_words = ENGLISH_STOP_WORDS

path = os.path.join(os.path.dirname(os.path.realpath(__file__)), ('ROUGE/DUC-2007/docs/' + sys.argv[1]))

with open('ROUGE/smart_common_words.txt') as f:
    new_stop_words = f.read().splitlines()

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

def get_synset(token):
    return [l.name for l in s.lemmas for s in wn.synsets(token)]

class QuerySynsetExpandingTokenizer(object):
    def __init__(self):
        self.first_run = True

  def __call__(self, doc):
      if self.first_run:
          self.query = doc
      self.query_tokens = [t for t in word_tokenize(doc)]
      self.query_set set(self.query_tokens)
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
              overlap = self.query_set.intersection(set(synonym_map[token]))
            if len(overlap):
                token = overlap[0]
    return tokens


def l1(sim_matrix, s, corpus_sums): #summary is collection of indicies
    n = sim_matrix.shape[0]
    alpha = 12.0/n
    score_sum = 0.0

    for i in range(n):
        score_sum += min([sum([sim_matrix[i, j] for j in s]), (alpha * corpus_sums[i])])
    return score_sum

def r1(corpus_sums, s, groups, rqj, beta = 0.5):
    k = len(groups)
        n = len(corpus_sums)

        result = 0.0
        for p in groups:
            result2 = 0.0
            for j in set(p).intersection(set(s)):
                result2 += ((beta/n) * corpus_sums[j] + ((1 - beta) * rqj[j]))

            result += math.sqrt(result2)

        return result

def reward(sim_matrix, s, corpus_sums, groups, rqj):
    return l1(sim_matrix, s, corpus_sums) + (6 * r1(corpus_sums, s, groups, rqj))

def greedy(sim_matrix, reward, corpus_sums, groups, rqj, lengths): #reward is a function
    st = [] #s at t
    length = 0
    while length <= 250: #Length violation test
        scoret = reward(sim_matrix, st, corpus_sums, groups, rqj) #Maybe save the score when we calculate it in the while loop?
        max_gain = 0.0
        max_gain_idx = -1

        for i in [i for i in range(sim_matrix.shape[0]) if i not in st and lengths[i] <= 250 - length]:
            temp = list(st)
            temp.append(i)
            gain = (reward(sim_matrix, temp, corpus_sums, groups, rqj) - scoret)
            if gain > max_gain:
                max_gain = gain
                max_gain_idx = i

        if max_gain_idx == -1:
            break

        st.append(max_gain_idx)
        length += lengths[max_gain_idx]

    return st

def file_setup(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))] #Directory Taken as Command Line Argument

    docs = []
    for filename in onlyfiles:
        if re.match("^(APW|NYT|XIE)", filename):
            f = open(os.path.join(path, filename), 'r')
            docs.append(f.read())

    return docs

def split_into_sentences(docs, nltk = False):
    sentences = []
    if not nltk:
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

def nouns_and_verbs(sentence):

    verbs_nouns = [word for word in word_tokenize(sentence) if nltk.pos_tag([word])[0][1][0] == 'N' or nltk.pos_tag([word])[0][1][0] == 'V']

    return verbs_nouns


docs = file_setup(path) #Do string replaces here on every doc (sentences) 


##################__CONTRACTION_REPLACEMENT__############

docs = [contraction_filter(doc) for doc in docs]

##################__STRING_REPLACEMENT__#################

#docs = [replace_all(doc) for doc in docs]

##################__VECTORIZERS__########################

vectorizer = TfidfVectorizer(input = 'content', ngram_range = (1, 2), stop_words = new_stop_words, tokenizer = LemmaTokenizer(), norm = 'l2', smooth_idf = True) #Add Stemming 
vectorizer.fit(docs)

q_vectorizer = CountVectorizer(input = 'content', ngram_range = (1, 2), stop_words = new_stop_words, tokenizer=QuerySynsetExpandingTokenizer())

with open(path + '/query.txt') as f:
    q_vectorizer.fit(f.readlines())


##################__SENTENCE_CREATION__########################

sentences = split_into_sentences(docs)

#################__GET_NOUNS_AND_VERBS_STUFF__#################

# for sentence in sentences:
# 	print nouns_and_verbs(sentence)

###############################################################

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

idxs = greedy(sim_matrix, reward, corpus_sums, groups, rqj, lengths)

for idx in idxs:
    print replace_all(sentences[idx])





