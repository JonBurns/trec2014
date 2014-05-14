#!/Users/jonathanburns/anaconda/bin/python

import subprocess
import os

path = 'ROUGE/DUC-2007/docs/'
path2 = 'ROUGE/DUC-2007/'

lines = os.listdir(path)[1:]

alpha_values = [10]
r_values = [0, 1]
beta_values = [0.3, 0.5]
lambda_values = [1, 6]

total_computations = len(alpha_values) * len(beta_values) * len(lambda_values) * len(r_values)

i = 0
for lambda_val in lambda_values:
    for beta in beta_values:
        for alpha in alpha_values:
            for r in r_values:
                print "{0}% complete".format((float(i)/float(total_computations)) * 100)
                testName = '.lambda-{0}-beta-{1}-alpha-{2}'.format(str(lambda_val), str(beta), str(alpha))
                for cluster in lines:

                    print 'python Summarizer.py ' + cluster + ' ' + str(alpha) + ' ' + str(beta) + ' ' + str(lambda_val) + ' ' + str(r)

                    output = subprocess.check_output('python Summarizer.py ' + cluster + ' ' + str(alpha) + ' ' + str(beta) + ' ' + str(lambda_val) + ' ' + str(r), shell = True)
                    with open(path2 + 'SYSTEM/' + cluster[:-1] + '/' + cluster[:-1] + testName + '.system', 'w') as f:
                        f.write(output)
                i += 1

subprocess.call('prepare_results.sh ' + "placeHolder" , shell = True)