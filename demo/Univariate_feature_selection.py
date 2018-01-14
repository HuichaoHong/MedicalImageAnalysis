#Data:  2017-12.30
#ref:   https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.pearsonr.html
import numpy as np
from scipy.stats import pearsonr
np.random.seed(0)
size = 300
x = np.random.normal(0, 1, size)
print "Lower noise", pearsonr(x, x + np.random.normal(0, 1, size))
print "Higher noise", pearsonr(x, x + np.random.normal(0, 10, size))
'''



'''
from minepy import MINE
m = MINE()
x = np.random.uniform(-1, 1, 10000)
print m.compute_score(x, x**2)
print m.mic()