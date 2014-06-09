import sys
import subprocess
import os


with open('/Users/jonathanburns/Development/SummerResearch/trec2014/ROUGE/DUC-2007/duc2007_topics.txt') as f:
    contents = f.readlines()

contents = [content.strip() for content in contents]

data = []

for i in range(0, len(contents) - 1, 3):
    data.append((contents[i], contents[i+2])) 

###MAKE CALLS###

test_name = 'hadoop_test_1'

subprocess.call('touch summary.txt', shell = True)

for part in data:
    ##Get Name of current subdirectory
    subdir = part[0]
    query = part[1]

    ##Set up query file
    with open('query.txt', 'w') as f:
        f.write(query)

    ##Make Ngrams
    ##Here is where the subdirectory is inserted
    print ('\n\nSCRIPT CALL>>python MRngrams.py -r hadoop hdfs:///user/jonathanburns/docs/' + subdir + ' > n_gram_prob.txt\n')

    subprocess.call('python MRngrams.py -r hadoop hdfs:///user/jonathanburns/docs/' + subdir + ' > n_gram_prob.txt', shell = True)

    ##Pickle ngrams
    print ('\n\nSCRIPT CALL>>python pickle_prob_temp.py n_gram_prob.txt\n')

    subprocess.call('python pickle_prob_temp.py n_gram_prob.txt', shell = True)

    ##Create Scoring
    print ('\n\nSCRIPT CALL>>python MRfilter.py -r hadoop hdfs:///user/jonathanburns/docs/' + subdir + ' --file qidx.p --file summary.txt --file query.txt > summary_temp.txt\n')

    subprocess.call('python MRfilter.py -r hadoop hdfs:///user/jonathanburns/docs/' + subdir + ' --file qidx.p --file summary.txt --file query.txt > summary_temp.txt', shell = True)

    ##Add to summary
    print ('\n\nSCRIPT CALL>>python summary_maker.py summary_temp.txt\n')

    length = subprocess.check_output('python summary_maker.py summary_temp.txt', shell = True)

    ##Check length and repeat if necessary 
    while int(length) < 250:
        print 'Loop of summary creation. Word Count so far: {0}'.format(length)
        print ('\n\nSCRIPT CALL>>python MRfilter.py -r hadoop hdfs:///user/jonathanburns/docs/' + subdir + ' --file qidx.p --file summary.txt --file query.txt > summary_temp.txt\n')
        subprocess.call('python MRfilter.py -r hadoop hdfs:///user/jonathanburns/docs/' + subdir + ' --file qidx.p --file summary.txt --file query.txt > summary_temp.txt', shell = True)

        print ('\n\nSCRIPT CALL>>python summary_maker.py summary_temp.txt\n')
        length = subprocess.check_output('python summary_maker.py summary_temp.txt', shell = True)

    subprocess.call('mv summary.txt ../ROUGE/DUC-2007/SYSTEM/'+ subdir[:-1] +'/'+ test_name +'.system', shell = True)

    subprocess.call('touch summary.txt', shell = True)



