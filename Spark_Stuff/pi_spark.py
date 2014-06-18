"""SimpleApp.py"""
from pyspark import SparkContext
import random
import sys
import math
sc = SparkContext("local", "Simple App")

NUM_SAMPLES = 10000000

def sample(p):
    x, y = random.random(), random.random()
    return 1 if x*x + y*y < 1 else 0

count = sc.parallelize(xrange(0, NUM_SAMPLES)).map(sample).reduce(lambda a, b: a + b)

estimation = (4.0 * count / NUM_SAMPLES)
perc_diff = (estimation - math.pi)/((math.pi + estimation)/2) * 100

print "Pi estimation difference %f" % perc_diff