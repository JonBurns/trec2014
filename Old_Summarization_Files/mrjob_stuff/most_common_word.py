from mrjob.job import MRJob 
import re

WORD_RE = re.compile(r"[\w']+")

class MRMostUsedWord(MRJob):

    def mapper_get_words(self, _, line):
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def combine_count_words(self, word, counts):
        yield (word, sum(counts))

    def reducer_count_words(self, word, counts):
        yield None, (sum(counts), word)

    def reducer_find_max_word(self, _, word_count_pairs):
        yield max(word_count_pairs)

    def steps(self):
        return [
            self.mr(mapper=self.mapper_get_words, 
                combiner=self.combine_count_words,
                reducer=self.reducer_count_words),
            self.mr(reducer=self.reducer_find_max_word)
            ]

if __name__ == '__main__':
    MRMostUsedWord.run()
