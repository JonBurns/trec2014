import re
import sys
from itertools import groupby

with open('ROUGE/ROUGE-EVAL/ROUGE.out') as f:
    content = f.readlines()

scores = []

for lines in content:
    if re.match(".*(ROUGE-2 Average_F:)+.*", lines):
        scores.append(re.split("(ROUGE-2 Average_F:)+", lines))

scores = [[score[2][:8].strip(), score[0].strip()] for score in scores]

scores.sort()
scores.reverse()


with open('./results.txt', 'w') as f:
    previous = float(scores[0][0])
    f.write("{0:<50}{1:^28}{2:<8}\n\n".format("TEST_NAME", "ROUGE-2 Average_F:", "Difference"))
    for score in scores:
        if score[1] == 'baseline-ss':
            f.write('------------------------------------------------------------------------------------------\n')
        if score[1] == sys.argv[1]:
            f.write('\n')
            f.write('>{0:<49}{1:^30}{2:<8}\n'.format(score[1], score[0], previous - float(score[0])))
            f.write('\n')
        else:    
            f.write('{0:<50}{1:^30}{2:<8}\n'.format(score[1], score[0], previous - float(score[0])))