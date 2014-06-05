from mrjob.job import MRJob 
import re
import operator
import sys
import math

class MRn_grams(MRJob):

    def pre_mapper(self, _, line):
        to_replace = {' ,' : ' ', ' .' : ' ', ' ?' : ' ', ' !' : ' ', '$ ' : ' ', ' \'s' : '', '`' : '', ' _' : '', '(' : '', ')' : '', '-' : ' ', '\"' : ''}
        for i, j in to_replace.iteritems():
            line = line.replace(i, j)
        line = line.replace(' \'', '').replace('\'', '').replace('_', '').replace('$', '').replace('.', '').replace(',', '').replace('?', '').replace('!', '')
        yield None, line.lower()

    def init_mapper(self):
        self.stop_words = ["a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fify", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves", 'unto', 'all', 'thou', 'thy', 'shall', 'shallnt', 'when', 'gutenberg', 'tm', 'said']
        temp = 'Southern Poverty Law Center Describe the activities of Morris Dees and the Southern Poverty Law Center'.lower()
        self.query = temp.split(' ')

    def mapper(self, _, line):
        #Yield each bi-gram
        line = line.replace('ca nt', 'cant').replace(' s ', '')
        words = line.split()
        for i in range(len(words)):
            if words[i] not in self.stop_words:
                score = 1
                if words[i] in self.query:
                    score += 2
                yield 'u{0}'.format(words[i]), score

        for i in range(len(words) - 1):
            self.increment_counter('n_gram_counters', 'bi-gram', 1)
            if words[i] not in self.stop_words and words[i+1] not in self.stop_words:
                score = 1
                in_query_so_far = 0
                if words[i] in self.query:
                    score += 2
                    in_query_so_far += 1
                if words[i+1] in self.query:
                    score += 2 + in_query_so_far
                yield 'b{0} {1}'.format(words[i], words[i + 1]), score #math.log1p(score)

        for i in range(len(words) - 2):
            if words[i] not in self.stop_words and words[i+1] not in self.stop_words and words[i+2] not in self.stop_words:
                score = 1
                in_query_so_far = 0
                if words[i] in self.query:
                    score += 2
                    in_query_so_far += 1
                if words[i+1] in self.query:
                    score += 2 + in_query_so_far
                    in_query_so_far += 1
                if words[i+2] in self.query:
                    score += 2 + in_query_so_far
                yield 't{0} {1} {2}'.format(words[i], words[i + 1], words[i + 2]), score

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield None, (math.pow(sum(counts), 1/1.5), word)

    def reducer_initial(self):
        self.uni_grams = {}
        self.bi_grams = {}
        self.tri_grams = {}
    def reducer_find_max_word(self, _, word_count_pairs):
        for i, j in word_count_pairs:
            if j[0] == 'u':
                self.uni_grams[j[1:]] = i
            if j[0] == 'b':
                self.bi_grams[j[1:]] = i
            if j[0] == 't':
                self.tri_grams[j[1:]] = i

    def reducer_fin(self):
        ##########----NOTE----: Sorting is for testing purposes only, it does not need to be done
        sorted_uni = (sorted(self.uni_grams.iteritems(), key=operator.itemgetter(1)))
        sorted_bi = (sorted(self.bi_grams.iteritems(), key=operator.itemgetter(1)))
        sorted_tri = (sorted(self.tri_grams.iteritems(), key=operator.itemgetter(1)))

        sorted_uni.reverse()
        sorted_bi.reverse()
        sorted_tri.reverse()

        for x in sorted_uni:
            yield x[0], float(x[1])/len(self.uni_grams) * 100

        for x in sorted_bi:
            yield x[0], float(x[1])/len(self.bi_grams) * 100

        for x in sorted_tri:
            yield x[0], float(x[1])/len(self.tri_grams) * 100

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
    MRn_grams.run()