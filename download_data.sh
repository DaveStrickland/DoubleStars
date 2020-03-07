#!/usr/bin/env bash
#-----------------------------------------------------------------------
# bash download_data.sh
#
# Downloads data tables needed for DoubleStars from CDS VizieR
# in gzipped fits format.
#
# @author Dave Strickland <dave.strickland@gmail.com>
#
# @history 2018-03-13 dks : Initial version coded.
# @history 2020-03-05 dks : Reformat history and author tags.
# @history 2020-03-06 dks : Add a .gitignore to $p_data_dir
#-----------------------------------------------------------------------
#

# Check that wget is available
which wget >& /dev/null
if [ $? -ne 0 ]; then
    echo "Error: wget is not installed or in your path."
    exit 1
fi 

# Check DOUBLE_STARS is defined, but work around it not being set...
if [ -z "$DOUBLE_STARS" ]; then
    echo "Warning: DOUBLE_STARS environment variable not set. Using ./"
    p_basedir=./
    echo "  You need to set DOUBLE_STARS for the python scripts to work properly."
else
    p_basedir=$DOUBLE_STARS
fi

p_data_dir=$p_basedir/data
p_wds_dir=$p_data_dir'/WDS'
p_wds_fnames=("ReadMe.WDS" \
    "B_wds.fits.gz" \
    "B_wds_refs.fits.gz" \
    "B_wds_notes.fits.gz")
p_wds_urls=("http://cdsarc.u-strasbg.fr/vizier/ftp/cats/B/wds/ReadMe" \
    "http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/fits.gz?B%2Fwds/wds.dat.gz" \
    "http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/fits.gz?B%2Fwds/refs.dat.gz" \
    "http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/fits.gz?B%2Fwds/notes.dat.gz" )

# Do we try to fix the header of B_wds.fits.gz?
# We can disable this by setting p_fix_hdr=0
p_fix_hdr=0

# current directory
p_odir=$(pwd)
p_fmod=$p_odir/fitsmodhead.py

if [ ! -d $p_data_dir ]; then
    echo "Creating base data directory: $p_data_dir"
    mkdir -p $p_data_dir
    # Create a .gitignore in $p_data_dir if we've just created it
    # to avoid WDS data getting added to the repo.
    cat << EOF > $p_data_dir/.gitignore
# Ignore the following directories
WDS
EOF
else
    echo "Using existing base data directory: $p_data_dir"
fi

# WDS specific stuff
echo "Setting up WDS data"
if [ ! -d $p_wds_dir ]; then
    echo "  Creating directory: $p_wds_dir"
    mkdir -p $p_wds_dir
else
    echo "  Using existing directory: $p_wds_dir"
fi
cd $p_wds_dir
ifile=0
nfiles=${#p_wds_fnames[@]}
echo "  About to download $nfiles files."
while [ $ifile -lt $nfiles ]; do
    p_file=${p_wds_fnames[$ifile]}
    if [ -e $p_file ]; then
        rm $p_file
    fi
    echo "  Downloading $p_file"
    wget -q --output-document=$p_file \
        ${p_wds_urls[$ifile]} \
        --limit-rate=1m
    if [ ! -e $p_file ]; then
        echo " Error: failed to download $p_file"
    fi    
    
    # sleep a bit to slow down web queries
    sleep 2
    ((ifile++))
done

# Can try to fix/update B_wds.fits.gz header.
if [ $p_fix_hdr -eq 1 ]; then
    if [ -e $p_fmod ]; then
        echo "NB: Using $p_fmod to fix B_wds.fits.gz EPOCH"
        python3 $p_fmod ./B_wds.fits.gz EPOCH 2000
    else
        echo "Warning: $p_fmod not found. Cannot fix B_wds.fits.gz EPOCH"
    fi
else
    echo "Not attempting to fix B_wds_fits.gz EPOCH keyword. YMMV."
fi
cd $p_odir

#-----------------------------------------------------------------------
#
exit 0
