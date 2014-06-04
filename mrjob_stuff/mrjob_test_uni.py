from mrjob.job import MRJob 
import re
import operator
import sys

class MRBiGrams(MRJob):

    def pre_mapper(self, _, line):
        to_replace = {' ,' : ' ', ' .' : ' ', ' ?' : ' ', ' !' : ' ', '$ ' : ' ', ' \'s' : '', '`' : '', ' _' : '', '(' : '', ')' : '', '-' : ' ', '\"' : ''}
        for i, j in to_replace.iteritems():
            line = line.replace(i, j)
        line = line.replace(' \'', '').replace('\'', '').replace('_', '').replace('$', '').replace('.', '').replace(',', '').replace('?', '').replace('!', '')
        # if 'ca nt' in line:
        #     sys.exit()
        yield None, line.lower()

    def init_mapper(self):
        self.stop_words = [
    'a', 'about', 'also', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'be',
    'but', 'by', 'can', 'com', 'did', 'do', 'does', 'for', 'from', 'had',
    'has', 'have', 'he', "he'd", "he'll", "he's", 'her', 'here', 'hers',
    'him', 'his', 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is',
    'it', "it's", 'its', 'just', 'me', 'mine', 'my', 'of', 'on', 'or', 'org',
    'our', 'ours', 'she', "she'd", "she'll", "she's", 'some', 'than', 'that',
    'the', 'their', 'them', 'then', 'there', 'these', 'they', "they'd",
    "they'll", "they're", 'this', 'those', 'to', 'us', 'was', 'we', "we'd",
    "we'll", "we're", 'were', 'what', 'where', 'which', 'who', 'will', 'with',
    'would', 'you', 'your', 'yours']
        temp = 'Southern Poverty Law Center Describe the activities of Morris Dees and the Southern Poverty Law Center'.lower()
        self.query = temp.split(' ')

    def mapper(self, _, line):
        #Yield each bi-gram
        #line = pre_mapper(line)
        line = line.replace('ca nt', 'cant').replace(' s ', '')
        words = line.split()
        # for i in range(len(words) - 2):
        #     self.increment_counter('n_gram_counters', 'bi-gram', 1)
        #     yield (words[i], words[i + 1], words[i + 2]), 1
        for i in range(len(words)):
            if words[i] not in self.stop_words:
                score = 1
                if words[i] in self.query:
                    score += 2
                yield '{0}'.format(words[i]), score
            

        # for i in range(len(words)):
        #     yield words[i], 1

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield None, (sum(counts), word)

    def reducer_initial(self):
        self.n_grams = {}

    def reducer_find_max_word(self, _, word_count_pairs):
        for i, j in word_count_pairs:
            self.n_grams[j] = i

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
            self.mr(mapper_init=self.init_mapper,
                mapper=self.mapper, 
                combiner=self.combiner,
                reducer=self.reducer),
            self.mr(reducer_init=self.reducer_initial,
                reducer=self.reducer_find_max_word,
               reducer_final=self.reducer_fin)
            ]

if __name__ == '__main__':
    MRBiGrams.run()