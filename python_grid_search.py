#!/Users/jonathanburns/anaconda/bin/python

import subprocess
import os

path = 'ROUGE/DUC-2007/docs/'
path2 = 'ROUGE/DUC-2007/'

#path2 + 'SYSTEM/' + cluster1 + '/' + cluster1 + '.' + sys.argv[1] + '.system

lines = os.listdir(path)[1:]

#alpha_values = [1, 5, 10, 20]
#beta_values = [0.1, 0.3, 0.5, 0.7, 0.9]
#lambda_values = [1, 3, 6, 9, 12]

alpha_values = [10]
beta_values = [0.3, 0.5]
lambda_values = [1, 6]

total_computations = len(alpha_values) * len(beta_values) * len(lambda_values)

i = 0
for lambda_val in lambda_values:
    for beta in beta_values:
        for alpha in alpha_values:
            print "{0}% complete".format((i/total_computations) * 100)
            testName = '.lambda-{0}-beta-{1}-alpha-{2}'.format(str(lambda_val), str(beta), str(alpha))
            for cluster in lines:
                output = subprocess.check_output('python Summarizer.py ' + cluster + ' 10 0.5 6', shell = True)
                with open(path2 + 'SYSTEM/' + cluster[:-1] + '/' + cluster[:-1] + testName + '.system', 'w') as f:
                    f.write(output)
            i += 1

subprocess.call('python prepare_results.sh ' + "placeHolder" , shell = True)