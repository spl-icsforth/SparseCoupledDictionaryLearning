"""SPARSE COUPLED DICTIONARY LEARNING

Sumplementary Methods for the execution of intermediate matrices (Lagrange multiplier matrices, sparse coding matrices)

:Author: Nancy Panousopoulou <apanouso@ics.forth.gr>

:Reference document: Konstantina  Fotiadou, Grigorios Tsagkatakis, Panagiotos Tsakalides `` Linear Inverse Problems with Sparsity Constraints'', DEDALE DELIVERABLE 3.1, 2016. 

:Date: December 2017

"""

import numpy as np

from numpy.linalg import inv
#from numpy.linalg import solve

from scipy.linalg import solve 


def updateY(previousY, c, op1, op2, maxbeta=1e+6, beta=0.01):
    """Update Lagrange multiplier matrix (Equation (19)). 
	
	Input Arguments
    ----------
    previousY : np.array
        The previous value of the Lagrange multiplier matrix
    c: double
		Step size parameter for the augmentend Lagrangian function
	op1: np.array
		First operand matrix (thresholding values)
	op2 : np.array
		Second operand matrix (sparse coding coefficients)
	maxbeta, beta: double
		Auxiliary parameters for updating Lagrange multiplier matrices.
	
	
	"""   
    return  previousY + min(maxbeta, beta*c)*(op1-op2)
        
    
def updThr(inputmat, lam=0.1):
	
    """
    Update thresholding matrices (Equations (13)-(14)). 
	
    Input Arguments
    ----------
    inputmat : np.array
        The input matrix for thresholding
    lam: double
		The thresholding value
		
	
	"""
        
    th = lam/2.
    
    ttt = np.random.random(inputmat.shape)
    #ttt = a - th [a > th]
    
    
    for bb in range(inputmat.shape[0]):
        for aa in range(inputmat.shape[1]):
        #print('*************')
        #print(aa)
        #print('*************')
            if inputmat[bb,aa]>th:
                ttt[bb,aa] = inputmat[bb,aa]-th
            elif abs(inputmat[bb,aa]) <= th:
                ttt[bb,aa] = 0.
            elif inputmat[bb,aa] < (-1.)*th:
                ttt[bb,aa] = inputmat[bb,aa] +th
            
            
            
    return ttt


    
def calcW(datain_h, datain_l, dictin_ht, dictin_lt, dtdh, dtdl, wh,wl, c1,c2,c3, y1,y2,y3,p,q):
    """
    Update sparse coding parameters (Equation (11)). 
	
	Input Arguments
    ----------
    datain_h, datain_l : np.array
        The input data matrices in high and low resolution respectively
    dictin_ht, dictin_lt: np.array
		The transpose of the input dictionary in high and low resolution respectively
	wh, wl: np.array
		The previous sparse coding matrics in high and low resolution respectively
	c1,c2,c3: double
		Step size parameters for the augmentend Lagrangian function
	y1,y2,y3: np.array
		The Langrange multiplier matrices
	p,q: np. array
		The thresholding matrices for high and low resolution respectively.
	"""   
    
    #wh: sparce coding in high resolution
    tmp2 = np.dot(dictin_ht, datain_h) + (y1 - y3) + c1*p + c3*wl
    
    tmp22 = np.dot(dtdh, tmp2)#+y1-y3)
    
    #wh: sparce coding in low resolution    
    tmp4 = np.dot(dictin_lt, datain_l) + (y2 - y3) + c2*q + c3*tmp22
    
    tmp44 = np.dot(dtdl, tmp4)
    
    return [tmp22, tmp44]
    

    
    