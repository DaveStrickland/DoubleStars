# DoubleStars README

Extracts the latest astronomical information for a list 
of stellar objects, in particular double stars.

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
0. Get a text format or HTML table format list of interesting objects.
   The only required information is a column of names or identifiers
   that we can pass to Simbad. (Lets call this data "level 0".)
1. Run `star_query.py` on that input to get first guess at recognized
   Simbad identifiers for those targets, in particular WDS 
   (Washington Double Star) and HIP (Hipparcos Output Catalog) IDs.
   This will also get basic observable data such as positions,
   parallaxes, proper motions, spectral types and B and V-band
   magnitudes.
   (We'll call the output fits table from this stage "level 1").
2. *(Not yet implemented)* Process the level 1 data to get Simbad ID's
   for the primary, secondary, etc, components of the multiple star
   systems.
3. *(Not yet implemented)* Query Simbad with these new, more specific, IDs to get the observable
   data for all selected multiple star components. (We'll call this
   "level 2".)
4. *(Not yet implemented)* Process the level 2 data to derive physical
   properties of the stars, e.g. distance, instrinsic luminosity, 
   temperature, radius, and maybe ZAMs mass and lifetime, along with
   the physical separation of the binary/multiple star components.
   
### star_query.py

Given an input HTML table or text file containing
a set of stellar names (either common names or catalog IDs), 
`star_query.py` can be run to produce HTML and gzipped 
[fits](https://en.wikipedia.org/wiki/FITS)-format
output tables that contain the following information:

     Name        | In HTML?| unit     |               Description               
---------------- |-------- |--------  | ---------------------------------------
            Star | yes     |          |             User-supplied star object ID
        SimbadID | yes     |          |                   Main ID used by Simbad
             WDS | yes     |          |        Washington Double Star Catalog ID
             SAO | yes     |          |                      SAO Star Catalog ID
             HIP | yes     |          |              Hipparcos Output Catalog ID
            NAME | yes     |          |                              Common name
              HD | yes     |          |                  Henry Draper Catalog ID
         RA_icrs | yes     | "h:m:s"  |Right ascension, HMS, ICRS at J2000 epoch
        DEC_icrs | yes     | "d:m:s"  |    Declination, DMS, ICRS at J2000 epoch
     RA_icrs_deg | no      |     deg  |       Right ascension in decimal degrees
    DEC_icrs_deg | no      |     deg  |           Declination in decimal degrees
   RADEC_bibcode | no      |          |                  Bibcode for coordinates
            magB | no      |     mag  |                V-band apparent magnitude
        magB_err | no      |          | Uncertainty in B-band apparent magnitude
    magB_bibcode | no      |          |    Bibcode for B-band apparent magnitude
            magV | yes     |     mag  |                V-band apparent magnitude
        magV_err | no      |          | Uncertainty in V-band apparent magnitude
    magV_bibcode | no      |          |    Bibcode for V-band apparent magnitude
        parallax | no      |     mas  |                                 parallax
    parallax_err | no      |     mas  |                             parallax_err
parallax_bibcode | no      |          |                     Bibcode for parallax
           pm_RA | no      | mas / yr |                       Proper motion in RA
          pm_DEC | no      | mas / yr |                      Proper motion in DEC
     pm_err_maja | no      | mas / yr |            Proper motion error major axis
     pm_err_mina | no      | mas / yr |            Proper motion error minor axis
    pm_err_angle | no      | deg      |            Proper motion error angle
      pm_bibcode | no      |          |                Bibcode for proper motion
       spec_type | yes     |          | Spectral type including luminosity class
       spec_qual | no      |          |                    Spectral type quality
    spec_bibcode | no      |          |                Bibcode for spectral type
     Teff_(Fe_H) | yes     | degK     |            Effective temperature in K
       \[Fe/H\]  | yes     |          |   Metal abundance relative to Sun in dex
    Fe_H_bibcode | no      |          |     Bibcode for metal abundance and Teff

All data items are written thhe gzipped fits table. Although some items are 
left out of the HTML output by default they can be included using the `--fullhtml` command line flag.


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

This code has been developed on Linux, specifically Fedora 27, but has
also been run successfully on Mac OS X 10.11 El Capitan using macports.

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

Run `star_query.py` with `-h` or `--help` to get the command line usage.
Example input files are provided as part of this package.

```
[dks@ithaqua DoubleStars]$ python3 star_query.py --help
usage: star_query.py [-h] [-p pretty_input_version.html] [-c name]
                     [--fullhtml] [--css table_style.css]
                     [--aliases ALIASES.csv] [-v]
                     input_file_or_txt output_summary.html output.fits.gz

positional arguments:
  input_file_or_txt     Input HTML table or ASCII TXT file of stars to be
                        processed.
  output_summary.html   Name for output HTML summary of processed data.
  output.fits.gz        name for output processed data table (fits format).

optional arguments:
  -h, --help            show this help message and exit
  -p pretty_input_version.html, --pretty pretty_input_version.html
                        Optional outputted "pretty" version of input HTML
                        table that uses the CSS table style for output HTML
  -c name, --col name   Name of table column containg star name/identifier
                        (default: Star)
  --fullhtml            Output all data fields used for the fits output to the
                        summary HTML file. By default bibcode, errors,
                        parallax and proper motion are excluded from the
                        summary HTML.
  --css table_style.css
                        CSS table style for output HTML (default:
                        darkTable.css)
  --aliases ALIASES.csv
                        CSV file containing mapping between user-supplied star
                        names and names acceptable to Simbad (default:
                        simbad_star_alias.csv)
  -v, --verbose         Verbose output for each object processed. Useful for
                        debugging purposes.
```

An example of running the code using a list of stars from [Bob King's
article on colored Double stars](http://www.skyandtelescope.com/observing/colored-double-stars-real-and-imagined/) 
follows. This was run in verbose mode to get it to output the list of
information collected on each object. (**Note** that this full set of
information is always written to the output fits-format table, but that
a smaller selection of the data is written to the output HTML table
**unless** `--fullhtml` is selected.)

```
[dks@ithaqua DoubleStars]$ python3 star_query.py bob_king_colored_double_stars.html king_processed_summary.html king_processed.fits.gz --pretty pretty_king_input.html --verbose
Using 15-element star alias dictionary from simbad_star_alias.csv
Input HTML or TXT file: bob_king_colored_double_stars.html
Output pretty HTML version of input file: pretty_king_input.html
Output processed data table (FITS): king_processed.fits.gz
Output summary of processed data (HTML): king_processed_summary.html
Wrote formatted table to pretty_king_input.html using CSS style darkTable
About to process 22 stars from bob_king_colored_double_stars.html
Using astroquery for data retrieval.
Processing eta Cas
Processing 1 Ari
Processing gamma And
Processing iota Tri = 6 Tri
Processing eta Per
Processing 32 Eri
Processing rho Ori
Processing 14 Aur
  Warning: For identifier=HD multiple responses found: ['33959', '33959A']
    Choosing 33959
Processing iota Ori
  Warning: For identifier=WDS multiple responses found: ['J05354-0555A', 'J05354-0555Aa,Ab']
    Choosing J05354-0555A
Processing gamma Lep
Processing h3945 CMa
Processing iota Cnc
Processing 24 Com
Processing xi Boo
Processing alpha Her
Processing 95 Her
Processing zeta Lyr
Processing Albireo
  Warning: For identifier=WDS multiple responses found: ['J19307+2758A', 'J19307+2758Aa,Ac']
    Choosing J19307+2758A
  Warning: For identifier=NAME multiple responses found: ['Albereo', 'Albireo']
    Choosing Albereo
Processing 31 Cyg
Processing beta Cap
Processing gamma Del
Processing delta Cep
      Star         SimbadID        WDS         SAO    HIP   ...     spec_bibcode    Teff_(Fe_H) [Fe/H]     Fe_H_bibcode   
                                                            ...                      unit-degK                            
---------------- ----------- ---------------- ------ ------ ... ------------------- ----------- ------ -------------------
         eta Cas   * eta Cas    J00491+5749AB  21732   3821 ... 1989ApJS...71..245K        5899  -0.31 2016A&A...587A...2B
           1 Ari   *   1 Ari    J01501+2217AB  74966   8544 ... 1985ApJS...59...95A           0   0.00                    
       gamma And   * gam And  J02039+4220A,BC   None   9640 ... 2013yCat....1.2023S           0   0.00                    
iota Tri = 6 Tri   * iot Tri    J02124+3018AB  55347  10280 ... 1969AJ.....74..916H           0   0.00 2008AJ....135..209M
         eta Per   * eta Per     J02507+5554A  23655  13268 ... 1989ApJS...71..245K        3500   0.09 1998A&A...338..623M
          32 Eri   *  32 Eri    J03543-0257AB   None  18255 ... 2008ApJS..176..216A           0   0.00                    
         rho Ori   * rho Ori    J05133+0252AB 112528  24331 ... 1989ApJS...71..245K        4599   0.22 2007AJ....133.2464L
          14 Aur   *  14 Aur     J05154+3241A  57799  24504 ... 1984ApJ...276..266A        7670   0.00 1991A&A...249..205B
        iota Ori   * iot Ori     J05354-0555A 132323  26241 ... 2011ApJS..193...24S       18000   0.10 1970A&A.....8..197C
       gamma Lep   * gam Lep     J05445-2227A 170759  27072 ... 2008ApJS..176..216A        6306  -0.12 2016A&A...587A...2B
       h3945 CMa   * 145 CMa     J07166-2319A 173349  35210 ... 1989ApJS...71..245K        3970   0.03 2014AJ....147..137L
        iota Cnc   * iot Cnc     J08467+2846A  80416  43103 ... 1989ApJS...71..245K        4905  -0.06 2014ApJ...785...94L
          24 Com *  24 Com A     J12351+1823A 100160  61418 ... 1997JApA...18..161Y           0  -0.04 1997JApA...18..161Y
          xi Boo   * ksi Boo    J14514+1906AB 101250  72659 ... 1978PASP...90..429L        5410  -0.05 2016A&A...587A...2B
       alpha Her   * alf Her    J17146+1423AB   None  84345 ... 2014yCat....1.2023S           0   0.00                    
          95 Her   *  95 Her    J18015+2136AB  85648  88267 ...                               0   0.00                    
        zeta Lyr * zet01 Lyr     J18448+3736A  67321  91971 ...                            7914   0.38 2011A&A...531A.165P
         Albireo * bet Cyg A     J19307+2758A  87301  95947 ... 1969PhDT.........5M        4270  -0.17 1990ApJS...74.1075M
          31 Cyg * omi01 Cyg J20136+4644Aa,Ab  49337  99675 ... 2000ApJ...541..298W        4186   0.03 2011A&A...531A.165P
        beta Cap   * bet Cap    J20210-1447AB   None   None ...                               0   0.00                    
       gamma Del   * gam Del    J20467+1607AB   None   None ...                               0   0.00                    
       delta Cep   * del Cep     J22292+5825A  34508 110991 ... 2013AJ....146...93E        5695   7.62 2011AJ....142..136L
<Table length=22>
      name        dtype     unit   format                description               
---------------- ------- --------- ------ -----------------------------------------
            Star   str24               {}              User-supplied star object ID
        SimbadID   str16                                     Main ID used by Simbad
             WDS   str20                          Washington Double Star Catalog ID
             SAO   str20                                        SAO Star Catalog ID
             HIP   str20                                Hipparcos Output Catalog ID
            NAME   str20                                                Common name
              HD   str20                                    Henry Draper Catalog ID
         RA_icrs   str13   "h:m:s"        Right ascension, HMS, ICRS at J2000 epoch
        DEC_icrs   str13   "d:m:s"            Declination, DMS, ICRS at J2000 epoch
     RA_icrs_deg float64       deg {:.6f}        Right ascension in decimal degrees
    DEC_icrs_deg float64       deg {:.6f}            Declination in decimal degrees
   RADEC_bibcode   str24                                    Bibcode for coordinates
            magB float32       mag {:.2f}                 V-band apparent magnitude
        magB_err float32           {:.2f}  Uncertainty in B-band apparent magnitude
    magB_bibcode   str24                      Bibcode for B-band apparent magnitude
            magV float32       mag {:.2f}                 V-band apparent magnitude
        magV_err float32           {:.2f}  Uncertainty in V-band apparent magnitude
    magV_bibcode   str24                      Bibcode for V-band apparent magnitude
        parallax float64       mas {:.2f}                                  parallax
    parallax_err float32       mas {:.2f}                              parallax_err
parallax_bibcode   str24                                       Bibcode for parallax
           pm_RA float64  mas / yr {:.2f}                       Proper motion in RA
          pm_DEC float64  mas / yr {:.2f}                      Proper motion in DEC
     pm_err_maja float32  mas / yr {:.2f}            Proper motion error major axis
     pm_err_mina float32  mas / yr {:.2f}            Proper motion error minor axis
    pm_err_angle   int16       deg                        Proper motion error angle
      pm_bibcode   str24                                  Bibcode for proper motion
       spec_type   str16                   Spectral type including luminosity class
       spec_qual    str1                                      Spectral type quality
    spec_bibcode   str24                                  Bibcode for spectral type
     Teff_(Fe_H)   int32 unit-degK                       Effective temperature in K
          [Fe/H] float32           {:.2f}    Metal abundance relative to Sun in dex
    Fe_H_bibcode   str19                       Bibcode for metal abundance and Teff

Wrote formatted table to king_processed_summary.html using CSS style darkTable

```

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
  
