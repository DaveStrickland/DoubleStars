#!/usr/bin/env python3
""" Extracts stellar data for named objects from Simbad using astroquery,
    returning the results in astroppy Table format.

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

from astroquery.simbad import Simbad
from astropy.table import Table, Column, hstack
from astropy.coordinates import SkyCoord
from astropy import units as u
import warnings
from astropy.utils.exceptions import AstropyUserWarning, AstropyWarning

__author__ = "Dave Strickland"
__copyright__ = "Copyright 2018, Dave Strickland"
__date__ = "2018/02/23"
__deprecated__ = False
__email__ =  "dave.strickland@gmail.com"
__license__ = "GPLv3"
__version__ = "0.1"

class SimbadStarQuery:
    """Queries Simbad for information about a stellar object,
    making the data available as an astropy Tables object.
    """
    
    def __init__(self, simbad_alias_dict=None):
        """Initializes a SimbadStarQuery object
        
        Inputs are an optional user-supplied dictionary that contains a
        mapping between known problematic user names
        and valid Simbad identifiers. This dictionary
        can be construced using DavesAstropyUtils.read_star_aliases().
        """
        self.user_ident = None
        self.simbad_alias_dict = simbad_alias_dict

        warnings.simplefilter('ignore', category=UserWarning, append=True)

        # This changes the default behaviour of ALL Simbad queries,
        # so it has the unfortunate effect of affecting future queries.
        Simbad.reset_votable_fields()
        Simbad.remove_votable_fields('coordinates')
        Simbad.add_votable_fields('ra(icrs)', 'dec(icrs)', 'coo_bibcode',
            'flux(B)', 'flux_error(B)', 'flux_bibcode(B)',
            'flux(V)', 'flux_error(V)', 'flux_bibcode(V)',
            'plx', 'plx_error', 'plx_bibcode', 
            'pm', 'pm_bibcode',
            'sp', 'sp_qual', 'sp_bibcode',
            'fe_h')
        
        # depends on prior knowledge of output names
        self.format_code_dict = {'FLUX_B': '{:.2f}',
            'FLUX_ERROR_B': '{:.2f}',
            'FLUX_V':       '{:.2f}',
            'FLUX_ERROR_V': '{:.2f}',
            'PLX_VALUE':    '{:.2f}',
            'PLX_ERROR':    '{:.2f}',
            'PMRA':         '{:.2f}',
            'PMDEC':        '{:.2f}',
            'PM_ERR_MAJA':  '{:.2f}',
            'PM_ERR_MINA':  '{:.2f}',
            'Fe_H_Fe_H':    '{:.2f}'}

        self.vo_to_output_name_dict = {'MAIN_ID': 'SimbadID',
            'COO_BIBCODE':  'RADEC_bibcode',
            'FLUX_B':       'magB',
            'FLUX_ERROR_B': 'magB_err',
            'FLUX_BIBCODE_B': 'magB_bibcode',
            'FLUX_V':       'magV',
            'FLUX_ERROR_V': 'magV_err',
            'FLUX_BIBCODE_V': 'magV_bibcode',
            'PLX_VALUE':    'parallax',
            'PLX_ERROR':    'parallax_err',
            'PLX_BIBCODE':  'parallax_bibcode',
            'PMRA':         'pm_RA',
            'PMDEC':        'pm_DEC',
            'PM_ERR_MAJA':  'pm_err_maja',
            'PM_ERR_MINA':  'pm_err_mina',
            'PM_ERR_ANGLE': 'pm_err_angle',
            'PM_BIBCODE':   'pm_bibcode',
            'SP_TYPE':      'spec_type',
            'SP_QUAL':      'spec_qual',
            'SP_BIBCODE':   'spec_bibcode',
            'Fe_H_Teff':    'Teff_(Fe_H)',
            'Fe_H_Fe_H':    '[Fe/H]',
            'Fe_H_bibcode': 'Fe_H_bibcode'}
            
        self.vo_extra_description_dict = {'MAIN_ID': 'Main ID used by Simbad',
            'WDS':          'Washington Double Star Catalog ID',
            'SAO':          'SAO Star Catalog ID',
            'HIP':          'Hipparcos Output Catalog ID',
            'NAME':         'Common name',
            'HD':           'Henry Draper Catalog ID',
            'COO_BIBCODE':  'Bibcode for coordinates',
            'FLUX_B':       'V-band apparent magnitude',
            'FLUX_ERROR_B': 'Uncertainty in B-band apparent magnitude',
            'FLUX_BIBCODE_B': 'Bibcode for B-band apparent magnitude',
            'FLUX_V':       'V-band apparent magnitude',
            'FLUX_ERROR_V': 'Uncertainty in V-band apparent magnitude',
            'FLUX_BIBCODE_V': 'Bibcode for V-band apparent magnitude',
            'PLX_VALUE':    'parallax',
            'PLX_ERROR':    'parallax_err',
            'PLX_BIBCODE':  'Bibcode for parallax',
            'PM_BIBCODE':   'Bibcode for proper motion',
            'SP_TYPE':      'Spectral type including luminosity class',
            'SP_BIBCODE':   'Bibcode for spectral type',
            'Fe_H_Teff':    'Effective temperature in K',
            'Fe_H_Fe_H':    'Metal abundance relative to Sun in dex',
            'Fe_H_bibcode': 'Bibcode for metal abundance and Teff'}
        return

    def get_simbad_object_id(self, user_ident, simbad_alias_dict):
        """Replaces the user star ID with a known Simbad compliant ID

        If the user's ID is in the simbad_alias_dict supplied by the
        creator of this object, then use the alias. Otherwise return the
        original user_ident as a simbad_ident to be used in the astroquery.
        """
        simbad_ident = user_ident
        if simbad_alias_dict is not None:
            if user_ident in simbad_alias_dict:
                simbad_ident = simbad_alias_dict[user_ident]
        return simbad_ident

    def get_table(self):
        """Returns the data associated with the latest query as
        an astropy.tables.Table object"""
        return Table(self.table, copy=True)
        
    def get_row(self):
        """Returns the data associated with the latest query as
        an astropy.tables.Row object
        """
        return self.table[0]
        
    def fix_main_id(self, result_table):
        """Fix some problem MAIN_ID returned by Simbad.
        
        Simbad will occasionally return "NAME Barnard's Star"
        instead of just "Barnard's Star". This function removes
        any "NAME " in the MAIN_ID. 
        """
        # Convert to string from bytes if necessary
        if result_table['MAIN_ID'].dtype in ['object']:
            wdth = self.best_str_len( len(result_table['MAIN_ID'][0]) )
            result_table['MAIN_ID'] = result_table['MAIN_ID'].astype('U{}'.format(wdth))
        
        if 'NAME ' in result_table['MAIN_ID'][0]:
            result_table['MAIN_ID'][0] = result_table['MAIN_ID'][0].replace('NAME ', '')
        return
        
    def do_query(self, user_ident):
        """Queries Simbad for the user-supplied object and processes the
        output.
        """
        # Reset some stuff.
        self.successfully_queried = False
        self.num_rows_returned = 0
        self.table = None

        # Turn non-Simbad compliant IDs into ones acceptable to Simbad
        self.user_ident = user_ident
        self.simbad_object_id = self.get_simbad_object_id(self.user_ident,
            self.simbad_alias_dict)
        
        # Query Simbad and make sure we get one (1) row returned
        result_table = Simbad.query_object(self.simbad_object_id)

        # check what we've got back
        if result_table is None:
            return
        else:
            self.num_rows_returned = len(result_table)
            if self.num_rows_returned == 0:
                return
            elif self.num_rows_returned > 1:
                return

        # Check we have data in the returned table.
        if self.sanity_check(result_table) is False:
            return

        self.fix_main_id(result_table)
        self.add_user_ident(result_table)

        # Fix up the coordinates so we have a uniform presentation
        self.fix_coordinates(result_table, 'RA_icrs', 'DEC_icrs')
        
        self.process_fe_h(result_table)

        # astroquery returns many fields a b'' byte strings that
        # Table considers to be dtype.object. FITs IO cannot handle
        # such object formats (although ascii IO can).
        # To solve this problem we detect such cases and force conversion
        # to Unicode strings.
        for colname in result_table.colnames:
            if result_table[colname].dtype in ['object']:
                wdth = self.best_str_len( len(result_table[colname][0]) )
                result_table[colname] = result_table[colname].astype('U{}'.format(wdth))

        # Get the alternate IDs in a table, column name 'ID"
        ids_table = Simbad.query_objectids(self.simbad_object_id)
        ids_list = ids_table['ID'].data.tolist()
        p_interesting_ids = self.parse_identifiers(ids_list)
        self.table = self.join_data_and_ids(result_table, p_interesting_ids)
        
        for col in self.table.colnames:
            # Add or update description, uses original column names
            if col in self.vo_extra_description_dict.keys():
                self.table[col].description = self.vo_extra_description_dict[col]
            # Fix/improve formatting
            if col in self.format_code_dict.keys():
                self.table[col].format = self.format_code_dict[col]
            # Final clean-up column names
            if col in self.vo_to_output_name_dict.keys():
                self.table.rename_column(col, self.vo_to_output_name_dict[col])

        self.successfully_queried = True
        return

    def process_fe_h(self, query_result_table):
        """Removes unwanted column returned as part of 'fe_h' query

        We remove these as:
        - Fe_H_log_g Gravity value only of interest to professional stellar astronomers
        - Fe_H_flag A detail we're not currently interested in
        - Fe_H_CompStar Comparison star is always the Sun
        - Fe_H_CatNo Not interested in the catalog number
        """
        fe_h_exclude_list = ['Fe_H_log_g', 'Fe_H_flag', 'Fe_H_CompStar', 'Fe_H_CatNo']
        query_result_table.remove_columns(fe_h_exclude_list)
        return
    
    def sanity_check(self, query_result_table):
        """Performs some sanity checks on Simbad object query's returned table.

        In some cases Simbad will accept a object query that matches some
        internal criteria but that does not actually correspond to a real
        object, for example 'psi Psc'. In this case it returns a table
        with the object name but empty data rather than returning an zero
        row table like we'd expect.

        This function does some checks on the table to make sure its
        cost real data in it.
        """
        pass_check = True

        # check RA and DEC are both present
        for col in ['RA_icrs', 'DEC_icrs']:
            val = query_result_table[col][0]
            if val is None:
                pass_check = False
            else:
                ldata = len(val)
                if ldata == 0:
                    pass_check = False
        return pass_check

    def join_data_and_ids(self, data_table, id_table):
        main_index = data_table.index_column('MAIN_ID')
        col_list = []
        idx_list = []
        for col in id_table.colnames:
            col_list.append(id_table[col])
            idx_list.append(main_index+1)
        data_table.add_columns(col_list,
            indexes=idx_list,
            copy=True)
        return data_table
    
    def best_str_len(self, an_input_str_len):
        """Work out an optimal str width for astropy tables based on a str len"""
        wdth = 8
        # // does integer division in python 3
        return wdth*(1 + (an_input_str_len // wdth))

    def parse_identifiers(self, ids_list):
        """
        Returns a single-row table containing the chosen identifiers
        that can be hstack'd onto a 1-row table of other info about this
        object.
        """
        p_id_names  = ['WDS', 'SAO', 'HIP', 'NAME', 'HD'];
        p_id_vals   = []
        # Can't use ints for HD as some have Alphanumeric suffices.
        ##p_id_dtypes = ['U20', np.int32, np.int32, 'U20', np.int32]
        p_id_dtypes = ['U20', 'U20', 'U20', 'U20', 'U20']
    
        ids_list.sort()
    
        for identifier in p_id_names:
            p_identifier_list=[]
            for line in ids_list:
                p_split = line.decode('utf-8').split()
                if identifier in p_split[0]:
                    p_identifier_list.append(p_split[1])
    
            # check how many results we've got
            if len(p_identifier_list) > 1:
                # Treatment depends on type of identifier
                if identifier in 'WDS':
                    # choose shortest string. Note list osrt returns none, its inplace
                    p_identifier_list.sort(key=len)
                    p_choice = p_identifier_list[0]
                else:
                    # simply take first
                    p_choice = p_identifier_list[0]
                p_id_vals.append(p_choice)
                print('  Warning: For identifier={} multiple responses found: {}'.format(identifier, p_identifier_list))
                print('    Choosing {}'.format(p_choice))
            elif len(p_identifier_list) == 1:
                p_id_vals.append(p_identifier_list[0])
            else:
                p_id_vals.append(None)
    
        # create table, rows has really to be a list of lists, not just a list.
        p_interesting_ids = Table(rows=[p_id_vals],
            names=p_id_names, dtype=p_id_dtypes)
            
        return p_interesting_ids
    
    def fix_coordinates(self, simbad_table, ra_name, dec_name, sys='icrs'):
        """Perform some fix-up work on the coordinate info returned by a Simbad query_object
        
        This routine takes the arbitrary precision string-formatted
        coordinates from the table row returned by the simbad query,
        and does the following:
        - Creates a SkyCooord object
        - Extracts floating point RA and DEC in decimal degrees, more
          useful for any later automated processing etc.
        - Rewrites string format sexigesimal RA and DEC with a fixed
          precision (0.1 seconds, 0.1 arcseconds), which looks better
          for textual presentation as it has a fixed width.
        """
        ra_str  = simbad_table[ra_name][0]
        dec_str = simbad_table[dec_name][0]
    
        # convert to sky coord
        sc = SkyCoord([(ra_str, dec_str)], unit=(u.hourangle, u.deg), frame=sys)
        # returns a list, so just get first element
        ra_deg  = sc.ra.degree[0]
        dec_deg = sc.dec.degree[0]
        # sc.ra.to_string returns a list, so just get first element
        ra_str  = sc.ra.to_string(u.hour, sep=':', precision=1)[0]
        dec_str = sc.dec.to_string(u.deg, sep=':', precision=1)[0]
            
        # update existing columns
        simbad_table[ra_name][0] = ra_str
        simbad_table[dec_name][0] = dec_str
        simbad_table[ra_name].description = 'Right ascension, HMS, ICRS at J2000 epoch'
        simbad_table[dec_name].description = 'Declination, DMS, ICRS at J2000 epoch'

        # add in floating point degrees
        dec_index = simbad_table.index_column(dec_name)
        ra_col = Column([ra_deg], 
            name='{}_deg'.format(ra_name), unit='deg',
            format='{:.6f}',
            description='Right ascension in decimal degrees')
        dec_col = Column([dec_deg], 
            name='{}_deg'.format(dec_name), unit='deg',
            format='{:.6f}',
            description='Declination in decimal degrees')
        col_list = [ra_col, dec_col]
        # insert after [dec_name]
        idx_list = [dec_index+1, dec_index+1]
        simbad_table.add_columns(col_list,
            indexes=idx_list,
            copy=True)
        return
    
    def add_user_ident(self, simbad_table):
        """Adds a column for the user-supplied ID to the table
        """
        user_col = Column([self.user_ident],
            name='Star', format='{}', dtype='U24',
            description='User-supplied star object ID')
        simbad_table.add_column(user_col, index=0)
        return
