#!/usr/bin/env python3
""" Test of generating an astropy table

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

import numpy as np
from astropy.table import Table, Column

__author__ = "Dave Strickland"
__copyright__ = "Copyright 2018, Dave Strickland"
__date__ = "2018/02/23"
__deprecated__ = True
__email__ =  "dave.strickland@gmail.com"
__license__ = "GPLv3"
__version__ = "0.1"

def main():
    col_names  = ['aa', 'ab', 'ac']
    col_dtypes = [np.int32, 'S', np.double]
    test_row = [-32, 'hello', 3.141]

    test_table = Table(names=col_names, dtype=col_dtypes)
    print('test table len={} content='.format(len(test_table)), test_table)
    
    print('Adding row...')
    test_table.add_row(test_row)
    print('test table len={} content='.format(len(test_table)), test_table)

    return

if __name__ == "__main__":
    main()
