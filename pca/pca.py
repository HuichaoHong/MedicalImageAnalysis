#-*- coding: utf-8 -*-
# Author: honghuichao
# Date:   2017.12.29
import numpy as np
from matplotlib import pyplot as plt
from scipy import io as spio
from sklearn.decomposition import pca


def PCA(X):
    m = X.shape[0]
    X_copy = X.copy()
    X_norm,mu,sigma = featureNormalize(X_copy)    # normalized the data
    Sigma = np.dot(np.transpose(X_norm),X_norm)/m  # Sigma
    U,S,V = np.linalg.svd(Sigma)       # SVD
    return X_norm,U

def featureNormalize(X):
    n = X.shape[1]
    mu = np.zeros((1,n));
    sigma = np.zeros((1,n))
    
    mu = np.mean(X,axis=0)   # 
    sigma = np.std(X,axis=0)
    for i in range(n):
        X[:,i] = (X[:,i]-mu[i])/sigma[i]
    return X,mu,sigma

def projectData(X_norm,U,K):
    Z = np.zeros((X_norm.shape[0],K))
    U_reduce = U[:,0:K]        
    Z = np.dot(X_norm,U_reduce) 
    return Z
''''
if __name__ == "__main__":
	X=[]
	X_norm,U=PCA(X)
	K = 10 
    Z = projectData(X_norm,U,K)  
''''
