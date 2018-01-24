
"""SPARSE COUPLED DICTIONARY LEARNING

The main script for execution

:Author: Nancy Panousopoulou <apanouso@ics.forth.gr>

::Reference document: Konstantina  Fotiadou, Grigorios Tsagkatakis, Panagiotos Tsakalides `` Linear Inverse Problems with Sparsity Constraints,'' DEDALE DELIVERABLE 3.1, 2016. 

:Date: December 2017

"""
import numpy as np


#from numpy import linalg as la


from numpy import genfromtxt
from math import sqrt

#import scipy.io as sio
from numpy.linalg import inv
from args import get_opts

from CDLOps import CDL, updateCDL
import time

def normD(dictin):
    """
    Normalize the dictionary between [0,1] 
    
    Input Arguments
    ----------
    dictin : np.array
        The input dictionary
    """    
    
    
    
    tmp = 1 / np.sqrt(np.sum(np.multiply(dictin, dictin), axis=0))
    
    return np.dot(dictin, np.diag(tmp))
    
         
def run_script():

    #the size of the image
    imageN =  opts.imageN 
    
    #the size of the dictionary 
    dictsize = opts.dictsize
    
    #the number of bands in high resolution
    bands_h_N = opts.bands_h
    
    #the number of bands in low resolution
    bands_l_N = opts.bands_l
    
    #parameters for training. 
    c1 = opts.c1 # Default value: 0.4
    
    c2 = opts.c2 # Default value: 0.4
    
    c3 = opts.c3 # Default value: 0.8
    
    maxbeta = opts.maxbeta #Default value: 1e+6 
    
    delta = opts.delta #Default value: 1e-4
    beta = opts.beta #Default value: 0.01
    lamda = opts.lamda #Default value: 0.1
    
    #number of iterations for training
    train_iter =opts.n_iter #default value: 150
    
    #the window for calculating the value of the error.
    wind = opts.window
    
    
    #input data are in the from (# of Pixels) x (# of Bands)
    data_h = genfromtxt(opts.inputhigh, delimiter=',')
    data_l = genfromtxt(opts.inputlow, delimiter=',')    
     
    #the initial dictionaries are in the from (Dictionary Size) x (# of Bands) 
    dict_h = data_h[:, 0:dictsize]
    dict_l = data_l[:, 0:dictsize]
   
    
    #normalize the dictionaries
    #dict_l = dict_l /la.norm(dict_l)
    #dict_h = dict_h /la.norm(dict_h)
    
    
    #mat2save =  './tttmpinit' + '_' + str(imageN) + 'x' + str(dictsize) + '.mat'  
    #sio.savemat(mat2save, {'dicth_init':dict_h, 'dictl_init': dict_l})
   
    #the CDL object responsible for all calculations...
    cdl = CDL(data_h, data_l, dictsize, imageN)
    
    phi_h = np.zeros(dictsize)
    phi_l = np.zeros(dictsize)
    
    dict_h_upd = np.zeros(dict_h.shape)
    dict_l_upd = np.zeros(dict_l.shape) 

    
    for k in range(train_iter):
        
        print(k)
        ttime3 = time.time()
        ##prepare the updated values of dictionaries for updating Wh, Wl, P, Q, Y1,Y2, Y3
        dict_ht = np.transpose(dict_h)
        dict_lt = np.transpose(dict_l)
    
   
        #(D_h^{T} \times D_h + (c_1+c_3)\times I)^{-1} -- first term of equation (11) for high resolution
        dtdh = np.dot(np.transpose(dict_h), dict_h) +  (c1 + c3)*np.eye(np.transpose(dict_h).shape[0])
        dtdhinv = inv(dtdh)
        #(D_l^{T} \times D_l + (c_2+c_3)\times I)^{-1} -- first term of equation (11) for low resolution
        dtdl = np.dot(np.transpose(dict_l), dict_l) +  (c2 + c3)*np.eye(np.transpose(dict_l).shape[0])
        dtdlinv = inv(dtdl)
        
        
        
        print('update...')
        #update all auxiliary matrices Wh, Wl, P, Q, Y1, Y2, Y3
        cdl = updateCDL(cdl, dict_ht, dict_lt, dtdhinv, dtdlinv,c1,c2,c3, maxbeta, beta, lamda)    
        
        
        for ii in range(dictsize):
            phi_h[ii] = np.dot(cdl.wh[ii,:], np.transpose(cdl.wh[ii,:])) + delta
            phi_l[ii] = np.dot(cdl.wl[ii,:], np.transpose(cdl.wl[ii,:])) + delta
        
        
        
        dict_h_upd = dict_h + np.dot(data_h, np.transpose(cdl.wh))/(phi_h)
        dict_l_upd = dict_l + np.dot(data_l, np.transpose(cdl.wl))/(phi_l) 

        #print(dict_h_upd.shape)
        #print(dict_l_upd.shape)
        #normalize dictionaries between [0,1]
        #dict_h = dict_h_upd / la.norm(dict_h_upd)
        #dict_l = dict_l_upd / la.norm(dict_l_upd)
        dict_h = normD(dict_h_upd)
        dict_l = normD(dict_l_upd)
     
        
        if ~((k +1) % wind):
            
            
        
            
            err_h = sqrt(np.sum(np.sum(np.square(cdl.datain_h - np.dot(dict_h, cdl.wh)))) / (bands_h_N * imageN)) 
            err_l = sqrt(np.sum(np.sum(np.square(cdl.datain_l - np.dot(dict_l, cdl.wl)))) / (bands_l_N * imageN))
    
            
            
            print('ERROR HIGH:')
            print(err_h)
            
            print('ERROR LOW:')
            print(err_l)
        
        
        
        print('Time elapsed for this iteration: ')
        ttime3 = time.time()-ttime3
        print(ttime3)
        #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            
        #mat2save =  './results' + str(imageN) + 'x' + str(dictsize) + '_' + str(k) +'standalone.mat'  
        
        #sio.savemat(mat2save, {'timeelapsed': ttime3, 'dicth':dict_h, 'dictl': dict_l, 'phi_h': phi_h, 'phi_l': phi_l, 'err_l':err_l, 'err_h': err_h})#, 'wh': wh, 'wl': wl})#'phih': phi_h, 'sw': sw})
      
      
def main(args=None):

    
    global opts
    opts = get_opts(args)
    run_script()
    

if __name__ == "__main__":
    main()

