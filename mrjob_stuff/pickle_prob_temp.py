import cPickle as pickle

with open('./ngrams_prob_uni.txt', 'r') as f:
    content_uni = f.readlines()

with open('./ngrams_prob.txt', 'r') as f:
    content_bi = f.readlines()

with open('./ngrams_prob_tri.txt', 'r') as f:
    content_tri = f.readlines()



query = {}

for sentence in content_uni:
    data = sentence.strip().split('\t')
    key = data[0].replace('\"', '')
    value = float(data[1])
    query[key] = value

for sentence in content_bi:
    data = sentence.strip().split('\t')
    key = data[0].replace('\"', '')
    value = float(data[1])
    query[key] = value

for sentence in content_tri:
    data = sentence.strip().split('\t')
    key = data[0].replace('\"', '')
    value = float(data[1])
    query[key] = value

pickle.dump(query, open('qidx.p', 'wb'))