from sklearn.feature_extraction.text import TfidfVectorizer

from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

import nltk.data

import os

from os import listdir
from os.path import isfile, join

from sklearn.metrics.pairwise import cosine_similarity

import sys

from sklearn.metrics.pairwise import pairwise_kernels

import re

path = '/Users/jonathanburns/docs/D0701A'

class LemmaTokenizer(object):
	def __init__(self):
		self.wnl = WordNetLemmatizer()

	def __call__(self, doc):
		return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

def l1(sim_matrix, s, corpus_sums): #summary is collection of indicies
	n = sim_matrix.shape[0]
	alpha = 100.0/n
	score_sum = 0.0

	for i in range(n):
		#Optimize sim_matrix[i].sum()
		score_sum += min([sum([sim_matrix[i, j] for j in s]), (alpha * corpus_sums[i])])
		#sum += min(1, (alpha * sim_matrix[i].sum()))
	return score_sum

def greedy(sim_matrix, reward, corpus_sums): #reward is a function
	st = [] #s at t
	while len(st) < 10: #Length violation test
		print "Starting iteration: ", len(st)
		scoret = reward(sim_matrix, st, corpus_sums)
		max_gain = 0.0
		max_gain_idx = -1

		for i in [i for i in range(sim_matrix.shape[0]) if i not in st]:
			temp = list(st)
			temp.append(i)
			gain = reward(sim_matrix, temp, corpus_sums) - scoret
			if gain > max_gain:
				max_gain = gain
				max_gain_idx = i

		st.append(max_gain_idx)

	return st


onlyfiles = [f for f in listdir(path) if isfile(join(path, f))] #Directory Taken as Command Line Argument

docs = []

for filename in onlyfiles:
	f = open(path + '/' + filename, 'r')
	docs.append(f.read())


vectorizer = TfidfVectorizer(input = 'content', ngram_range = (1, 2), stop_words = 'english', tokenizer = LemmaTokenizer(), norm = 'l2', smooth_idf = True) #Add Stemming 
vectorizer.fit(docs)

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

sentences = []

for doc in docs:
	for sentence in sent_detector.tokenize(doc.strip()):
		if len(sentence) > 25 and not re.match(".*``.*", sentence) and not re.match(".*''.*", sentence): 
			sentences.append(sentence)

sentences = list(set(sentences))

tfidf = vectorizer.transform(sentences)

sim_matrix = pairwise_kernels(tfidf.todense(), metric = 'cosine')

corpus_sums = []

for i in range(sim_matrix.shape[0]):
	corpus_sums.append(sim_matrix[i].sum())

if __name__ == '__main__':
	idxs = greedy(sim_matrix, l1, corpus_sums)

	print idxs

	for idx in idxs:
		print sentences[idx]
#sum += min(sum([sim_matrix[i, j] for j in s]), (alpha * sim_matrix[i].sum()))


#vectors = vectorizer.transform(sentences)

#x = vectorizer.transform(["Another man , Joe Oliver Watson , pleaded guilty to manslaughter in the case this summer and is awaiting sentencing ."])
#print x.sum()