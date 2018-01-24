# -*- coding: utf-8 -*-

"""SF DECONVOLVE ARGUMENTS

This module sets the arguments for sf_deconvolve.py.

:Author: Samuel Farrens <samuel.farrens@gmail.com>

:Version: 2.4

:Date: 23/10/2017

"""

import argparse as ap
from argparse import ArgumentDefaultsHelpFormatter as formatter


class ArgParser(ap.ArgumentParser):

    """Argument Parser

    This class defines a custom argument parser to override the
    default convert_arg_line_to_args method from argparse.

    """

    def __init__(self, *args, **kwargs):

        super(ArgParser, self).__init__(*args, **kwargs)

    def convert_arg_line_to_args(self, line):
        """Convert argument line to arguments

        This method overrides the default method of argparse. It skips blank
        and comment lines, and allows .ini style formatting.

        Parameters
        ----------
        line : str
            Input argument string

        Yields
        ------
        str
            Argument strings

        """

        line = line.split()
        if line and line[0][0] not in ('#', ';'):
            if line[0][0] != '-':
                line[0] = '--' + line[0]
            if len(line) > 1 and '=' in line[0]:
                line = line[0].split('=') + line[1:]
            for arg in line:
                yield arg


def get_opts(args=None):

    """Get script options

    This method sets the PSF deconvolution script options.

    Returns
    -------
    arguments namespace

    """

    # Set up argument parser
    parser = ArgParser(add_help=False, usage='%(prog)s [options]',
                       description='PSF Deconvolution Script',
                       formatter_class=formatter,
                       fromfile_prefix_chars='@')
    required = parser.add_argument_group('Required Arguments')
    optional = parser.add_argument_group('Optional Arguments')
    
    

    # Add arguments
    optional.add_argument('-h', '--help', action='help',
                          help='show this help message and exit')

    
    optional.add_argument('-q', '--quiet', action='store_true',
                          help='Suppress verbose.')

    required.add_argument('-ih', '--inputhigh', required=True,
                          help='Input data file name (high resolution).')
    
    required.add_argument('-il', '--inputlow', required=True,
                          help='Input data file name (low resolution).')

    
    required.add_argument('-d', '--dictsize', type=int,
                      help='Dictionanry size.')
    
    required.add_argument('-img', '--imageN', type=int,
                      help='Size of input image.')
    
    
    optional.add_argument('-n', '--n_iter', type=int, default=150,
                              help='Number of iterations.')

    optional.add_argument('--window', type=int, default=1,
                              help='Window to measure error.')
    
    optional.add_argument('--bands_h', type=int, default=25, help='Number of bands in high resolution')
    
    optional.add_argument('--bands_l', type=int, default=9, help='Number of bands in low resolution')
    
    optional.add_argument('--c1', type=float, default=0.4)
    optional.add_argument('--c2', type=float, default=0.4)
    optional.add_argument('--c3', type=float, default=0.8)
    
    optional.add_argument('--maxbeta', type=float, default=1e+6)
    
    optional.add_argument('--delta', type=float, default=1e-4)
    
    optional.add_argument('--beta', type=float, default=0.01)
    
    optional.add_argument('--lamda', type=float, default=0.1)
    
            
    # Return the argument namespace
    
    return parser.parse_args(args)
    
