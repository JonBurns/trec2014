import sys
import subprocess
import os


unis = [.037, .039]
bis = [.035, .037, .039]
tris = [.115, .117, .119]

total = len(unis) + len(bis) + len(tris)
        
for uni in unis:
    for bi in bis:
        for tri in tris:
            test = 'U_{0}_B_{1}_T_{2}'.format(uni, bi, tri)
            subprocess.call('python Spark_Stuff/Spark_Rouge_Script.py ' + test + ' ' + repr(uni) + ' ' + repr(bi) + ' ' + repr(tri), shell = True)

subprocess.call('./Old_Summarization_Files/prepare_results.sh ' + 'temp', shell = True)
subprocess.call('python Old_Summarization_Files/getResults.py ' + 'temp', shell = True)