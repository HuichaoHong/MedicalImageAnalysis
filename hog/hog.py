#-*- coding: utf-8 -*-
# Author: honghuichao
# Date:   2017.12.29
from skimage.feature import *
from skimage.io import *
import matplotlib.pyplot as plt
import numpy as np
if __name__ == '__main__':
	I=imread('../sample/sample.jpg',as_grey=True)
	I=hog(I)
	plt.show(I)
	

