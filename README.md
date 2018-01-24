SRARSE COUPLED DICTIONARY LEARNING
=============

> Author: **Konstantina Fotiadou, Greg Tsagkatakis, Nancy Panousopoulou**  
> Year: **2017-2018**   
> Email: [kfot@ics.forth.gr](mailto:kfot@ics.forth.gr), [greg@ics.forth.gr](mailto:greg@ics.forth.gr)
> Website: [https://github.com/spl-icsforth](https://github.com/spl-icsforth)  
> Reference Documents: Konstantina  Fotiadou, Grigorios Tsagkatakis, Panagiotos Tsakalides, "Linear Inverse Problems with Sparsity Constraints," DEDALE DELIVERABLE 3.1, 2016.  

Contents
------------
1. [Introduction](#intro_anchor)
1. [Dependencies](#depend_anchor)
1. [Execution](#exe_anchor)
    1. [Input Format](#in_format)
    1. [Required Input Parameters](#required)
    1. [Optional Input Parameters](#optional)
    1. [Example](#eg_anchor)


<a name="intro_anchor"></a>
## Introduction

This repository is designed for solving the problem of spectral super-resolution, adhering to a sparse-based machine learning technique. Our goal is to recover a high-spectral resolution multi- or hyperspectral image from only few spectral observations. The estimation of the high-spectral resolution scene is formulated as the joint estimation of the coupled pair of dictionaries, representing both the low and the high spectral resolution feature spaces, and the joint sparse coefficients. Specifically, we design a coupled dictionary learning (CDL) architecture, relying on the alternating direction method of multipliers (ADMM), which updates the dictionaries by closed form solutions. 
Our CDL algorithm considers as input multiple training examples (i.e. hyper-pixels) extracted from corresponding low- and high- spectral resolution data-cubes, along with a few specification parameters, such as: 

* The number of iterations in order to achieve high convergence rate;
* The sparsity regularization parameter that balances the fidelity of the reconstruction;
* The number of dictionary atoms, which denotes the coupled dictionaries size.

The output of our algorithm include the coupled dictionaries (i.e. high and low spectral resolution), along with the reconstruction errors (RMSE) for both the dictionaries and the augmented lagrangian function.

<a name="depend_anchor"></a>
## Dependencies

<a name="required_package"></a>
### Required Packages

In order to run the code in this repository the following packages must be installed:

* [Python](https://www.python.org/)</a>**
[Tested with v 2.7.12]

* [Numpy](http://www.numpy.org/)** [Tested with v 1.14.0, v 1.13.3]

* [Scipy](http://www.scipy.org/)** [Tested with v 1.0.0]


<a name="exe_anchor"></a>
## Execution

The code for execution is the python script ``SparseCoupledDictionaryTraining.py`` which considers as input a low- and high- spectral resolution data-cubes and calculates the coupled dictionanries (i.e. in low and high resolution), as well as the reconstruction errors (RMSE) for both the dictionaries and the augmented lagrangian function.

The python scripts CDLOps.py and AuxOps.py contain sumplementary classes and methods for all intermediate steps. The args.py script defines the required and optional input parameters for executing the code.

<a name="in_format"></a>
### Input Format

The input files should have the following format:

- Input Data-cubes: Two csv files (one for low and one for high resolution) should be provided in the form (#of bands) x (#of samples). 

For example, if the number of bands in low resolution equals to 9, and the number of bands in high resolution equals 25, and each data cube has 100 samples, then the input for the high resolution is a matrix [25, 100] and the input for the low resolution is a matrix [9, 100].

Consult the csv files provided under the folder `data samples`.

<a name="required"></a>
### Required Input Parameters

This library considers the following required input parameters:

* '-ih', '--inputhigh': Input data file name (high resolution).
* '-il', '--inputlow': Input data file name (low resolution).
* '-d', '--dictsize': The number of atoms for the low and high resolution dictionaries
* '-img', '--imageN': The size of the image (number of samples for input high and low resolution data cubes)

<a name="optional"></a>
### Optional input parameters
This library considers the following optional input parameters:

* '-n', '--n_iter': The number of iterations for calculating the dictionaries (Default value: 150)
* '--window': The window for calculating the RMSE
* '--bands_h': The number of bands in high resolution. Default value 25.
* '--bands_l': The number of bands in low resolution. Default value 9.
* '--c1': Step size parameter for the augmentend Lagrangian function. Default value 0.4.
* '--c2': Step size parameter for the augmentend Lagrangian function. Default value 0.4.
* '--c3': Step size parameter for the augmentend Lagrangian function. Default value 0.8.
* '--maxbeta': Auxiliary parameter for updating Lagrange multiplier matrices. Default value 1e+6
* '--delta': Regularization factor. Default value 1e-4
* '--beta': Auxiliary parameter for updating Lagrange multiplier matrices. Default value 0.01
* '--lamda': The threshold value. Default value 0.1


<a name="py_ex"></a>
### Running the executable script

The code runs at a terminal (not in a Python session):

```bash
$ python SparseCoupledDictionaryTraining.py --inputhigh INPUT_HR.csv --inputlow INPUT_LR.csv --dictsize DICTSIZE --imageN IMG --bands_h BANDS_H --bands_l BANDS_L --n_iter N --window W
```

Where:

* `INPUT_HR.csv` is the csv file containing the data cubes in high resolution
* `INPUT_LR.csv` is the csv file containing the data cubes in low resolution
* `DICTSIZE` is the size (number of atoms) of the dictionaries that will be calculated
* `IMG` is the size of the input data samples
* `BANDS_H` is the number of bands in high resolution
* `BANDS_L` is the number of bands in low resolution
* `N` is the number of iterations for calculating the dictionaries
* `W` is the window for calculating the RMSE


<a name="eg_anchor"></a>
### Example

The following example uses sample data cubes of size 25x100 in high resolution and 9x100 in low resolution, in order to produce two dictionaries (in low and high resolution) containing 64 atoms.

The corresponding csv files are available at ``datasamples`` directory.


```bash
$ python SparseCoupledDictionaryTraining.py --inputhigh datasamples/input_hr.csv --inputlow datasamples/input_lr.csv --dictsize 64 --imageN 100 --bands_h 25 --bands_l 9 --n_iter 100 --window 10
```
After the termination of the loop the output of the algorithm is stored in variables `dict_h`, `dict_l` (dictionaries in high and low resolution) and `err_h`, `err_l` (RMSE in high and low resolution).

## How to reference
If you find any of this library useful for your research, please give credit in your publications where it is due.

## Disclaimer
Copyright (c) 2017-2018, Signal Processing Lab (SPL), Institute of Computer Science (ICS), FORTH, Greece.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the Signal Processing Lab, the Institute of Computer Science and FORTH, nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THE SOFTWARE LIBRARIES AND DATASETS ARE PROVIDED BY THE INSTITUTE AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
