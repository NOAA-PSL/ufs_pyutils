#!/bin/bash --norc --noprofile -posix
set -x -e
cd /Users/henry.winterbottom/trunk/UFS-RNR.HenryWinterbottom-NOAA/ush/batch
/usr/local/bin/singularity run ./tests/lolcow_latest.sif
# Created: 18:20:49 Wednesday November 23, 2022