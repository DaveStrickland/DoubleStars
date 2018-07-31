#!/usr/bin/env python3
"""Read and use Washington Double Star data from Vizier

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

from astropy.table import Table, Column, Row, vstack
import DavesAstropyUtils as dapu

__author__     = "Dave Strickland"
__copyright__  = "Copyright 2018, Dave Strickland"
__date__       = "2018/03/22"
__deprecated__ = False
__email__      = "dave.strickland@gmail.com"
__license__    = "GPLv3"
__version__    = "0.2.0"

class WDS:
    """Utility to access data from the Washington Double Star
    catalog
    """
    def __init__(self, wds_data_file, max_mag_diff, verbose):
        self.wds_data_file = wds_data_file
        self.max_mag_diff = float(max_mag_diff)
        self.verbose = verbose
        self.wdsdata = dapu.read_table(self.wds_data_file, verbose)
        self.clean()
        self.wdsdata.add_index('WDS')
        return
        
    def clean(self):
        """Removes table columns we're not likely to need"""
        cols_to_clean = ['Disc', 'Obs1', 'Nobs', 'pa1', 'sep1',
            'pmRA1', 'pmDE1', 'pmRA2', 'pmDE2', 'DM', 
            'n_RAh', 'RAh', 'RAm', 'RAs',
            'DE-', 'DEd', 'DEm', 'DEs'];
        self.wdsdata.remove_columns(cols_to_clean)
        if self.verbose:
            print('Remaining table columns:')
            print(self.wdsdata.info)
        return

    def get_likely_components(self, wds_id, filter_mode=None):
        """Performs a set of filtering operations on the
        list of possible stellar components.

        The filtering applied depends on the filtering mode.

        'abs' selects only A, B and C components, irrespective
        of whether they are physically likely companions or not.
         - select_abc

        'positive' selects only those components likely to be
        members of the same system, irrespective of how easy
        they are to observe
        - select_physical

        'negative' is used to filter out components thought not
        to be physical, or too difficult to observe as an
        amateur astronomer given a large magnitude difference:
        - prune_spectroscopic_binaries
        - prune_unphysical
        - prune_magnitude
        """

        if filter_mode is None:
            filter_mode = 'negative'

        self.current_id = wds_id
        self.current_data = None
        self.current_data = self.wdsdata.loc[wds_id]
        
        # If there is only a single row astropy returns a Row object
        # instead of a Table. As other logic depends on Table format
        # we convert these Rows into single row Tables
        if isinstance(self.current_data, Row):
            tmp_table = Table(rows=self.current_data, copy=True, copy_indices=False)
            self.current_data = tmp_table

        # This is necessary for string comparisons to table objects
        # and the sort syntax to work.
        self.current_data.convert_bytestring_to_unicode()

        # Sort to get components in the sort of order we expect
        self.current_data.sort('Comp')
            
        if 'negative' in filter_mode:
            self.prune_spectroscopic_binaries()
            self.prune_unphysical()
            self.prune_mag_diff()
        elif 'positive' in filter_mode:
            self.select_physical()
        elif 'abc' in filter_mode:
            self.select_abc()
        else:
            print('Error: For {} unexpected filter_mode={} specified.'.format(wds_id, 
                filter_mode))

        ids_list = self.make_wds_id_list()
        return self.current_data, ids_list

    def make_wds_id_list(self):
        """Convert remaining WDS components back into Simbad
        compatible WDS IDs.
        
        The logic is relatively complex and is described within
        the function body itself.
        """
        if self.current_data is None:
            ids_list = None
            return ids_list
        num_comp = len(self.current_data)
        if num_comp > 0:
            ids_list = []
            for idx in range(num_comp):
                comp = self.current_data['Comp'][idx].strip()
                if len(comp) == 0:
                    # WDs seems not to state component names if there
                    # aren't more than two, so AB is implied in such cases.
                    comp='AB'
                    
                if 'a,' in comp:
                    # If there is a lower case a, e.g. Aa,Ab then
                    # Simbad will expect that entire string.
                    ids_list.append(comp)
                elif ',' in comp:
                    # Cases like 'A,BC' seem to handled by Simbad
                    # with a separate A and a separate BC component,
                    # i.e. no separate B and C components.
                    ids_list.extend( comp.split(',') )
                else:
                    # Cases like AB or BC, we need to split every
                    # character
                    for char in comp:
                        ids_list.append(char)
                
            # Now remove duplicates and sort...
            ids_list = list(sorted(set(ids_list)))
        else:
            ids_list = None
            return ids_list
            
        # Convert back into Simbad form by adding in the J<wds_id> parts
        simbad_ids_list = []
        for comp in ids_list:
            simbad_ids_list.append( ''.join(['J', self.current_id, comp]) )
        return simbad_ids_list

    def select_abc(self):
        """A simplistic filter that only selects the A, B and C
        components (if present) of any WDS system.
        
        This filter doesn't apply any physical criteria, rather
        it exists to select the first few components that may
        be part of a multiple system. This may correspond more
        closely to common, purely visual, selection of close
        double or triples than the 'negative'
        filter implemented elsewhere in this class.
        """
        if self.current_data is None:
            return
        if len(self.current_data) == 0:
            self.current_data = None
            return
        row_list = []
        for idx in range(len(self.current_data)):
            comp = self.current_data['Comp'][idx].strip()
            if len(comp) == 0:
                # WDs seems not to state component names if there
                # aren't more than two, so AB is implied in such cases.
                comp='AB'

            if 'AB' in comp:
                continue
            elif 'Aa' in comp:
                # spectroscopic binary components
                continue
            elif 'AC' in comp:
                continue
            elif 'BC' in comp:
                continue
            else:
                # remove to component
                row_list.append(idx)

        num_spec = len(row_list)
        if num_spec > 0:
            if self.verbose:
                print('    For {} removed {} non-ABC components'.format(self.current_id,
                    num_spec))
            self.current_data.remove_rows(row_list)
        if len(self.current_data) == 0:
            self.current_data = None
        return

    def select_physical(self):
        """Use WDS 'Notes' strings to select only those objects likely to
        be physically part of the same stellar system.
        
        Select components with determined orbits, or statistically 
        similar parallax and/or proper motions. These correspond 
        to the WDS 'Note' column entries 'C', 'O', 'T', 'V' or 'Z'.
        """
        if self.current_data is None:
            return
        if len(self.current_data) == 0:
            self.current_data = None
            return
        row_list = []
        for idx in range(len(self.current_data)):
            note_str = self.current_data['Notes'][idx]
            if 'C' in note_str:
                continue
            elif 'O' in note_str:
                continue
            elif 'T' in note_str:
                continue
            elif 'V' in note_str:
                continue
            elif 'Z' in note_str:
                continue
            else:
                # If we get here then we dont match any of the positive
                # criteria, so add this row to the list to remove
                row_list.append(idx)

        num_spec = len(row_list)
        if num_spec > 0:
            if self.verbose:
                print('    For {} removed {} non-definite components'.format(self.current_id,
                    num_spec))
            self.current_data.remove_rows(row_list)
        if len(self.current_data) == 0:
            self.current_data = None
        return


    def prune_unphysical(self):
        """Use WDS 'Notes' strings to remove objects likely not to
        be physically part of the same stellar system.
        
        Remove components with statistically different parallax
        and/or proper motions, or otherwise noted in the WDS as
        being of dubious validity. These correspond to the WDS 'Note'
        column entries 'S', 'U', 'X', and 'Y'
        """
        if self.current_data is None:
            return
        if len(self.current_data) == 0:
            self.current_data = None
            return
        row_list = []
        for idx in range(len(self.current_data)):
            note_str = self.current_data['Notes'][idx]
            if 'S' in note_str:
                # S = statistically different parallax and proper motions
                row_list.append(idx)
            elif 'U' in note_str:
                # U = proper motion indicates non-physical
                row_list.append(idx)
            elif 'X' in note_str:
                # X = something else indicating unlikely to be physical
                row_list.append(idx)
            elif 'Y' in note_str:
                # Y = statistically different parallax
                row_list.append(idx)
        num_spec = len(row_list)
        if num_spec > 0:
            if self.verbose:
                print('    For {} pruning {} unlikely components'.format(self.current_id,
                    num_spec))
            self.current_data.remove_rows(row_list)
        return

    def prune_spectroscopic_binaries(self):
        """Use 'Comp' strings to remove spectroscopic binary components
        """
        if self.current_data is None:
            return
        if len(self.current_data) == 0:
            self.current_data = None
            return
        row_list = []
        for idx in range(len(self.current_data)):
            # Look for entries with lower case compents  with commas
            if 'a,' in self.current_data['Comp'][idx]:
                row_list.append(idx)
        num_spec = len(row_list)
        if num_spec > 0:
            if self.verbose:
                print('    For {} pruning {} spectroscopic binaries'.format(self.current_id,
                    num_spec))
            self.current_data.remove_rows(row_list)
        return

    def prune_mag_diff(self):
        """Prune out components where the magnitude difference
        listed in the WDS data is greater than the configured
        maximum magnitude difference.

        This filter is useful for amateur astronomical use where
        very faint companions may be difficult to see and uninteresting
        from an observing stand point.
        """
        if self.current_data is None:
            return
        if len(self.current_data) == 0:
            self.current_data = None
            return
        row_list = []
        for idx in range(len(self.current_data)):
            mag1 = float(self.current_data['mag1'][idx])
            mag2 = float(self.current_data['mag2'][idx])
            dm = mag2 - mag1
            if dm > self.max_mag_diff:
                row_list.append(idx)
        num_spec = len(row_list)
        if num_spec > 0:
            if self.verbose:
                print('    For {} pruning {} components with mag2-mag1>{} mag'.format(self.current_id,
                    num_spec, self.max_mag_diff))
            self.current_data.remove_rows(row_list)
        return


def wds_id_from_simbad_wds(simbad_wds):
    """Extracts the main WDS ID from a Simbad WDS ID.

    This function exists to facilitate access to the official
    Washington Double Star catalog using IDs returned by Simbad.

    This function attempts to extract an WDS ID, for example
    '14396-6050', from the WDS IDs returned by Simbad, for example 'J14396-6050C'.
    In short, it checks the length and strips off the leading
    'J' and trailing component 'xx' etc.

    If a valid ID cannot be returned then None is returned.
    """
    p_owds = None
    if simbad_wds is not None:
        if not 'None' in simbad_wds:
            # Rather than use a regex we rely on Simbad's constancy
            # to extract the 5 ra digits, sign, and 4 dec digits
            if len(simbad_wds) >= 11: 
                p_owds = simbad_wds[1:11]
    return p_owds
