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
    "yourselves", 'unto', 'all', 'thou', 'thy', 'shall', 'shallnt', 'when', 'gutenberg', 'tm']
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
                score += .5 * value

        for i in range(len(words) - 1):
            word = '{0} {1}'.format(words[i], words[i + 1])
            value = self.filter(word)
            if value:
                score += 1.5 * value

        for i in range(len(words) - 2):
            word = '{0} {1} {2}'.format(words[i], words[i+1], words[i+2])
            value = self.filter(word)
            if value:
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