#!/usr/bin/env bash
#-----------------------------------------------------------------------
# bash download_data.sh
#
# Downloads data tables needed for DoubleStars from CDS VizieR
# in gzipped fits format, and corrects a malformed fits EPOCH keyword 
# in the main WDS data table.
#
# It can also download the main table in ascii format to get around a 
# fits file corruption problem that appeared in the 2018-2019 timeframe.
#
# If the user has HEASOFT installed it will use fverify to verify that 
# the downloaded fits files are valid.
#
# @author Dave Strickland <dave.strickland@gmail.com>
#
# @history 2018-03-13 dks : Initial version coded.
# @history 2020-03-05 dks : Reformat history and author tags.
# @history 2020-03-06 dks : Add a .gitignore to $p_data_dir
# @history 2020-03-21 dks : Option to download main WDS data in text form.
# @history 2020-06-12 dks : Minor improvements to header correction section.
#                           As of 6/12/20 the main WDS fits file is still corrupt.
#                           Update documentation. Still need to add
#                           conversion of ascii WDS table to fits.
#-----------------------------------------------------------------------
#

# Check that wget is available
which wget >& /dev/null
if [ $? -ne 0 ]; then
    echo "Error: wget is not installed or in your path."
    exit 1
fi 

# See if fverify is present (part of HEASOFT).
which fverify >& /dev/null
if [ $? -eq 0 ]; then
    p_verify=$(which fverify)
fi 


# Check DOUBLE_STARS is defined, but work around it not being set...
if [ -z "$DOUBLE_STARS" ]; then
    echo "Warning: DOUBLE_STARS environment variable not set. Using ./"
    p_basedir=./
    echo "  You need to set DOUBLE_STARS for the python scripts to work properly."
else
    p_basedir=$DOUBLE_STARS
fi

# Switch on whether to download and convert the text version of the
# table to work around a bug with the fits version.
p_do_text=1

# Do we try to fix the header of B_wds.fits.gz?
# - We can disable this by setting p_fix_hdr=0
# - Not necessary of p_do_test==1.
p_fix_hdr=0

p_data_dir=$p_basedir/data
p_wds_dir=$p_data_dir'/WDS'

if [ $p_do_text -eq 0 ]; then
    p_wds_fnames=("ReadMe.WDS" \
        "B_wds.fits.gz" \
        "B_wds_refs.fits.gz" \
        "B_wds_notes.fits.gz")
    p_wds_urls=("https://cdsarc.u-strasbg.fr/vizier/ftp/cats/B/wds/ReadMe" \
        "https://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/fits.gz?B/wds/wds.dat.gz" \
        "https://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/fits.gz?B/wds/refs.dat.gz" \
        "https://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/fits.gz?B/wds/notes.dat.gz" )
else
    p_wds_fnames=("ReadMe.WDS" \
        "B_wds.dat.gz" \
        "B_wds_refs.fits.gz" \
        "B_wds_notes.fits.gz")
    p_wds_urls=("https://cdsarc.u-strasbg.fr/vizier/ftp/cats/B/wds/ReadMe" \
        "https://cdsarc.unistra.fr/ftp/B/wds/___wds.dat.gz" \
        "https://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/fits.gz?B/wds/refs.dat.gz" \
        "https://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/fits.gz?B/wds/notes.dat.gz" )
fi

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

# Download and process each file in turn.
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
    else
        if [ $(echo $p_file | grep -c fits) -gt 0 ]; then
            # If fverify is present, attempt to verify any fits file.
            if [ ! -z "$p_verify" ]; then
                echo "    Verifying FITS compliance with fverify..."
                p_tmp=$(mktemp)
                $p_verify $p_file >& $p_tmp
                p_nerr=$(grep "Verification found" $p_tmp | awk '{print $7}')
                if [ $p_nerr -eq 0 ]; then
                    echo "      OK. File passes inspection."
                    rm $p_tmp
                else
                    # Move the temporary file and rename it.
                    p_tmp2=$p_odir'/fverify_error_log_'$p_file
                    mv $p_tmp $p_tmp2
                    echo "      Warning: fverify found $p_nerr errors. Check $p_tmp2 for details."
                fi
            fi
        fi
    fi    
    
    # sleep a bit to slow down web queries
    sleep 2
    ((ifile++))
done

# Can try to fix/update B_wds.fits.gz header.
# This will only work if there aren't other major problems with the file.
if [ $p_fix_hdr -eq 1 ]; then
    p_fcheck=./B_wds.fits.gz
    if [ -e $p_fcheck ]; then
        if [ -e $p_fmod ]; then
            echo "NB: Using $p_fmod to attempt to fix B_wds.fits.gz EPOCH"
            echo "  If there are other problems with the file this is likely to fail."
            python3 $p_fmod $p_fcheck EPOCH 2000
        else
            echo "Warning: $p_fmod not found. Cannot fix $p_fcheck EPOCH"
        fi
    else
        echo "Warning: Cannot check fits header for non-existant file $p_fcheck"
    fi
else
    echo "Not attempting to fix $p_fcheck EPOCH keyword. YMMV."
fi
cd $p_odir

echo "WDS data download completed at" $(date)

#-----------------------------------------------------------------------
#
exit 0
