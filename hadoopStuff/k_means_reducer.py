#!/usr/bin/env python
import sys
import cPickle as pickle 

old_key = None
list_of_idxs = []
k_means = []
vectorized_sentences = pickle.load(open('vectorized_sentences.p', 'rb'))

for line in sys.stdin:
    data = line.split('\t')
    new_key = int(data[0])
    idx = int(data[1])

    if old_key and old_key and old_key != new_key:
    #do stuff for changing keys
        print '{0}\t{1}'.format(old_key, repr(list_of_idxs))
        avrg_vector = []
        #Stuff for the new k-means
        for i in range(len(vectorized_sentences[0])):
            sum = 0.0
            for index in list_of_idxs:
                #print '{0}\t{1}'.format(i, len(vectorized_sentences))
                sum += vectorized_sentences[index][i]
            avrg_vector.append(sum/len(list_of_idxs))

        k_means.append(avrg_vector)
        list_of_idxs = []
    
    list_of_idxs.append(idx)
    old_key = new_key



pickle.dump(k_means, open('kmeans_groups.p', 'wb'))