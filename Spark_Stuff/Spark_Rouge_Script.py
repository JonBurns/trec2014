import sys
import subprocess
import os

if len(sys.argv) < 4:
    uni = 1
    bi = 1
    tri = 1
else:
    uni = sys.argv[2]
    bi = sys.argv[3]
    tri = sys.argv[4]


with open('/Users/jonathanburns/Development/SummerResearch/trec2014/Old_Summarization_Files/ROUGE/DUC-2007/duc2007_topics.txt') as f:
    contents = f.readlines()

contents = [content.strip() for content in contents]

data = []

for i in range(0, len(contents) - 1, 3):
    data.append((contents[i], contents[i+2])) 

###MAKE CALLS###

test_name = 'Spark_' + sys.argv[1]#Index_Pos_Reward_Top_15_Reward'

subprocess.call('touch summary.txt', shell = True)

for part in data:
    ##Get Name of current subdirectory
    subdir = part[0]
    query = part[1].replace('\"', '')

    ##Set up query file

    ##Here is where the subdirectory is inserted
    print ('\n\nSCRIPT CALL>> spark-submit Spark_Stuff/Spark_Summarization_Basic.py ' + subdir + ' ' + '\"' + query + '\" ' + repr(uni) + ' ' + repr(bi) + ' ' + repr(tri) + '\n')

    subprocess.call('spark-submit Spark_Stuff/Spark_Summarization_Basic.py ' + subdir + ' ' + '\"' + query + '\" ' + repr(uni) + ' ' + repr(bi) + ' ' + repr(tri), shell = True)

    subprocess.call('mv summary.txt Old_Summarization_Files/ROUGE/DUC-2007/SYSTEM/'+ subdir[:-1] +'/'+ subdir[:-1] + '.' + test_name +'.system', shell = True)

    subprocess.call('touch summary.txt', shell = True)

#subprocess.call('./Old_Summarization_Files/prepare_results.sh ' + test_name, shell = True)
#subprocess.call('python Old_Summarization_Files/getResults.py ' + test_name, shell = True)
