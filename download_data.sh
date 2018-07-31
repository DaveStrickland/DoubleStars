#!/usr/bin/env bash
#-----------------------------------------------------------------------
# bash download_data.sh
#
# Downloads data tables needed for DoubleStars from CDS VizieR
# in gzipped fits format.
#
# Dave Strickland <dave.strickland@gmail.com> Mar 13, 2018 v0.1.1
#-----------------------------------------------------------------------
#

if [ -z "$DOUBLE_STARS" ]; then
    echo "DOUBLE_STARS environment variable not set. Using ./"
    p_basedir=./
else
    p_basedir=$DOUBLE_STARS
fi

p_data_dir=$p_basedir/Data
p_wds_dir=$p_data_dir'/WDS'
p_wds_fnames=("ReadMe.WDS" \
    "B_wds.fits.gz" \
    "B_wds_refs.fits.gz" \
    "B_wds_notes.fits.gz")
p_wds_urls=("http://cdsarc.u-strasbg.fr/vizier/ftp/cats/B/wds/ReadMe" \
    "http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/fits.gz?B%2Fwds/wds.dat.gz" \
    "http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/fits.gz?B%2Fwds/refs.dat.gz" \
    "http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/fits.gz?B%2Fwds/notes.dat.gz" )

# current directory
p_odir=$(pwd)
p_fmod=$p_odir/fitsmodhead.py

if [ ! -d $p_data_dir ]; then
    echo "Creating base data directory: $p_data_dir"
    mkdir -p $p_data_dir
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
# Must fix/update B_wds.fits.gz header.
if [ -e $p_fmod ]; then
    echo "NB: Using $p_fmod to fix B_wds.fits.gz EPOCH"
    python3 $p_fmod ./B_wds.fits.gz EPOCH 2000
else
    echo "Warning: $p_fmod not found. Cannot fix B_wds.fits.gz EPOCH"
fi
cd $p_odir

#-----------------------------------------------------------------------
#
exit 0
