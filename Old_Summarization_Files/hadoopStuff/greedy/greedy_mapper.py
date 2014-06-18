#!/usr/bin/env python

import cPickle as pickle 
import sys
import math
import numpy

groups = pickle.load(open('kmeans_groupings.p', 'rb'))
sim_matrix = pickle.load(open('sim_matrix.p', 'rb'))
corpus_sums = pickle.load(open('corpus_sums.p', 'rb'))
rqj = pickle.load(open('rqj.p', 'rb'))
summary = pickle.load(open('summary.p', 'rb'))


def l1(s, sim_matrix, corpus_sums, alpha_numer = 12): #summary is collection of indicies
    n = sim_matrix.shape[0]
    alpha = float(alpha_numer)/float(n)
    score_sum = 0.0

    for i in range(n):
        score_sum += min([sum([sim_matrix[i, j] for j in s]), (alpha * corpus_sums[i])])
    return score_sum

def r1(s, corpus_sums, groups, rqj, beta = 0.5):
    k = len(groups)
    n = len(corpus_sums)

    result = 0.0
    for p in groups:
        result2 = 0.0
        for j in set(p).intersection(set(s)):
            result2 += ((beta/n) * corpus_sums[j] + ((1 - beta) * rqj[j]))

        result += math.sqrt(result2)

    return result

def reward(s, lambda_var = 6):
    l1_result = l1(s, sim_matrix, corpus_sums)
    r1_result = (lambda_var * r1(s, corpus_sums, groups, rqj))
    return l1_result + r1_result

scoret = reward(summary)

for line in sys.stdin:
#def greedy(elements, reward, cost, budget=250, r=0.0): #reward is a function
    data = line.split('\t')
    idx = int(data[0])
    if idx not in summary:
        temp = list(summary)
        temp.append(idx)
        gain = (reward(temp) - scoret)
        print '{0}\t{1}'.format(str(idx), str(gain))


