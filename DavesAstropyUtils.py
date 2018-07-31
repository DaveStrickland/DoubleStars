#!/usr/bin/env python3
""" Various utilities for dealing with astropy

A set of unrelated utility functions related to astropy

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

__author__ = "Dave Strickland"
__copyright__ = "Copyright 2018, Dave Strickland"
__date__ = "2018/02/23"
__deprecated__ = False
__email__ =  "dave.strickland@gmail.com"
__license__ = "GPLv3"
__version__ = "0.2.0"

def convert_greek_unicode_symbol(anInputStr):
    """Replaces unicode greek symbols with the ASCII textual name 
    of that symbol.
    
    Also replaces some problematic unicode characters that are not
    recognized by the Simbad ID service. Note that unicode characters
    and their hex codes can be looked up on the web, e.g. at
    https://www.fileformat.info/info/unicode/char/search.htm or
    https://unicodelookup.com/, if you know what you're looking 
    for. To find what unicode character is
    in some text use http://www.babelstone.co.uk/Unicode/whatisit.html
    """
    # Greek alphabet mapping from https://gist.github.com/beniwohli/765262
    greek_alphabet = {
        u'\u0391': 'Alpha',
        u'\u0392': 'Beta',
        u'\u0393': 'Gamma',
        u'\u0394': 'Delta',
        u'\u0395': 'Epsilon',
        u'\u0396': 'Zeta',
        u'\u0397': 'Eta',
        u'\u0398': 'Theta',
        u'\u0399': 'Iota',
        u'\u039A': 'Kappa',
        u'\u039B': 'Lamda',
        u'\u039C': 'Mu',
        u'\u039D': 'Nu',
        u'\u039E': 'Xi',
        u'\u039F': 'Omicron',
        u'\u03A0': 'Pi',
        u'\u03A1': 'Rho',
        u'\u03A3': 'Sigma',
        u'\u03A4': 'Tau',
        u'\u03A5': 'Upsilon',
        u'\u03A6': 'Phi',
        u'\u03A7': 'Chi',
        u'\u03A8': 'Psi',
        u'\u03A9': 'Omega',
        u'\u03B1': 'alpha',
        u'\u03B2': 'beta',
        u'\u03B3': 'gamma',
        u'\u03B4': 'delta',
        u'\u03B5': 'epsilon',
        u'\u03B6': 'zeta',
        u'\u03B7': 'eta',
        u'\u03B8': 'theta',
        u'\u03B9': 'iota',
        u'\u03BA': 'kappa',
        u'\u03BB': 'lamda',
        u'\u03BC': 'mu',
        u'\u03BD': 'nu',
        u'\u03BE': 'xi',
        u'\u03BF': 'omicron',
        u'\u03C0': 'pi',
        u'\u03C1': 'rho',
        u'\u03C3': 'sigma',
        u'\u03C4': 'tau',
        u'\u03C5': 'upsilon',
        u'\u03C6': 'phi',
        u'\u03C7': 'chi',
        u'\u03C8': 'psi',
        u'\u03C9': 'omega'}
    
    # Unicode characters Simbad can't handle
    tricky_unicode = {
        u'\u2019': "'"    # U+2019 single right quote
        }
    
    # iterate over input string character by character
    outputList = []
    for c in anInputStr:
        if c in greek_alphabet:
            out = greek_alphabet[c]
            #print('found {} in alphabet, replace with {}'.format(c, out))
            outputList.append(out)
        elif c in tricky_unicode:
            out = tricky_unicode[c]
            outputList.append(out)
        else:
            outputList.append(c)
    outputStr = ''.join(outputList).strip()
    return outputStr

def read_table(input_file, p_verbose=False):
    """Attempts to read the file into an astropy Table object.

    This function attempts to determine the file type based on the file
    name, and then calls the correct reader function.
    """
    import sys
    import os.path

    # Don't have to worry about race conditions for this type of work
    if not os.path.isfile(input_file):
        print('Error: Input file {} not found'.format(input_file))
        sys.exit(3)
    
    try:
        if 'txt' in input_file or 'csv' in input_file:
            p_data = read_ascii(input_file, p_verbose)
        elif 'html' in input_file:
            p_data = read_html(input_file, p_verbose)
        elif 'fits' in input_file:
            p_data = read_fits(input_file, p_verbose)
        else:
            print('Error: Unexpected file format for input file {}'.format(input_file))
            sys.exit(1)
    except:
        print('Error: Failed to correctly read {}'.format(input_file))
        sys.exit(2)
    
    if p_verbose:
        print('Read {} row tables from {}'.format(len(p_data), input_file))
    return p_data

def read_ascii(input_txt_file, p_verbose=False):
    """Reads data from a comma separated txt/csv file, returning an astropy Tables object

    The format of the input txt/csv file shoould be one object per line, 
    with the first non-commented line being the Table column heading.
    Commas should be used as delimiters.
    """
    from astropy.table import Table
    if p_verbose:
        print('Reading data table from {}'.format(input_txt_file))
    p_data = Table.read(input_txt_file, 
        format='ascii.basic', 
        delimiter=',')
    if p_verbose:
        print(p_data.info)
    return p_data

def read_html(input_html_table, p_verbose=False):
    """Reads data from a cleanly formatted HTML table, returning an astropy Tables object"""
    from astropy.table import Table
    if p_verbose:
        print('Reading data table from {}'.format(input_html_table))
    p_data = Table.read(input_html_table, 
        format='ascii.html')
    if p_verbose:
        print(p_data.info)
    return p_data

def read_fits(input_html_table, p_verbose=False):
    """Reads data from a FITS or gzipped FITS file, returning an astropy Tables object"""
    from astropy.table import Table
    if p_verbose:
        print('Reading data table from {}'.format(input_html_table))
    p_data = Table.read(input_html_table, 
        format='fits')
    if p_verbose:
        print(p_data.info)
    return p_data

def write_table(atable, an_output_file, a_css_style):
    """Writes the astropy Table to disk using a format determined
    from the file name itself.
    """
    if '.fits' in an_output_file:
        write_to_fits(atable, an_output_file)
    elif '.html' in an_output_file:
        write_to_html(atable, an_output_file, a_css_style)
    else:
        print('Error: Unexpected file format for output table')
        print('  File name: {}'.format(an_output_file))
        print('  Expecting file name suffix to include either "fits" or "html"')
        print('  Nothing will be written now...')
    return

def write_to_fits(atable, an_output_file):
    """Write an astropy table to a fits file
    """
    atable.write(an_output_file, format='fits', overwrite=True)
    return

def write_to_html(atable, an_output_file, a_css_style=None):
    """Writes out an astropy Table to HTML while applying a CSS style to it."""
    from astropy.table import Table
    if a_css_style is None:
        a_css_style = 'darkTable.css'
    # This reads the css and applies it within the table
    with open(a_css_style, 'r') as css_file:
       p_css_str = css_file.read() 

    # Need to extract actual name of table style used in the CSS. Assuming
    # its the first and only one.
    first = p_css_str.split(None, 1)[0]
    p_style = first.split('.')[1]

    p_html_dict = {'css': p_css_str,
        'table_class': p_style}

    # For some reason the include_names and exclude_names options listed
    # in the astropy documentation don't work.
    atable.write(an_output_file, 
        format='ascii.html', 
        overwrite=True, 
        htmldict=p_html_dict)
    print('Wrote formatted table to {} using CSS style {}'.format(an_output_file, p_style))
    return

def read_star_aliases(star_alias_csv_file):
    """Creates a dictionary of problematic user star names and the
    names that Simbad will recognize, used by SimbadStarQuery.
    """
    import csv
    star_alias_dict = {}
    with open(star_alias_csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        # skip first line as its a header
        next(csvreader)
        for row in csvreader:
            if len(row) < 2:
                print('Warning: row from {} contains less than two items. Skipping it.'.format(star_alias_csv_file))
            else:
                star_alias_dict[row[0]] = row[1]
    return star_alias_dict
