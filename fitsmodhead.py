#!/usr/bin/env python3
"""A python version of HEASOFT ftool fmodhead

Simple python tool to modify an existing FITS keyword.

Limitations:
- Currently modifies the keyword in every HDU it exists in.
- No ability to specify a single HDU
- No ability to add or delete keywords

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import os
import os.path
import sys
from astropy.io import fits

__author__ = "Dave Strickland"
__copyright__ = "Copyright 2018, Dave Strickland"
__date__ = "2018/03/14"
__deprecated__ = False
__email__ =  "dave.strickland@gmail.com"
__license__ = "GPLv3"
__version__ = "0.2.0"

def command_line_opts():
    parser = argparse.ArgumentParser()
    # required command line arguments
    parser.add_argument(dest='fitsfile', metavar='INP.fits',
        help='Input FITS file to have keywords modified.')
    parser.add_argument(dest='keyword', default=None, metavar='KEYWORD',
        help='Keyword to have its value modified.')
    parser.add_argument(dest='value', default=None, metavar='VALUE',
        help='Value to set the keyword to.')

    action_default='modify'
    parser.add_argument('--action',
        dest='action', default=action_default,
        help='Action to take on specified keyword. (default: {})'.format(action_default))
    parser.add_argument('-v', '--verbose',
        dest='verbose', action='store_true',
        help='Verbose output for each object processed. Useful for debugging purposes.')
        
    args = parser.parse_args()
    return args

def main():
    p_args = command_line_opts()

    # Don't have to worry about race conditions for this type of work
    if not os.path.isfile(p_args.fitsfile):
        print('Error: Input file {} not found. Current dir: {}'.format(p_args.fitsfile, os.getcwd()))
        sys.exit(1)

    # We can't use with open as... syntax because output_verify
    # has to be called on close() in order to fix non-compliant
    # fits files, even though verifying the headers fixes it in the
    # 'in memory' headers.
    hdu_list = fits.open(p_args.fitsfile, mode='update')
    if p_args.verbose:
        print('Structure of {} follows:'.format(p_args.fitsfile))
        print(hdu_list.info())

    for hdu in hdu_list:
        hdu.verify('silentfix+ignore')
        if p_args.keyword in hdu.header:
            hdr = hdu.header
            print('Original keyword={} value={}'.format(p_args.keyword, hdr[p_args.keyword]))
            hdr[p_args.keyword] = p_args.value
            print('Updated keyword={} value={}'.format(p_args.keyword, hdr[p_args.keyword]))
        
    hdu_list.close(output_verify='silentfix+ignore')
    return

if __name__ == "__main__":
    main()
