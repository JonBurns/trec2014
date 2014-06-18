"""SimpleApp.py"""
from pyspark import SparkContext

#Function needs to return a sequence for flatmap
def n_grams(line):
    sequence = []
    words = line.strip().split(' ')
    for i in range(len(words)):

        ##UNIGRAMS
        sequence.append('u{0}'.format(words[i]))
        
        ##BIGRAMS
        if i >= len(words)-1:
            continue

        sequence.append('b{0} {1}'.format(words[i], words[i + 1]))

        ##TRIGRAMS
        if i >= len(words)-2:
            continue

        sequence.append('t{0} {1} {2}'.format(words[i], words[i + 1], words[i + 2]))
    return sequence

logFile = "ROUGE/DUC-2007/docs/D0701A/"  # Should be some file on your system
sc = SparkContext("local", "Simple App")
logData = sc.textFile(logFile).cache()

grams = logData.flatMap(n_grams).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).collect()

unigrams = {}
bigrams = {}
trigrams = {}

uni_count = 0
bi_count = 0
tri_count = 0

for gram in grams:

    if gram[0][0] == 'u':
        unigrams[gram[0][1:]] = unigrams.get(gram[0][1:], 0) + gram[1]
        uni_count += gram[1]

    if gram[0][0] == 'b':
        bigrams[gram[0][1:]] = bigrams.get(gram[0][1:], 0) + gram[1]
        bi_count += gram[1]

    if gram[0][0] == 't':
        trigrams[gram[0][1:]] = trigrams.get(gram[0][1:], 0) + gram[1]
        tri_count += gram[1]

for i,j in unigrams.iteritems():
    unigrams[i] = float(j)/uni_count

for i,j in bigrams.iteritems():
    bigrams[i] = float(j)/bi_count

for i,j in trigrams.iteritems():
    trigrams[i] = float(j)/tri_count

#numBs = logData.filter(lambda s: 'b' in s).count()

for i,j in unigrams.iteritems():
    print '{0}\t\t{1}'.format(i, j)

print '-----------------------------------------------------------'

for i,j in bigrams.iteritems():
    print '{0}\t\t{1}'.format(i, j)

print '-----------------------------------------------------------'

for i,j in trigrams.iteritems():
    print '{0}\t\t{1}'.format(i, j)



