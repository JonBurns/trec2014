import sys
import subprocess
import os


with open('/Users/jonathanburns/Development/SummerResearch/trec2014/Old_Summarization_Files/ROUGE/DUC-2007/duc2007_topics.txt') as f:
    contents = f.readlines()

contents = [content.strip() for content in contents]

data = []

for i in range(0, len(contents) - 1, 3):
    data.append((contents[i], contents[i+2])) 

###MAKE CALLS###

test_name = 'Spark_test_4_with_tri_40_bi_30_uni_60'

subprocess.call('touch summary.txt', shell = True)

for part in data:
    ##Get Name of current subdirectory
    subdir = part[0]
    query = part[1]

    ##Set up query file

    ##Here is where the subdirectory is inserted
    print ('\n\nSCRIPT CALL>> spark-submit Spark_Stuff/Spark_Summarization_Basic.py ' + subdir + ' ' + '\"' + query + '\"' + '\n')

    subprocess.call('spark-submit Spark_Stuff/Spark_Summarization_Basic.py ' + subdir + ' ' + '\"' + query + '\"', shell = True)

    subprocess.call('mv summary.txt Old_Summarization_Files/ROUGE/DUC-2007/SYSTEM/'+ subdir[:-1] +'/'+ subdir[:-1] + '.' + test_name +'.system', shell = True)

    subprocess.call('touch summary.txt', shell = True)

subprocess.call('./Old_Summarization_Files/prepare_results.sh ' + test_name, shell = True)
subprocess.call('python Old_Summarization_Files/getResults.py ' + test_name, shell = True)
