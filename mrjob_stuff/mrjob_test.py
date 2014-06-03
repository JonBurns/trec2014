from mrjob.job import MRJob 
import re
import operator

class MRBiGrams(MRJob):

    def pre_mapper(self, _, line):
        to_replace = {' ,' : ' ', ' .' : ' ', ' ?' : ' ', ' !' : ' ', '$ ' : ' ', ' \'' : '', '`' : '', ' _' : '', '(' : '', ')' : '', '-' : ' ', '\"' : ''}
        for i, j in to_replace.iteritems():
            line = line.replace(i, j)
        line = line.replace('\'', '').replace('_', '').replace('$', '').replace('.', '').replace(',', '').replace('?', '').replace('!', '')
        yield None, line.lower()

    def mapper(self, _, line):
        #Yield each bi-gram
        #line = pre_mapper(line)
        words = line.split()
        for i in range(len(words) - 2):
            self.increment_counter('n_gram_counters', 'bi-gram', 1)
            yield (words[i], words[i + 1], words[i + 2]), 1
        #for i in range(len(words) - 1):
            #self.increment_counter('n_gram_counters', 'bi-gram', 1)
            #yield (words[i], words[i + 1]), 1
            

        #for i in range(len(words)):
            #yield words[i], 1

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield None, (sum(counts), word)

    def reducer_initial(self):
        self.n_grams = {}

    def reducer_find_max_word(self, _, word_count_pairs):
        for i, j in word_count_pairs:
            string_temp = j[0] + ' ' + j[1] + ' ' + j[2]
            self.n_grams[string_temp] = i

    def reducer_fin(self):
        sorted_x = (sorted(self.n_grams.iteritems(), key=operator.itemgetter(1)))
        sorted_x.reverse()
        for x in sorted_x:
            yield x[0], float(x[1])/len(self.n_grams) * 100
        #for i,j in self.n_grams.iteritems():
            #yield i, float(j)/len(self.n_grams) * 100

    def steps(self):
        return [
            self.mr(mapper=self.pre_mapper),
            self.mr(mapper=self.mapper, 
                combiner=self.combiner,
                reducer=self.reducer),
            self.mr(reducer_init=self.reducer_initial,
                reducer=self.reducer_find_max_word,
               reducer_final=self.reducer_fin)
            ]

if __name__ == '__main__':
    MRBiGrams.run()