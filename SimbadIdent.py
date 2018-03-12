#!/usr/bin/env python3
"""A simple web-scraper of stellar information using the Simbad service.

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

import os
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord

__author__ = "Dave Strickland"
__copyright__ = "Copyright 2018, Dave Strickland"
__date__ = "2018/02/23"
__deprecated__ = True
__email__ =  "dave.strickland@gmail.com"
__license__ = "GPLv3"
__version__ = "0.1"

class SimbadIdent:
    """Parses data associated with a Simbad Ident query
    
    Deprecated. Original developed before I noticed astroquery
    could do this. This method may be less resource intensive than
    using astroquery, and can work offline too (when the files have
    already been downloaded).
    """

    def __init__(self, user_ident, usecached=True):
        self.user_ident = user_ident
        self.rawfile = self.get_simbdad_id(self.user_ident, usecached)
        self.data = []
        self.identifiers = {}
        self.read_data(self.rawfile)
        self.parse_identifiers()
        self.parse_coordinates()
        self.parse_data()

    def __str__(self):
        # Limitation. This only works if the object is fully constructed.
        #return 'SimbadIdent: user_ident={}, datafile={}, Data={}'.format(self.user_ident, self.rawfile, self.data)
        return 'SimbadIdent: user_ident={}, datafile={}, coord={}, identifiers={}, pm={}, plx={}, spec_type={}, magB={}, magV={}'.format(self.user_ident, 
            self.rawfile,
            self.coord,
            self.identifiers,
            self.pm,
            self.plx,
            self.spec_type,
            self.magB,
            self.magV)

    def parse_coordinates(self):
        """Extracts ICRS coordinates, uncertainty (mas), and reference"""
        # This is handled slightly differently to parse_data because we
        # want to do some specialized processing on the coordinates using
        # astropy's SkyCoord class.
        self.coord = None
        val_indices = slice(1,7)
        err_indices = slice(10,13)
        ref_indices = 13
        for line in self.data:
            if 'Coordinates(ICRS' in line:
                tmp = line.split(' ')
                tmp = list(filter(bool, tmp)) # remove empty strings

                if (len(tmp) > 7):
                    coord_str = ' '.join(tmp[val_indices])
                    sc = SkyCoord(coord_str, unit=(u.hourangle, u.deg), frame='icrs')
                    ##vals = sc.to_string('hmsdms', precision=1)
                    # returns a list, so just get first element
                    ra_deg  = sc.ra.degree
                    dec_deg = sc.dec.degree
                    # sc.ra.to_string returns a list, so just get first element
                    ra_str  = sc.ra.to_string(u.hour, sep=':', precision=1)
                    dec_str = sc.dec.to_string(u.deg, sep=':', precision=1)
                else:
                    ra_deg = None
                    dec_deg = None
                    ra_str = None
                    dec_str = None

                # error measurements
                ##if (len(tmp) > 12):
                ##    errs = tmp[err_indices]
                ##    if isinstance(errs, list):
                ##        errs = ' '.join(errs).strip('[]') # get rid of simbad's []
                ##    else:
                ##        errs = errs.strip('[]')
                ##    # Catch some common cases where there really arent uncertainties known
                ##    if '~' in errs:
                ##        errs = None
                ##else:
                ##    errs = None

                # reference bibcode
                if (len(tmp) > 13):
                    refs = tmp[ref_indices]
                    if isinstance(refs, list):
                        refs = ' '.join(vals)
                    if '~' in refs:
                        refs = None
                else:
                    refs = None
                setattr(self, 'coord', {'ra_str': ra_str,
                    'dec_str': dec_str,
                    'ra_deg': ra_deg,
                    'dec_deg': dec_deg, 
                    'ref': refs})
                break
        return

    def parse_data(self):
        """Extracts data such as:
        - B, V magnitudes, 
        - proper motion, 
        - parallax
        - spectral type.
        Data values, errors and reference ADS bibcode are all extracted
        and stored in a dict.
        """
        # this is a brute force method that is slightly inefficient as
        # it repeatedly iterates over self.data, but it does get the job done with
        # minimum lines of code.
        self.data_name_dict = {'pm': 'Proper motions',
            'plx': 'Parallax',
            'spec_type': 'Spectral type',
            'magB': 'Flux B',
            'magV': 'Flux V'}
        self.val_indices = {'pm': slice(2,4),
            'plx': 1,
            'spec_type': 2,
            'magB': 3,
            'magV': 3}
        self.err_indices = {'pm': slice(4,6),
            'plx': 2,
            'spec_type': 3,
            'magB': 4,
            'magV': 4}
        self.ref_indices = {'pm': 8,
            'plx': 4,
            'spec_type': 4,
            'magB': 6,
            'magV': 6}
        self.float_conv = {'pm': False,
            'plx': True,
            'spec_type': False,
            'magB': True,
            'magV': True}
        self.col_name_dict = {'pm': 'pm',
            'plx': 'plx',
            'spec_type': 'spec_type',
            'magB': 'magB',
            'magV': 'magV'}
        self.measurement_units = {'pm': 'mas mas',
            'plx': 'mas',
            'spec_type': '',
            'magB': 'mag',
            'magV': 'mag'}
     
        for data_name in self.data_name_dict.keys():
            # set up default in case it doesn't exist
            setattr(self, data_name, {'val': None, 'err': None, 'ref': None}) 
            for line in self.data:
                # data_name_dict(data_name) is the search string
                search_string = self.data_name_dict[data_name]
                if search_string in line:
                    tmp = line.split(' ')
                    tmp = list(filter(bool, tmp)) # remove empty strings
                    vals = tmp[self.val_indices[data_name]]
                    errs = tmp[self.err_indices[data_name]]
                    refs = tmp[self.ref_indices[data_name]]
                    # create a string if we have a list, skip otherwise
                    if isinstance(vals, list):
                        vals = ' '.join(vals)
                    if '~' in vals:
                        vals = None

                    if isinstance(errs, list):
                        errs = ' '.join(errs).strip('[]') # get rid of simbad's []
                    else:
                        errs = errs.strip('[]')
                    if '~' in errs:
                        errs = None

                    if isinstance(refs, list):
                        refs = ' '.join(vals)
                    if '~' in refs:
                        refs = None

                    # floating point conversion?
                    if self.float_conv[data_name]:
                        if vals is not None:
                            vals = float(vals)
                        else:
                            vals = float('nan')
                        if errs is not None:
                            errs = float(errs)
                        else:
                            errs = float('nan')

                    #print(data_name, {'val': vals, 'err': errs, 'ref': refs})
                    setattr(self, data_name, {'val': vals, 'err': errs, 'ref': refs})
                    break
        return

    def parse_identifiers(self):
        """Parse the primary (Simbad) object identifier as well as 
        secondary identifiers of interest to us such as WDS, SAO, HD,
        and the common name.
        """
        # Get Simbad's own primary identifier
        obj_index = 5 # TODO do dynamically
        tmp = self.data[obj_index].replace('Object ','').split('---')
        simbad_ident = tmp[0].strip()
        self.identifiers['MAIN_ID'] = simbad_ident

        [l_start, l_end] = self.find_identifier_section()
        for identifier in ['WDS', 'SAO', 'HIP', 'NAME', 'HD']:
            identifier_found= False
            for i in range(l_start, l_end+1):
                line = self.data[i].strip()

                if identifier in line:
                    tmp = line.split(' ')
                    tmp = list(filter(bool, tmp)) # remove empty strings
                    idx = tmp.index(identifier)
                    self.identifiers[identifier] = tmp[idx+1]
                    identifier_found = True
                    break # break out of line loop
            if not identifier_found:
                self.identifiers[identifier] = None

        # parse secondary identifiers we're interested in.
        return

    def get_astropy_table_defn(self):
        """Returns column name, dtype and units lists for the data in this
        object that can be used to define an astropy Table object to
        store the data returned by get_astropy_table_row().
        """
        # unfortunately we can't make this truly self describing.
        ##col_names  = ['user_ident']
        ##col_dtypes = ['U16']
        ##col_units  = ['']
        for key in self.identifiers:
            col_names.append(key)
            col_dtypes.append('U20')
            col_units.append('')
        # for the following we have the value, error and reference to store.
        col_names.append('RA_icrs')
        col_names.append('DEC_icrs')
        col_names.append('RA_icrs_deg')
        col_names.append('DEC_icrs_deg')
        col_names.append('RADEC_bibcode')
        col_dtypes.append('U13') # ra
        col_dtypes.append('U13') # dec
        col_dtypes.append(np.float64) # ra
        col_dtypes.append(np.float64) # dec
        col_dtypes.append('U24') # ref
        col_units.append('h:m:s')
        col_units.append('d:m:s')
        col_units.append('deg')
        col_units.append('deg')
        col_units.append('bibcode')

        for data_name in self.data_name_dict.keys():
            vname = self.col_name_dict[data_name]
            ename = 'e_{}'.format(vname)
            rname = 'ref_{}'.format(vname)

            col_names.append(vname)
            col_names.append(ename)
            col_names.append(rname)
            if self.float_conv[data_name]:
                col_dtypes.append(np.double) # val
                col_dtypes.append(np.double) # err
            else:
                col_dtypes.append('U16') # val
                col_dtypes.append('U16') # err
            col_dtypes.append('U24') # ref
        
            col_units.append(self.measurement_units[data_name])
            col_units.append(self.measurement_units[data_name])
            col_units.append('bibcode')

        return [col_names, col_dtypes, col_units]

    def get_astropy_table_row(self):
        """Returns the data stored in this object as a list in the
        same format as given by get_astropy_table_defn. This list
        can be used to add a row to an astropy Table object using its
        add_row() method.
        """
        p_list = [self.user_ident]
        for key in self.identifiers:
            p_list.append(self.identifiers[key])
        p_list.append(self.coord['ra_str'])
        p_list.append(self.coord['dec_str'])
        p_list.append(self.coord['ra_deg'])
        p_list.append(self.coord['dec_deg'])
        p_list.append(self.coord['ref'])
        for data_name in self.data_name_dict.keys():
            data_dict = getattr(self, data_name)
            p_list.append(data_dict['val'])
            p_list.append(data_dict['err'])
            p_list.append(data_dict['ref'])
        return p_list

    def get_simbdad_id(self, aSimbadIdentifier, usecached=True):
        """Query Simbad by Identifier, storing the output as a file in
        subdirectory Simbad.
        
        If usecached is True, then don't perform the internet query if we
        have the file on disk already.
        """
        import os
        import urllib
        import pathlib
        import time
    
        # store files in subdirectory of current dir
        odir = 'Simbad'
        if not os.path.isdir(odir):    
            pathlib.Path(odir).mkdir(parents=True, exist_ok=True)
            print('Created {} to store Simbad data in'.format(odir))
    
        ofile = '{}/{}.simbad_id'.format(odir, aSimbadIdentifier.replace(' ', '_'))
        ofile_exists = os.path.isfile(ofile)
        if ofile_exists and usecached:
            print('  For "{}" using cached file {}'.format(aSimbadIdentifier, ofile))
        else:
            print('  Querying Simbad for "{}"'.format(aSimbadIdentifier))
            time.sleep(1.5) # to avoid hammering Simbad with many queries.
            # Have to replace spaces with %20
            simbad_url = 'http://simbad.u-strasbg.fr/simbad/sim-id?output.format=ASCII&Ident={}&obj.bibsel=off&obj.messel=off&obj.notesel=off'.format(aSimbadIdentifier.replace(' ', '%20'))
            try:
                response = urllib.request.urlopen(simbad_url, timeout = 5)
                content = response.read()
                f = open(ofile, 'wb')
                f.write(content)
                f.close()
            except urllib.error.URLError as e:
                print('  Error querying Simbad: ',type(e))
                print('    Original URL used: {}'.format(simbad_url))
                ofile = None
        return ofile


    def find_identifier_section(self):
        l_start = None
        l_end = None
        for (i, line) in enumerate(self.data):
            if 'Identifiers' in line:
                l_start = i + 1
            if '====================' in line:
                l_end = i
        return [l_start, l_end]

    def read_data(self, datafile):
        if os.path.isfile(datafile):
            with open(datafile, 'r') as f:
                self.data = f.readlines()
        else:
            raise ValueError('Cannot find file {}'.format(datafile))
        # strip off returns in lines
        # Note: This is a inplace operation, and also avoids the
        # need for map or lambda.
        for idx, line in enumerate(self.data):
            self.data[idx] = line.strip()
        return

