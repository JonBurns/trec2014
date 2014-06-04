from mrjob.job import MRJob 
import re
import operator
import cPickle as pickle
import sys

class MRBiGrams(MRJob):
    
    def filter(self, ngram):
        try:
            value = self.query[ngram] 
            return value
        except KeyError:
            return False 

    def mapper_initial(self):
        self.query = pickle.load(open('qidx.p', 'rb'))
        if len(self.query) == 0:
            sys.exit()
        #self.query = {'of the' : 1, 'sentence is' : 1, 'is fake' : 1}

    def pre_mapper(self, _, line):
        temp_line = line
        to_replace = {' ,' : ' ', ' .' : ' ', ' ?' : ' ', ' !' : ' ', '$ ' : ' ', ' \'s' : '', '`' : '', ' _' : '', '(' : '', ')' : '', '-' : ' ', '\"' : ''}
        for i, j in to_replace.iteritems():
            temp_line = temp_line.replace(i, j)
        temp_line = temp_line.replace(' nt', 'nt').replace(' s ', '').replace(' \'', '').replace('\'', '').replace('_', '').replace('$', '').replace('.', '').replace(',', '').replace('?', '').replace('!', '')

        words = temp_line.lower().split()
        score = 0.0
        for i in range(len(words)):
            word = '{0}'.format(words[i])
            value = self.filter(word)
            if value:
                score += 0.5 * value

        for i in range(len(words) - 1):
            word = '{0} {1}'.format(words[i], words[i + 1])
            value = self.filter(word)
            if value:
                score += 2 * value

        # for i in range(len(words) - 2):
        #     word = '{0} {1} {2}'.format(words[i], words[i+1], words[i+2])
        #     value = self.filter(word)
        #     if value:
        #         score += 1.5 * value

        if score >= 50:
            yield score, line.lower()

    # def mapper(self, _, line):
    #     #Yield each bi-gram
    #     #line = pre_mapper(line)
    #     words = line.split()
    #     for i in range(len(words) - 2):
    #         self.increment_counter('n_gram_counters', 'bi-gram', 1)
    #         yield (words[i], words[i + 1], words[i + 2]), 1
        #for i in range(len(words) - 1):
            #self.increment_counter('n_gram_counters', 'bi-gram', 1)
            #yield (words[i], words[i + 1]), 1
            

        #for i in range(len(words)):
            #yield words[i], 1

    # def combiner(self, word, counts):
    #     yield (word, sum(counts))

    # def reducer(self, word, counts):
    #     yield None, (sum(counts), word)

    # def reducer_initial(self):
    #     self.n_grams = {}

    # def reducer_find_max_word(self, _, word_count_pairs):
    #     for i, j in word_count_pairs:
    #         string_temp = j[0] + ' ' + j[1] + ' ' + j[2]
    #         self.n_grams[string_temp] = i

    # def reducer_fin(self):
    #     sorted_x = (sorted(self.n_grams.iteritems(), key=operator.itemgetter(1)))
    #     sorted_x.reverse()
    #     for x in sorted_x:
    #         yield x[0], float(x[1])/len(self.n_grams) * 100
    #     #for i,j in self.n_grams.iteritems():
    #         #yield i, float(j)/len(self.n_grams) * 100

    def steps(self):
        return [
            self.mr(mapper_init=self.mapper_initial,
            mapper=self.pre_mapper)#,
            #self.mr(mapper=self.mapper, 
                #combiner=self.combiner,
                #reducer=self.reducer),
            #self.mr(reducer_init=self.reducer_initial,
                #reducer=self.reducer_find_max_word,
               #reducer_final=self.reducer_fin)
            ]

if __name__ == '__main__':
    MRBiGrams.run()