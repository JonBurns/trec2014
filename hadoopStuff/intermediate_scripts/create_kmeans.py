#!/usr/bin/env python
import sys
import cPickle as pickle 
import random 
import numpy

vectorized_sentences = pickle.load(open('vectorized_sentences.p', 'rb'))
random.shuffle(vectorized_sentences)

num_sentences = len(vectorized_sentences)
num_groups = num_sentences/5

groups = numpy.empty(num_groups, dtype = list)
for i in range(num_groups):
    list_of_vectors = []
    averaged_vector = []
    for j in range(10):
        list_of_vectors.append(vectorized_sentences[random.randint(0, num_sentences - 1)])
    for j in range(len(vectorized_sentences[0])):
        sum = 0.0
        for vector in list_of_vectors:
            sum += vector[j]
        averaged_vector.append(sum/float(len(list_of_vectors)))
    groups.append(averaged_vector)


pickle.dump(groups, open('kmeans_groups.p', 'wb'))