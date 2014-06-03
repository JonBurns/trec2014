from mrjob.job import MRJob 
import re

WORD_RE = re.compile(r"[\w']+")

class MRMostUsedWord(MRJob):

    def init_get_words(self):
        self.words = {}

    def get_words(self, _, line):
        for word in WORD_RE.findall(line):
            word = word.lower()
            self.words.setdefault(word, 0)
            self.words[word] = self.words[word] + 1

    def final_get_words(self):
        for word, val in self.words.iteritems():
            yield word, val

    def sum_words(self, word, counts):
        yield word, sum(counts)

    def steps(self):
        return [self.mr(mapper_init=self.init_get_words, 
                mapper=self.get_words,
                mapper_final=self.final_get_words,
                combiner=self.sum_words,
                reducer = self.sum_words)]

if __name__ == '__main__':
    MRMostUsedWord.run()
