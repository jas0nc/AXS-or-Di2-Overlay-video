#!/usr/bin/env bash

homedir="/Users/jachan/Documents/GitHub/AXS-or-Di2-Overlay-video"
outputdir="/Users/jachan/Downloads/Overlay"

export PATH="/opt/homebrew/bin:$PATH"
cd $homedir

echo "~~~~ Jason's Cycling Videos YouTube Channel - Gearbox Overlay Tool ~~~~"
echo "~~~~ Running on $homedir ~~~~"
echo "~~~~ Clearing cache ~~~~"
echo "~~~~ Drag the Event file (csv) to here ~~~~"
read input
filename="$(basename $input .csv)"

echo "~~~~ Converting $input to $outputdir/$filename-gearbox.mov ~~~~"
python3.11 gear_overlay.py $input -o $outputdir/$filename-gearbox.mov