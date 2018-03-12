#!/usr/bin/env python3
""" Extracts information about stars contained in an input HTML table

This program exists to extract professional-level astronomical information
about the stars listed on the Internet in a HTML-table format, for example
from amatuer astronomy websites.

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
from astropy.table import Table, Column, hstack
import argparse
import warnings
from astropy.utils.exceptions import AstropyUserWarning, AstropyWarning
from SimbadStarQuery import SimbadStarQuery
import DavesAstropyUtils as dapu
import re
import sys

__author__ = "Dave Strickland"
__copyright__ = "Copyright 2018, Dave Strickland"
__date__ = "2018/02/23"
__deprecated__ = False
__email__ =  "dave.strickland@gmail.com"
__license__ = "GPLv3"
__version__ = "0.1"

def fix_names(anInputStr):
    """Perform various fixed on star names from the web HTML tables.

    - Strips cases like 'gamma And   \n  (Almach)' down to 'gamma And'
    - Removes unicode characters Simbad doesn't recognize
    """    
    if not (isinstance(anInputStr, str) or isinstance(anInputStr, np.str_)):
        raise TypeError('anInputStr must be a str or numpy.str_. Was {}'.format(type(anInputStr)))

    # Search for (*) and replace it with ''
    anInputStr = re.sub('\(.*?\)', '', anInputStr)

    # Get rid of internal newlines.
    cleanStr = ' '.join( [ el.strip() for el in anInputStr.splitlines() ] )
    outputStr = dapu.convert_greek_unicode_symbol(cleanStr)
    return outputStr

def command_line_opts():
    p_ihtml = 'input_file_or_txt'
    p_phtml = 'pretty_input_version.html'
    p_ohtml = 'output_summary.html'
    p_otable = 'output.fits.gz'
    p_css = 'darkTable.css'
    p_alias_file = 'simbad_star_alias.csv'
    p_namecol = 'Star'
    parser = argparse.ArgumentParser()
    # required command line arguments
    parser.add_argument(dest='input_file', metavar=p_ihtml,
        help='Input HTML table or ASCII TXT file of stars to be processed.')
    parser.add_argument(dest='ohtml', default=None, metavar=p_ohtml,
        help='Name for output HTML summary of processed data.')
    parser.add_argument(dest='otable', default=None, metavar=p_otable,
        help='name for output processed data table (fits format).')

    # optional arguments
    parser.add_argument('-p', '--pretty',
        dest='pretty', default=None, metavar=p_phtml,
        help='Optional outputted \"pretty\" version of input HTML table that uses the CSS table style for output HTML')
    parser.add_argument('-c', '--col', 
        dest='namecol', default=p_namecol, metavar='colname',
        help='Name of table column containg star name/identifier (default: {})'.format(p_namecol))
    parser.add_argument('--fullhtml', 
        dest='fullhtml', action='store_true', 
        help='Output all data fields used for the fits output to the summary HTML file. By default bibcode, errors, parallax and proper motion are excluded from the summary HTML.')
    parser.add_argument('--css',
        dest='cssfile', default=p_css, metavar='table_style.css',
        help='CSS table style for output HTML (default: {})'.format(p_css))
    parser.add_argument('--aliases',
        dest='star_alias_file', default=p_alias_file, metavar='ALIASES.csv',
        help='CSV file containing mapping between user-supplied star names and names acceptable to Simbad (default: {})'.format(p_alias_file))
    parser.add_argument('-v', '--verbose',
        dest='verbose', action='store_true',
        help='Verbose output for each object processed. Useful for debugging purposes.')
        
    args = parser.parse_args()
    return args

def main():
    # Suppress warnings from the unit module 'cos we're not interested.
    warnings.simplefilter('ignore', category=AstropyWarning, append=True)

    p_args = command_line_opts()

    # known incorrect names or ones that Simbad reacts oddly to.
    bad_names_dict = dapu.read_star_aliases(p_args.star_alias_file)
    if p_args.verbose:
        print('Using {}-element star alias dictionary from {}'.format(
            len(bad_names_dict),
            p_args.star_alias_file))

    p_ifile = p_args.input_file
    print('Input HTML or TXT file: {}'.format(p_ifile))
    if p_args.pretty is not None:
        print('Output pretty HTML version of input file: {}'.format(p_args.pretty))
    print('Output processed data table (FITS): {}'.format(p_args.otable))
    print('Output summary of processed data (HTML): {}'.format(p_args.ohtml))

    # Read in the original HTML or TXT star list into a table for processing
    p_data = dapu.read_table(p_ifile)
    if p_args.pretty is not None:
        dapu.write_to_html(p_data, p_args.pretty, p_args.cssfile)

    # Check the column with the star names/identifiers exists
    if not p_args.namecol in p_data.colnames:
        print('Error: Identifier column name "{}" not found in {} data'.format(p_args.namecol, p_ifile))
        print('  Did you mean "{}" instead?'.format(p_data.colnames[0]))
        print('  Use "--col colname" to specifiy the correct column name on the command line')
        sys.exit(1)

    print('About to process {} stars from {}'.format(len(p_data), p_ifile))
    p_otable = None
    p_ofail_list = None
    [p_otable, p_ofail_list] = do_astroquery(p_args, p_data, bad_names_dict)

    # to replace missing data with a fill value.
    # NOTE: Doesn't quite work as not all missing values are identified
    # as such in simbad returned data, for unknown reasons.
    p_otable = p_otable.filled(-999)

    # write out main table as data and html
    if p_args.verbose:
        print(p_otable.info)
    p_otable.write(p_args.otable, format='fits', overwrite=True)
    #p_otable.write(p_args.otable, format='ascii.ecsv', delimiter=',', overwrite=True)

    # HTML format we only write a summary, removing some columns
    if p_args.fullhtml: 
        p_exclude_list=[]
    else:
        p_exclude_list=['RA_icrs_deg', 'DEC_icrs_deg', 
            'RADEC_bibcode',
            'magB', 'magB_err', 'magB_bibcode', 
            'magV_err', 'magV_bibcode', 
            'parallax', 'parallax_err', 'parallax_bibcode', 
            'pm_RA', 'pm_DEC', 
            'pm_err_maja', 'pm_err_mina', 
            'pm_err_angle', 'pm_bibcode',
            'spec_qual', 'spec_bibcode',
            'Fe_H_bibcode']

    p_tmp_table = Table(p_otable, copy=True)
    if len(p_exclude_list) > 0:
        p_tmp_table.remove_columns(p_exclude_list)
    dapu.write_to_html(p_tmp_table, p_args.ohtml, p_args.cssfile)

    # warn user about objects we failed to query successfully
    if p_ofail_list is not None and len(p_ofail_list) > 0:
        print('Queries failed for the following {} object names.'.format(len(p_ofail_list)))
        print('  Please check these using http://simbad.u-strasbg.fr/simbad/sim-fid OR')
        print('  using http://simbad.u-strasbg.fr/simbad/sim-fcoo')
        print('  Failed objects: {}'.format(p_ofail_list))
    return
    

def do_astroquery(p_args, p_data, p_alias_dict):
    print('Using astroquery for data retrieval.')
    
    # Initialize the class that does the queries and formats the tables.
    sid = SimbadStarQuery(p_alias_dict)
    p_otable = None
    p_fail_list=[]
    p_object_num = -1
    for row in p_data:
        p_object_num = p_object_num + 1
        star_name = fix_names(row[p_args.namecol])
        print('Processing {}'.format(star_name))
        sid.do_query(star_name)
        if not sid.successfully_queried:
            print('  Warning: Simbad.query_object fails for {}'.format(star_name))
            p_fail_list.append(star_name)
            continue

        num_rows = sid.num_rows_returned
        if (num_rows == 0):
            print('  Warning: No rows returns from Simbad.query_object for {}'.format(star_name))
            p_fail_list.append(star_name)
            continue
        elif (num_rows > 1):
            print('  Warning: {:d} rows returned from Simbad.query_object for {}'.format(num_rows, star_name))
            p_fail_list.append(star_name)
            continue
        

        # Define the output table structure based on content on simbad object
        if p_otable is None:
            p_otable = sid.get_table()
            ##if p_args.verbose:
            ##    print('  Initial table:\n',
            ##        p_otable)

        else:
            # Add row data existing table
            p_otable.add_row( sid.get_row() )
            ##if p_args.verbose:
            ##    # Note sure why row print out isn't truncated the normal way
            ##    print('  Table for object number {}:\n'.format(p_object_num), 
            ##        p_otable[p_object_num])

    if p_args.verbose:
        print(p_otable)
    return p_otable, p_fail_list
    
if __name__ == "__main__":
    main()
