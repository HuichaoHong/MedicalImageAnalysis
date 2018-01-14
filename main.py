#-*- coding: utf-8 -*-
# Author: honghuichao
# Date:   2017.12.29
import caffe
import cv2
from pca import *
import numpy as np
from skimage.feature import hog
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
import os,sys

###main
def DCNN_feature(image,net,weight,status,blobs,):
	net=caffe.Net(net,weight,status,blobs)
	im=caffe.io.load_image(image)
	net.blobs['data']=im
	out=net.forward()
	return net.blobs[blobs].data[0]####decise the layer feature that we want to!!

def hog_feature(image):
	return hog(image)

def concat_feature(image):#fd feature from dcnn,fh denote feature using hand!!!
	fh=hog_feature(image)
	fd=DCNN_feature()
	np.reshape(fd,[1,-1]);# we reshape the size to [1,n],and n denote that 
	np.reshape(fh,[1,-1]);
	fd.extend(fh)
	return fd

def get_feature(path):
#path:txt file,ranged in row!!!!the first element denote the path of image,second is the labels 
	features=[]
	labels=[]
	file=open(path,'wt')
	lines=file.lines();
	feature=np.zeros([len(lines),])
	for line in lines:
		image=split(line,' ')[0]
		label=split(line,' ')[1]
		labels.append(label)
		features.append(concat_feature(image))
	return np.array(element),np.array(labels)


if __name__ == '__main__':
	#sample 
	features,labels=get_feature('demopath')
    svm_classifier=svm.SVC()
    svm_classifier.fit(features,labels)
    '''
    '''
    rf_classifier=RandomForestClassifier();
    rf_classifier.fit(features,labels)

	''''
	