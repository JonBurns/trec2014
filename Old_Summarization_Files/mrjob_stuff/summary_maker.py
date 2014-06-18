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

old_len = len([word for sentence in summary for word in sentence.split(' ')])

for i in range(len(content)):
    new_sentence = content[i].split('\t')[1]
    new_sentence_len = len(new_sentence.split(' '))
    
    if old_len + new_sentence_len <= 250:
        summary.append(new_sentence)
        break

with open('summary.txt', 'w') as f:
    for sentence in summary:
        f.write(sentence.replace('"', ''))

summary_len = len([word for sentence in summary for word in sentence.split(' ')])
print "{0}".format(summary_len)