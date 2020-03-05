# DoubleStars Version 0.2.alpha README

Extracts the latest astronomical information for a list 
of stellar objects, in particular double/multiple stellar systems.

## Introduction

These are a collection of python scripts to extract the latest 
astronomical information available for a list of stellar objects
that is input either by HTML table, or a simple text file. 

My purpose in writing them was to get the best, or better, information 
on interesting stars listed in amateur astromical articles (such as
[this article](http://www.skyandtelescope.com/observing/colored-double-stars-real-and-imagined/) 
or [this article](http://www.skyandtelescope.com/observing/celestial-objects-to-watch/pretty-double-stars-for-everyone/)). 
These articles often have lists of interesting objects, but the coordinates
and/or names can be lacking sufficient information needed to use with 
computer-guided amateur telescopes, or to look up other information 
easily on the web.

Information is extracted from [Simbad](http://simbad.u-strasbg.fr/simbad/)
Astronomical Database and written to HTML and fits-format tables using 
[astropy](http://www.astropy.org/) under the hood. Note that these
scripts are **written for Python 3 only!** If you're still using 
Python 2 please upgrade!

The scripts available so far are only a start at getting the physical 
information I'm really interested in, i.e. true luminosity, mass,
stellar radius, separation and distance of binary or multiple star 
systems. The code to do that will be added at a later date.

The basic work flow is:
1. Get a text format or HTML table format list of interesting objects.
   The only required information is a column of names or identifiers
   that we can pass to Simbad. (Lets call this data "level 0".)
2. Run `star_query.py` on that input to get first guess at recognized
   Simbad identifiers for those targets, in particular WDS 
   (Washington Double Star) and HIP (Hipparcos Output Catalog) IDs.
   This will also get basic observable data such as positions,
   parallaxes, proper motions, spectral types and B and V-band
   magnitudes.
   We'll call the output fits table from this stage "level 1".
   If you're just running it to get information on some arbitrary stars
   without an interest in known double/multiple star systems then you
   can skip ahead to step 5.
3. Run `process_wds_ids.py` on the level 1 data to get Simbad ID's
   for the primary, secondary, etc, components of the multiple star
   systems. (Only needed when you're interested in double/multiple star
   systems.)
4. Re-run `star_query.py` on the outut of step #3, using 
   the new, more specific, IDs to get the observable
   data for all selected multiple star components. We'll call this
   "level 2". (Only needed when you're interested in double/multiple star
   systems.)
5. *(Not yet implemented)* Process the level 2 data to derive physical
   properties of the stars, e.g. distance, instrinsic luminosity, 
   temperature, radius, and maybe ZAMs mass and lifetime, along with
   the physical separation of the binary/multiple star components.
   
A short series of blog posts discuss running these tools on Bob 
King's "Colored Doubles":
- [Colorful binary star systems for small telescopes: Part 1](https://superwinds.blogspot.com/2018/03/colorful-binary-star-systems-for-small.html)
- [Colorful binary star systems for small telescopes: Part 2](https://superwinds.blogspot.com/2018/07/colorful-binary-star-systems-for-small.html) 
 
   
### Script Overview

The following subsections provide an overview of the scripts. More detailed
usage information is provided in the [EXAMPLES.md](examples/EXAMPLES.md) 
document.

#### star_query.py

Given an input HTML table, FITS table, or text file containing
a set of stellar names (either common names or catalog IDs), 
`star_query.py` can be run to produce HTML and gzipped 
[fits](https://en.wikipedia.org/wiki/FITS)-format
output tables that contain the following information:

|     Name        | In HTML?| unit     |               Description |              
| --- | --- | ---  | --- |
|            Star | yes     |          |             User-supplied star object ID |
|        SimbadID | yes     |          |                   Main ID used by Simbad |
|             WDS | yes     |          |        Washington Double Star Catalog ID |
|             SAO | yes     |          |                      SAO Star Catalog ID |
|             HIP | yes     |          |              Hipparcos Output Catalog ID |
|            NAME | yes     |          |                              Common name |
|              HD | yes     |          |                  Henry Draper Catalog ID |
|         RA_icrs | yes     | hrs:min:sec | Right ascension, HMS, ICRS at J2000 epoch |
|        DEC_icrs | yes     | deg:min:sec |    Declination, DMS, ICRS at J2000 epoch |
|     RA_icrs_deg | no      |     deg  |       Right ascension in decimal degrees |
|    DEC_icrs_deg | no      |     deg  |           Declination in decimal degrees |
|   RADEC_bibcode | no      |          |                  Bibcode for coordinates |
|            magB | no      |     mag  |                V-band apparent magnitude |
|        magB_err | no      |          | Uncertainty in B-band apparent magnitude |
|    magB_bibcode | no      |          |    Bibcode for B-band apparent magnitude |
|            magV | yes     |     mag  |                V-band apparent magnitude |
|        magV_err | no      |          | Uncertainty in V-band apparent magnitude |
|    magV_bibcode | no      |          |    Bibcode for V-band apparent magnitude |
|        parallax | no      |     mas  |                                 parallax |
|    parallax_err | no      |     mas  |                             parallax_err |
|parallax_bibcode | no      |          |                     Bibcode for parallax |
|           pm_RA | no      | mas / yr |                      Proper motion in RA |
|          pm_DEC | no      | mas / yr |                     Proper motion in DEC |
|     pm_err_maja | no      | mas / yr |           Proper motion error major axis |
|     pm_err_mina | no      | mas / yr |           Proper motion error minor axis |
|    pm_err_angle | no      | deg      |                Proper motion error angle |
|      pm_bibcode | no      |          |                Bibcode for proper motion |
|       spec_type | yes     |          | Spectral type including luminosity class |
|       spec_qual | no      |          |                    Spectral type quality |
|    spec_bibcode | no      |          |                Bibcode for spectral type |
|     Teff_(Fe_H) | yes     | degK     |            Effective temperature in K |
|       \[Fe/H\]  | yes     |          |   Metal abundance relative to Sun in dex |
|    Fe_H_bibcode | no      |          |     Bibcode for metal abundance and Teff |

All data items are written thhe gzipped fits table. Although some items are 
left out of the HTML output by default they can be included using the 
`--fullhtml` command line flag.

### process_wds_ids.py

Extracts a clean list of Washington Double Star (WDS) IDs from the initial FITS-dormat output
of star_query.py. The script then combines that with the information on all listed
(likely and unlikely) companions from the main WDS data file to generate a 
list of likely stellar companions using one of several different filtering
methods.

The output table produced by `process_wds_ids.py` can then be fed back into
`star_query.py` as input along with the `--stage2` command line flag.

A separate bash script, `download_data.sh`, should be used before running `process_wds_ids.py`.
The bash script will download the main WDS data table needed by process_wds_ids.py`
from CDS. (It also uses `fitsmodhead.py` to fix a FITS header keyword 
problem in the WDS data table that would otherwise prevent astropy.io.fits from
reading the WDS data.)

## Inputs

Along with the code this project comes with four example input files:
- `bob_king_colored_double_stars.html` from [Colored Double Stars, Real
   and Imagined by Bob King, Sky & Telescope, December 14 2016](http://www.skyandtelescope.com/observing/colored-double-stars-real-and-imagined/).
- `alan_adler_pretty_double_stars.html` from [Pretty Double Stars for Everyone, by Alan Adler, Sky & Telescope, July 26 2006](http://www.skyandtelescope.com/observing/celestial-objects-to-watch/pretty-double-stars-for-ever/).
- `brightest_m_dwarfs.html` from [14 Red Dwarf Stars to View from Backyard Telescopes, by David Dickinson, Universe Today, 13 May 2014](https://www.universetoday.com/111716/14-red-dwarf-stars-to-view-with-backyard-telescopes/).
- `alternate_input.txt` is an example of the simple text file input format.

### Using This Code With Your Own Inputs

However most users will want to use it will their own inputs. The simplest
way of doing this, for a small list of objects, is to create a simple 
ascii (or utf-8) CSV file following the format shown in `alternate_input.txt`.
The CSV file column containing the object names/ID can be called anything 
and in any position within the file. However if its not called `Star` then
you must pass the name to `star_query.py` using the `-c` or `--col` command
line argument.

If you wish to use a longer list of object that is already formatted as
a HTML table within a web page then follow these steps.
- Open the web page containing the HTML table in your browser.
- Right click on the page and select "View page source".
- Scroll down in the new window that opens, select the HTML table 
  containing the objects, and right click again to select "copy".
- Open a text editor and paste the HTML table into it, then select
  "save as" and save it with `.html` extension. 
- Make a note of the
  table column name for the stars names/IDs, as you need to
  use it with `--col` if it isn't the default `Star` expected by 
  `star_query.py`.
- You will *almost certainly* need to hand edit the HTML formatting of
  the table before `star_query.py` will sucessfully use it, because
  astropy expects the table to stritly follow the table syntax and
  to not be too complex.
- In particular, there must be one table row of column headings, i.e.,
  the first table row (`<tr> ... </tr>`) must have columns that are
  in `<th> ... </th>` format.
- Spanning multiple columns with `colspan` confuses astropy. You'll 
  have to either remove columns or add new columns to get the table
  to work.
- Rows with either multiple names (e.g. "AX Microscopii/Lacaille 8760") or no names (assumed to be
  continuations of the previous row?) will almost certainly not
  work. Use your judgement to deal with them, but you may have to
  comment them out or delete them.

### Unrecognized Inputs

Simbad may not recognize a user-supplied identifier. Identifiers used
in an amateur astronomical community may not correspond to the catalog
naming conventions used by Simbad (.e.g "h3945 CMa", 
or they may be from a catalog/source not recognized by Simbad at all 
(e.g. "Struve"). In some cases Simbad recognizes the identifier but
returns multiple possible matches, or in rare cases accepts the
identifier but returns no data. In any case, `star_query.py` will tell
you which identifiers it had trouble with when it runs.

There are various ways to find identifiers that Simbad will recognize:
- Perform an [object ID query at Simbad](http://simbad.u-strasbg.fr/simbad/sim-fid) youself and see what it
  returns. If it returns two or more possible matches you can select
  which one best matches your intended target (based on position and
  magnitude, for example).
- If the basic query returns nothing then you may be forced to perform
  a [Simbad coordinate query](http://simbad.u-strasbg.fr/simbad/sim-fcoo),
  if you have some idea of the Right Ascension (RA) and Declination 
  (Dec) of the target. Note that amateur astronomical articles 
  often only provide RA as hours and minutes, and Dec as degrees and
  arcminutes, leaving out the seconds and arcseconds and rounding
  off to the minutes/arcminutes. So to get a match so you will have
  to search all targets within a radius of your input. Simbad does
  this by default for coordinate queries, but the default search radius of
  2 arcminutes may be a bit small and probably should be increased to
  10 arcmin.

Once you have the "correct" IDs you can add them to 
`simbad_star_alias.csv`, following the format of the entries already
present in that file. Or create your own alias file and pass that
into `star_query.py` with the `--aliases` command line option.

## License and Dependencies

### Software License

This code is made available under the GNU General Public License, version 3.
See LICENSE for details.

### Operating Systems and Dependencies

This code has been developed on Linux, specifically Fedora versions 27 
to 31, but has also been run successfully on Mac OS X 10.11 El Capitan
using macports.

On Fedora you will need to have the following packages installed:

`python3 python3-astropy python3-astroquery python3-numpy`

The specific versions I'm using are:
```
python3.x86_64                       3.6.4-7.fc27              @updates
python3-astropy.x86_64               2.0.2-1.fc27              @fedora 
python3-astroquery.noarch            0.3.6-2.fc27              @fedora 
python3-numpy.x86_64                 1:1.13.3-4.fc27           @updates
```

Installing these packages, or having them already installed, 
should satisfy any other dependencies.

On a different Linux distribution, or on OSX using macports,
installing a similar set of dependencies should get it working.

## Usage

Each of the command line python programs use argparse, so you can the
`--help` command line option to get a full list of the arguments
each accepts.

## Examples

A set of examples with commentary is provided in 
[examples/EXAMPLES.md](examples/EXAMPLES.md).


## Other Useful Info

- Various sites, including [babelstone](http://www.babelstone.co.uk/Unicode/whatisit.html), 
  can be used to identify mysterious unicode characters in input
  HTML tables that Simbad may not be able to resolve.
- [Divtable's table styler](http://divtable.com/table-styler/) can 
  be used to generate alternate CSS styles for the HTML tables.
- [fv](https://heasarc.gsfc.nasa.gov/ftools/fv/) can be used to view and edit fits files. (Note that it refuses to
  modify gzipped fits files even though it reads them, so gunzip them
  if you want to edit a gzipped fits file.)
- The reference [Bibcodes](https://en.wikipedia.org/wiki/Bibcode) 
  can be looked up using [NASA ADS](http://www.adsabs.harvard.edu/), 
  which in many cases can get you access to a free scanned version of the
  article or a freely accessible PDF or HTML version of it (at least
  for articles from major journals that are over a year old).
  
