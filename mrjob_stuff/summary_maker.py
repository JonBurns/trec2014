import sys

try:
    with open('summary.txt') as f:
        summary = f.readlines()
except IOError:
    print 'summary.txt does not exist, creating empty'
    summary = []

try:
    with open(sys.argv[1]) as f:
        content = f.readlines()
except IOError:
    print '{0} does not exist'.format(sys.argv[1])

new_sentence = content[0].split('\t')[1]

summary.append(new_sentence)

with open('summary.txt', 'w') as f:
    for sentence in summary:
        f.write(sentence.replace('"', ''))

summary_len = len([word for word in sentence.split(' ') for sentence in summary])
print "{0}".format(summary_len)