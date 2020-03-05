#!/bin/bash -xv
#-----------------------------------------------------------------------
# bash run_examples.sh
#
# Reruns the entire sequence of scripts corresponding to the example
# shown in EXAMPLES.md
#
# @note The DOUBLE_STARS environment variable is used to find the
#   scripts, data, and ancilliary files. 
#
# @author Dave Strickland <dave.strickland@gmail.com>
#
# @history 2020-03-05 dks : Initial version coded.
#-----------------------------------------------------------------------
#

# DOUBLE_STARS must be defined.
if [ -z "$DOUBLE_STARS" ]; then
    echo "Error: DOUBLE_STARS environment variable not defined."
    echo "  The DOUBLE_STARS environment variable should be set point to"
    echo "  the directory containing the python scripts."
    exit 1
else
    echo "Using DOUBLE_STARS=$DOUBLE_STARS"
fi


#python3 star_query.py bob_king_colored_double_stars.html \
    #king_processed_summary.html king_processed.fits.gz \
    #--pretty pretty_king_input.html --verbose

#-----------------------------------------------------------------------
# All done
exit 0
