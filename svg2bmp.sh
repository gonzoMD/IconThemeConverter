#!/bin/bash

mkdir bmp

size=(24 16)
filenames=(go-previous go-next window-close view-refresh go-home edit-find rating document-print font-select view-form view-form-action stock_xfburn-audio-cd exchange-positions-clockwise mail-read view-fullscreen stock_notes)
target=214

echo Making bitmaps 214-217 from your svg...

for i in ${size[@]}; do
    for j in ${filenames[@]}; do
        inkscape $j.svg --export-png="$j-$i.png" -w$i -h$i --without-gui
    done
    convert +append $(echo ${filenames[@]/%/-$i.png}) ./bmp/$target.bmp
    convert +append $(echo ${filenames[@]/%/-$i.png}) -modulate 100,130,100 ./bmp/$((target+1)).bmp
    ((target=target+2))
done

size=(16 24)
filenames=(edit-cut edit-copy edit-paste font-select send-to document-preview)
target=225

echo Making bitmaps 225-228 from your svg...

for i in ${size[@]}; do
    for j in ${filenames[@]}; do
        inkscape $j.svg --export-png="$j-$i.png" -w$i -h$i --without-gui
    done
    convert +append $(echo ${filenames[@]/%/-$i.png}) ./bmp/$target.bmp
    convert +append $(echo ${filenames[@]/%/-$i.png}) -modulate 100,130,100 ./bmp/$((target+1)).bmp
    ((target=target+2))
done
