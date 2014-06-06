from mrjob.job import MRJob 
import re
import operator
import cPickle as pickle
import sys

class MRBiGrams(MRJob):
    
    def mapper_initial(self):
        self.n_gram_prob = pickle.load(open('qidx.p', 'rb'))
        self.summary = []
        if len(self.n_gram_prob) == 0:
            sys.exit()
        self.query = 'Southern Poverty Law Center Describe the activities of Morris Dees and the Southern Poverty Law Center'.lower()

    def pre_mapper(self, _, line):
        temp_line = line
        to_replace = {' ,' : ' ', ' .' : ' ', ' ?' : ' ', ' !' : ' ', '$ ' : ' ', ' \'s' : '', '`' : '', ' _' : '', '(' : '', ')' : '', '-' : ' ', '\"' : ''}
        for i, j in to_replace.iteritems():
            temp_line = temp_line.replace(i, j)
        temp_line = temp_line.replace(' nt', 'nt').replace(' s ', '').replace(' \'', '').replace('\'', '').replace('_', '').replace('$', '').replace('.', '').replace(',', '').replace('?', '').replace('!', '')

        words = temp_line.lower().split()
        score = 0.0
        counter = 0
        for i in range(len(words)):
            word = '{0}'.format(words[i])
            value = self.n_gram_prob.get(word, 0)

            if word not in self.summary and value != 0:
                score += .5
            if word in self.query and value != 0:
                value *= 3

            score += value 

            if i >= len(words)-1:
                continue

            word = '{0} {1}'.format(words[i], words[i + 1])
            value = self.n_gram_prob.get(word, 0)

            if word not in self.summary and value != 0:
                score += 1
            if word in self.query and value != 0:
                value *= 5

            score += 1.5 * value

            if i >= len(words)-2:
                continue

            word = '{0} {1} {2}'.format(words[i], words[i+1], words[i+2])
            value = self.n_gram_prob.get(word, 0)

            if word not in self.summary and value != 0:
                score += 1.5
            if word in self.query and value != 0:
                value *= 7

            score += 2 * value

        #IMPORTANT: WE ARE PASSING THE EDITED LINE HERE
        yield None, (score, temp_line.lower())


    def reducer_initial(self):
        self.scores = []

    def reducer(self, _, word_score_pair):
        for word_score in word_score_pair:

            self.scores.append(word_score)

    def reducer_fin(self):
        sorted_scores = self.scores
        sorted_scores.sort()
        sorted_scores.reverse()
        top_10 = len(sorted_scores)/20
        sorted_scores = sorted_scores[:top_10]
        for score in sorted_scores:
            yield score[0], score[1]

    def steps(self):
        return [
            self.mr(mapper_init=self.mapper_initial,
            mapper=self.pre_mapper,#,
            reducer_init=self.reducer_initial,
            reducer=self.reducer,
            reducer_final=self.reducer_fin)
            ]

if __name__ == '__main__':
    MRBiGrams.run()