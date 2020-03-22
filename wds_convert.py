#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  wds_convert.py
#  
#  Copyright 2020 Dave Strickland <dave.strickland@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
"""Convert ASCII WDS file into Fits format, correcting formatting errors. 

"""

import argparse
import os
import os.path
import sys
from astropy.io import fits
from astropy.io import ascii

__author__     = "Dave Strickland"
__copyright__  = "Copyright 2020, Dave Strickland"
__date__       = "2020/03/21"
__deprecated__ = False
__email__      =  "dave.strickland@gmail.com"
__license__    = "GPLv3"
__version__    = "0.2.0"

def command_line_opts():
    parser = argparse.ArgumentParser('Converts ASCII WDS table to Fits format')

    # required command line arguments
    parser.add_argument(dest='data_file', metavar='wds.dat',
        help='Input ASCII WDS data file.')
    parser.add_argument(dest='readme_file', metavar='ReadMe.WDS',
        help='Input ASCII WDS ReadMe file.')
    parser.add_argument(dest='fits_file', metavar='fits_output.fits',
        help='Output Fits-format file.')

    parser.add_argument('-v', '--verbose',
        dest='verbose', action='store_true',
        help='Verbose output for each object processed. Useful for debugging purposes.')
        
    args = parser.parse_args()
    return args

def clean_data(idata_file, odata_file):
    """Cleans up and corrects the ASCII WDS data.
    
    At present it only handles known errors in the DEs column.
    
    :param idata_file: Name of input ASCII data file
    :param odata_file: Name of output ASCII file cleaned data will be written to.
    """
    
    if not os.path.isfile(idata_file):
        print('Error: Input file {} not found'.format(idata_file))
        sys.exit(1)
    
    print('Cleaning up data from {}'.format(idata_file))    
    with open(idata_file, 'r') as f:
        raw_data = f.readlines()
    
    # Expected line length (130 characters plus newline)
    expected_len = 131
    
    # Process data
    clean_data = []
    n_bad = 0
    n_fix = 0
    for idx, line in enumerate(raw_data):
        line_len = len(line)
        if line_len != expected_len:
            n_bad += 1
            new_line, is_good = fix_line(line)
            if is_good:
                clean_data.append(new_line)
                n_fix += 1
            else:
                print('  Unexpected line was line {} (1-based)'.format(idx+1))
        else:
            clean_data.append(line)
    
    print('  Read and processed {} lines from {}'.format(idx+1, idata_file))
    print('  There were {} bad lines of data'.format(n_bad) +
        ' of which we fixed {}.'.format(n_fix))
    
    # Write clean data to file.
    with open(odata_file, 'w') as f:
        f.writelines(clean_data)
    print('  Wrote {} lines of data to {}'.format(len(clean_data), odata_file))
    return

def fix_line(iline):
    """Attempts to fix the line assuming that that the DEs column may be
       missing or partially missing.
       
    The DEs column (chars 127-131, 1-based) is expected to be "xx.x\n",
    but can be "xx.\n" or "\n". In these two cases we add either 00.0 
    or 0 before the newline. 
    
    Other cases we cant handle, just report to user.
    """
    
    status    = True
    good_len  = 131
    case_alen = 130
    case_blen = 127
    
    if len(iline) == good_len:
        # Shouldn't even get passed these lines
        oline = iline
    elif len(iline) == case_alen:
        cut_pnt = case_alen - 1
        oline   = iline[:cut_pnt] + '0' + iline[cut_pnt:]
    elif len(iline) == case_blen:
        cut_pnt = case_blen - 1
        oline   = iline[:cut_pnt] + '0.00' + iline[cut_pnt:]
    else:
        print('Warning: Unexpected line length of {}'.format(len(iline)))
        print('  Line is [{}]'.format(iline))
        oline  = iline
        status = False
    return oline, status

def main(args):
    p_args = command_line_opts()
    readme_file = p_args.readme_file
    data_file   = p_args.data_file
    
    # The CDS file parser expects the data file name to exactly match
    # the names given in the README. This is wds.dat for the main data
    # file. 
    tmpdata_file = 'wds.dat'
    if data_file == tmpdata_file:
        print('Warning: over-writing original input file.')
    clean_data(data_file, tmpdata_file)
    
    r     = ascii.get_reader(ascii.Cds, readme=readme_file)
    table = r.read(tmpdata_file)
    table.write(p_args.fits_file, format='fits', overwrite=True)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
