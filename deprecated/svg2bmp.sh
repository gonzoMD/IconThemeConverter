#!/bin/bash


svg2bmp()
{
    echo Making bitmaps starting with $target from your svg...

    for i in ${size[@]}; do
        for j in ${filenames[@]}; do
            inkscape $j.svg --export-png="$j-$i.png" -w$i -h$i --without-gui
        done
        convert +append $(echo ${filenames[@]/%/-$i.png}) ./bmp/$target.bmp
        convert +append $(echo ${filenames[@]/%/-$i.png}) -modulate 100,130,100 ./bmp/$((target+1)).bmp
        ((target=target+2))
    done
}

mkdir bmp

size=(24 16)
filenames=(go-previous go-next window-close view-refresh go-home edit-find rating document-print font-select view-form view-form-action stock_xfburn-audio-cd exchange-positions-clockwise mail-read view-fullscreen stock_notes)
target=204

svg2bmp

size=(24 16)
filenames=(go-previous go-next rating starred view-sidetree edit-cut edit-copy edit-paste edit-undo edit-redo edit-delete document-new document-open document-save document-preview view-calendar-special-occasion help-contents edit-find edit-find-replace document-print view-grid view-compact view-column view-list-compact sort-name view-sort-ascending view-sort-ascending view-sort-ascending go-parent-folder network-connect network-disconnect folder-new view-column gtk-convert snap kdeconnect kdeconnect view-grid view-column font-select view-list-compact document-new document-new-from-template ../../apps/scalable/system-file-manager folder-move folder-copy folder-sync)
target=214

svg2bmp

size=(16 24)
filenames=(edit-cut edit-copy edit-paste font-select send-to document-preview)
target=225

svg2bmp

size=(20)
filenames=(go-jump)
target=230

svg2bmp