"""Spark_Summarization_Basic.py"""
from pyspark import SparkContext
from Stop_words import ENGLISH_STOP_WORDS
import numpy as np
import sys

from tokenizers import get_synset
    

def query_filter(line, query):
    count = 0
    for word in query:
        if word not in ENGLISH_STOP_WORDS and word in line.lower():
            count += 1

    if count > 0:
        return True
    else:
        return False

def filter_zero_vectors(np_vector):
    summation = np.sum(np_vector)
    if summation < 1:
        return False
    else:
        return True

def query_fancier(alist):
    new_query = []
    for word in alist:
        new_query.append(word)
        for syn in get_synset(word):
            new_query.append(syn.lower())
    return new_query

#Function needs to return a sequence for flatmap
def uni_grams(line):
    line = line.replace(" n't", "n't").replace(' \' ', '')
    sequence = []
    words = line.strip().split(' ')
    for i in range(len(words)):

        uni_gram = '{0}'.format(words[i]).lower()
        if uni_gram not in ENGLISH_STOP_WORDS:
            sequence.append(uni_gram)

    return sequence

#Function needs to return a sequence for flatmap
def bi_grams(line):
    line = line.replace(" n't", "n't").replace(' \' ', '')
    sequence = []
    words = line.strip().split(' ')
    for i in range(len(words) - 1):
        
        first_bi_gram = '{0}'.format(words[i]).lower()
        second_bi_gram = '{0}'.format(words[i + 1]).lower()
        if first_bi_gram not in ENGLISH_STOP_WORDS and second_bi_gram not in ENGLISH_STOP_WORDS:
            sequence.append('{0} {1}'.format(first_bi_gram, second_bi_gram))

    return sequence

#Function needs to return a sequence for flatmap
def tri_grams(line):
    line = line.replace(" n't", "n't").replace(' \' ', '')
    sequence = []
    words = line.strip().split(' ')
    for i in range(len(words) - 2):
        
        first_tri_gram = '{0}'.format(words[i]).lower()
        second_tri_gram = '{0}'.format(words[i + 1]).lower()
        third_tri_gram = '{0}'.format(words[i + 2]).lower()
        if first_tri_gram not in ENGLISH_STOP_WORDS and second_tri_gram not in ENGLISH_STOP_WORDS and third_tri_gram not in ENGLISH_STOP_WORDS:
            sequence.append('{0} {1} {2}'.format(first_tri_gram, second_tri_gram, third_tri_gram))

    return sequence

#Function needs to return a sequence for flatmap
def quad_grams(line):
    line = line.replace(" n't", "n't").replace(' \' ', '')
    sequence = []
    words = line.strip().split(' ')
    for i in range(len(words) - 3):
        
        first_quad_gram = '{0}'.format(words[i]).lower()
        second_quad_gram = '{0}'.format(words[i + 1]).lower()
        third_quad_gram = '{0}'.format(words[i + 2]).lower()
        fourth_quad_gram = '{0}'.format(words[i + 3]).lower()
        if first_quad_gram not in ENGLISH_STOP_WORDS and second_quad_gram not in ENGLISH_STOP_WORDS and third_quad_gram not in ENGLISH_STOP_WORDS and fourth_quad_gram not in ENGLISH_STOP_WORDS:
            sequence.append('{0} {1} {2} {3}'.format(first_quad_gram, second_quad_gram, third_quad_gram, fourth_quad_gram))

    return sequence


def vector_map(line, n_gram_model):
    new_vect = np.zeros(len(n_gram_model), np.int)
    fixed_line = line.replace(" n't", "n't").replace(' \' ', '').lower()

    for i in range(len(n_gram_model)):
        if n_gram_model[i][0] in fixed_line:
            new_vect[i] = 1

    return line, new_vect

def vector_or_adder(vector_one, vector_two):
    new_vect = np.zeros(len(vector_one), np.int)

    for i in range(len(vector_one)):
        new_vect[i] = vector_one[i] or vector_two[i]

    return new_vect

def summary_mapper(sentence_vector, summary_vector):
    addition_vector = vector_or_adder(sentence_vector[1], summary_vector[1])
    score = np.sum(addition_vector) - np.sum(summary_vector[1])
    return sentence_vector[0], addition_vector, score




if len(sys.argv) < 3:
    logFile = "Old_Summarization_Files/ROUGE/DUC-2007/docs/D0701A/"  # Should be some file on your system
    query = bi_grams('Describe the activities of Morris Dees and the Southern Poverty Law Center. '.lower())
else:
    logFile = 'Old_Summarization_Files/ROUGE/DUC-2007/docs/' + sys.argv[1] + '/'
    query = uni_grams(sys.argv[2].lower())


sc = SparkContext("local", "Summarizer App", pyFiles=['Spark_Stuff/Spark_Summarization_Basic.py', 'Spark_Stuff/Stop_words.py', 'Spark_Stuff/tokenizers.py'])
logData = sc.textFile(logFile).cache()

#query = query_fancier(query)

#Create Models
unigrams = logData.filter(lambda x: query_filter(x, query)).flatMap(uni_grams).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
bigrams = logData.filter(lambda x: query_filter(x, query)).flatMap(bi_grams).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
trigrams = logData.filter(lambda x: query_filter(x, query)).flatMap(tri_grams).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
quadgrams = logData.filter(lambda x: query_filter(x, query)).flatMap(quad_grams).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

#Get top 50 
set_of_uni = np.array(unigrams.takeOrdered(50, key=lambda x: -x[1]))
set_of_bi = np.array(bigrams.takeOrdered(30, key=lambda x: -x[1]))
set_of_tri = np.array(trigrams.takeOrdered(40, key=lambda x: -x[1]))
set_of_quad = np.array(trigrams.takeOrdered(5, key=lambda x: -x[1]))

model = np.concatenate((set_of_uni, set_of_bi, set_of_tri, set_of_quad))

#Blank Summary
summary = "", np.zeros(len(model), np.int)

used = []
count = 0
#Future: Make is an np array?
vect_sent_tuple = logData.filter(lambda x: query_filter(x, query)).map(lambda x: vector_map(x, model)).reduceByKey(lambda a, b: a).filter(lambda x: filter_zero_vectors(x[1])).cache()

while len(summary[0].split(' ')) < 250:
    summary_set = vect_sent_tuple.map(lambda x: summary_mapper(x, summary)).takeOrdered(1, lambda x: -x[2])
    new_summary = (summary[0] + summary_set[0][0] + '\n', summary_set[0][1])
    score = summary_set[0][2]

    if score == 0:
        break

    summary = new_summary
    count += 1

with open('summary.txt', 'w') as f:
    f.write(summary[0].replace(' , ', ', ').replace(' .', '.').replace(' n\'t', 'n\'t').replace(' \'s', '\'s'))




    # for item in range(len(summary_set[0][1])):
    #     if summary_set[0][1][item] == 1 and item not in used:
    #         print '{0}\t{1}'.format(item, model[item])
    #         used.append(item)

