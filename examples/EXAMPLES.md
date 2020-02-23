# DoubleStars Examples

## Bob King's Colored Double Stars

An example of running the code using a list of stars from [Bob King's
article on colored Double stars](http://www.skyandtelescope.com/observing/colored-double-stars-real-and-imagined/) 
follows. This was run in verbose mode to get it to output the list of
information collected on each object. (**Note** that this full set of
information is always written to the output fits-format table, but that
a smaller selection of the data is written to the output HTML table
**unless** `--fullhtml` is selected.)

## Step 1: Running star_query

### star_query.py usage

Run `star_query.py` with `-h` or `--help` to get the command line usage.
Example input files are provided as part of this package.

```bash
$ python3 star_query.py --help
usage: star_query.py [-h] [-p pretty_input_version.html] [-c colname]
                     [--fullhtml] [--css table_style.css]
                     [--aliases ALIASES.csv] [--stage2]
                     [--stage2col stage2col] [-v]
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
  -c colname, --col colname
                        Name of the table column containing primary target
                        star name/identifier (default: Star) In the default
                        (aka primary stage) processing the targets are listed
                        by the name in this column and the Simbad search uses
                        this identifier (or the alternative from the "aliases"
                        file).
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
  --stage2              Activate secondary stage processing. This should only
                        by performed on inputs that have WDS components
                        identified. In secondary stage processing targets are
                        still listed with respect to the user ID in the
                        "colname" table column, but the Simbad searches are
                        made using identifiers in the "stage2col" table column
                        instead.
  --stage2col stage2col
                        Name of the table column containing identifier used
                        for each target in stage2 processing (default: WDS)
  -v, --verbose         Verbose output for each object processed. Useful for
                        debugging purposes.

```

### Querying Simbad


In this case we're using the HTML table extracted from that article (slightly
editted to remove some HTML table complexities that astropy can't handle).


```bash
$ python3 star_query.py bob_king_colored_double_stars.html \
    king_processed_summary.html king_processed.fits.gz \
    --pretty pretty_king_input.html --verbose
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

Note that `king_processed.fitz.gz` is the full set of output data, while
`king_processed_summary.html` is a subset of that data that is easier
for humans to view.

## Step 2: Run process_wds_ids

### process_wds_ids.py usage

Before running `process_wds_ids.py` for the first time you should 
run `download_data.sh` to download and fix the WDS data file it 
needs. This only needs to be done once, e.g:

```bash
$ bash download_data.sh 
DOUBLE_STARS environment variable not set. Using ./
Using existing base data directory: .//Data
Setting up WDS data
  Using existing directory: .//Data/WDS
  About to download 4 files.
  Downloading ReadMe.WDS
  Downloading B_wds.fits.gz
  Downloading B_wds_refs.fits.gz
  Downloading B_wds_notes.fits.gz
NB: Using fitsmodhead.py to fix B_wds.fits.gz EPOCH
Original keyword=EPOCH value=2000,.
Updated keyword=EPOCH value=2000
```

`process_wds_ids.py` has the following options:
```bash
& python3 process_wds_ids.py --help
usage: process_wds_ids.py [-h] [--wds-detail wds_detail.html]
                          [--css table_style.css] [-w WDSFILE]
                          [--filter FILTER] [--magdiff MAGDIFF] [-v]
                          INPUT_STAR_QUERY_OUTPUT.fits OUT_TABLE

positional arguments:
  INPUT_STAR_QUERY_OUTPUT.fits
                        Fits table that was generated by star_query.py
  OUT_TABLE             Name for table of processed targets with their WDS
                        identifiers. Format is determined from file name.

optional arguments:
  -h, --help            show this help message and exit
  --wds-detail wds_detail.html
                        Name for optional output of WDS informational data on
                        processed WDS components that passed filtering. Format
                        is determined from file name.
  --css table_style.css
                        CSS table style for output HTML (default:
                        darkTable.css)
  -w WDSFILE, --wdsfile WDSFILE
                        Location of WDS data table. (default:
                        Data/WDS/B_wds.fits.gz)
  --filter FILTER       Type of binary star filtering to apply. Valid entries
                        are "abc", "negative", or "positive" (default:
                        negative) "abc" selects A, B and C components.
                        "positive" selects only physically likely companions.
                        "negative" deselects unphysical components and
                        components with large magnitude differences.
  --magdiff MAGDIFF     Maximum magnitude difference allowed in negative
                        filter (default: 6.0)
  -v, --verbose         Verbose output for each object processed. Useful for
                        debugging purposes.
```

### Running process_wds_ids

An example of using `process_wds_ids.py` with the `positive` filter is 
shown below. This also writes some additional information extracted 
from the WDS data to a separate HTML format table with a name defined 
by the `--wds-detail` command line parameter.
```bash
$ python3 process_wds_ids.py king_processed.fits.gz king_wds_postv_ids.html \
    --wds-detail=king_wds_postv_detail.html  --filter=positive
Processing 22 targets from king_processed.fits.gz
  Target #0 eta Cas obtained WDS-like ID 00491+5749 from J00491+5749AB
  Target #1 1 Ari obtained WDS-like ID 01501+2217 from J01501+2217AB
    Target #1 1 Ari has no likely WDS components after filtering
  Target #2 gamma And obtained WDS-like ID 02039+4220 from J02039+4220A,BC
  Target #3 iota Tri = 6 Tri obtained WDS-like ID 02124+3018 from J02124+3018AB
    Target #3 iota Tri = 6 Tri has no likely WDS components after filtering
  Target #4 eta Per obtained WDS-like ID 02507+5554 from J02507+5554A
    Target #4 eta Per has no likely WDS components after filtering
  Target #5 32 Eri obtained WDS-like ID 03543-0257 from J03543-0257AB
    Target #5 32 Eri has no likely WDS components after filtering
  Target #6 rho Ori obtained WDS-like ID 05133+0252 from J05133+0252AB
    Target #6 rho Ori has no likely WDS components after filtering
  Target #7 14 Aur obtained WDS-like ID 05154+3241 from J05154+3241A
  Target #8 iota Ori obtained WDS-like ID 05354-0555 from J05354-0555A
    Target #8 iota Ori has no likely WDS components after filtering
  Target #9 gamma Lep obtained WDS-like ID 05445-2227 from J05445-2227A
    Target #9 gamma Lep has no likely WDS components after filtering
  Target #10 h3945 CMa obtained WDS-like ID 07166-2319 from J07166-2319A
  Target #11 iota Cnc obtained WDS-like ID 08467+2846 from J08467+2846A
  Target #12 24 Com obtained WDS-like ID 12351+1823 from J12351+1823A
    Target #12 24 Com has no likely WDS components after filtering
  Target #13 xi Boo obtained WDS-like ID 14514+1906 from J14514+1906AB
  Target #14 alpha Her obtained WDS-like ID 17146+1423 from J17146+1423AB
  Target #15 95 Her obtained WDS-like ID 18015+2136 from J18015+2136AB
  Target #16 zeta Lyr obtained WDS-like ID 18448+3736 from J18448+3736A
  Target #17 Albireo obtained WDS-like ID 19307+2758 from J19307+2758A
  Target #18 31 Cyg obtained WDS-like ID 20136+4644 from J20136+4644Aa,Ab
  Target #19 beta Cap obtained WDS-like ID 20210-1447 from J20210-1447AB
  Target #20 gamma Del obtained WDS-like ID 20467+1607 from J20467+1607AB
  Target #21 delta Cep obtained WDS-like ID 22292+5825 from J22292+5825A
Found WDS IDs for 14 input targets, skipped 8
Wrote formatted table to king_wds_postv_ids.html using CSS style darkTable
Wrote filtered WDS component for input targets to king_wds_postv_ids.html
Wrote formatted table to king_wds_postv_detail.html using CSS style darkTable
Wrote WDS component detail info to king_wds_postv_detail.html
Information on targets with no WDS or all WDS components filtered out.
  0 input targets with no WDS info: []
  8 input targets where positive filtering removed all components: ['1 Ari', 'iota Tri = 6 Tri', 'eta Per', '32 Eri', 'rho Ori', 'iota Ori', 'gamma Lep', '24 Com']
```

## Step 3: Rerun star_query

TBA

## Step 4: Calculate physical properties using XXX

TBA

