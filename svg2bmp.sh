#!/bin/bash

mkdir bmp

    size=(16 24)
    filenames=(go-previous go-next window-close view-refresh go-home edit-find rating document-print font-select view-form view-form-action stock_xfburn-audio-cd exchange-positions-clockwise mail-read view-fullscreen stock_notes)

    echo Making bitmaps 214-217 from your svg...

    for i in ${size[@]}; do
        for j in ${filenames[@]}; do
        inkscape $j.svg --export-png="$j-$i.png" -w$i -h$i --without-gui
        done
		convert +append $(echo ${filenames[@]/%/-$i.png}) ./bmp/$i.bmp
		convert +append $(echo ${filenames[@]/%/-$i.png}) -modulate 100,130,100 ./bmp/$i-sat.bmp
		
    done
