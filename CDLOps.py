
"""SPARSE COUPLED DICTIONARY LEARNING

Sumplementary Class and Methods for the execution of intermediate matrices (Lagrange multiplier matrices, sparse coding matrices)

:Author: Nancy Panousopoulou <apanouso@ics.forth.gr>

:Reference document: Konstantina  Fotiadou, Grigorios Tsagkatakis, Panagiotos Tsakalides `` Linear Inverse Problems with Sparsity Constraints'', DEDALE DELIVERABLE 3.1, 2016. 

:Date: December 2017

"""

import numpy as np
import AuxOps as aops

import copy



class CDL():
    """Coupled Dictionary Learning Class

    This class defines the intermediate matrices ((Lagrange multiplier matrices, sparse coding matrices)

    Parameters
    ----------
    datain_h : np.ndarray
        Input data array, containing the data cubes in high resolution
    datain_l : np.ndarray
        Input data array, containing the data cubes in low resolution    
	dictsize : int
		The size of the dictionaries
	imageN: int
		The number of samples in low and high resolution data cubes.
    """    
    
    def __init__(self, datain_h, datain_l, dictsize, imageN):
        
        
      
        
        
        
        self.datain_h = datain_h
        self.datain_l = datain_l
        
        #sparse coding matrices
        self.wh = np.zeros((dictsize,imageN))
        self.wl = np.zeros((dictsize,imageN))
        
        #
        self.p = np.zeros((dictsize, imageN))
        self.q = np.zeros((dictsize, imageN))
        
        #Lagrangian multiplier matrices
        self.y1 = np.zeros((dictsize, imageN))
        self.y2 = np.zeros((dictsize, imageN))
        self.y3 = np.zeros((dictsize, imageN))
        
        self.dictsize = dictsize
        
    

def updateCDL(cdlin, dictin_ht, dictin_lt, dtdh, dtdl, c1,c2,c3, maxbeta, beta, lamda):
    """
    Method for updating intermediate matrices 

    Input Arguments
    ----------
    cdlin : CDL object
        The set of intermediate matrices to be updated
    dictin_ht: np.array
		The transpose of the input dictionary in high resolution
	dictin_lt: np.array
        The transpose of the input dictionary in low resolution    
	dtdh: np.array
		Auxiliary matrix - first term of Equation (11) for the high resolution dictionaries
	dtdl: np.array
		Auxiliary matrix - first term of Equation (11) for the low resolution dictionaries
	c1, c2, c3: double
		Step size parameters for the augmentend Lagrangian function
	maxbeta, beta: double
		Auxiliary parameters for updating Lagrange multiplier matrices.
	lamda: double
		The threshold value.
	"""	
    
    y11= cdlin.y1
    y22 = cdlin.y2
    
    y33 = cdlin.y3
    pp = cdlin.p
    
    qq = cdlin.q
    
        
                     
    datain_h = cdlin.datain_h
    datain_l = cdlin.datain_l
        
    wl = cdlin.wl
    wh = cdlin.wh
    
    #print('wh & wl')    
    #update the sparse coding matrices according to Eq. (11)
    
    whl = aops.calcW(datain_h, datain_l, dictin_ht,dictin_lt, dtdh, dtdl, wh, wl, c1,c2,c3, y11,y22,y33,pp,qq)
    
    
    #update the thresholding matrices according to Eq. (13)
    pp = aops.updThr(np.array(whl[0])-y11/c1, lamda)
    qq = aops.updThr(np.array(whl[1])-y22/c2, lamda)
    #update the Lagrange multiplier matrices according to Eq. (19).
    y11 = aops.updateY(y11, c1,  pp, np.array(whl[0]), maxbeta, beta)
    y22 = aops.updateY(y22, c1,  qq, np.array(whl[1]), maxbeta, beta)
    y33 = aops.updateY(y33, c3,  np.array(whl[0]), np.array(whl[1]), maxbeta, beta)   
        
    #print(y11.shape)
    #print(y22.shape)
    #print(y33.shape)
    
    #Save back to the CDL object and return 
    cdlin.wh = np.array(whl[0]).copy()
    cdlin.wl = np.array(whl[1]).copy()
        
        
    cdlin.y1 = y11.copy() 
    cdlin.y2 = y22.copy()
    cdlin.y3 = y33.copy()
    cdlin.p = pp.copy()
    cdlin.q = qq.copy()
        
    return cdlin  

