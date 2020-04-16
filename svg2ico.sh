#!/bin/bash

svg2png()
{

    svg=$1

    size=(16 32 24 48)

    echo Making bitmaps from your svg...

    for i in ${size[@]}; do
        inkscape $svg --export-png="$svg-$i.png" -w$i -h$i --without-gui
    done

}


png2ico()
{

echo Converting to icons...

convert $(ls -v $1*.png) ./ico/$1.ico

## Clean-up maybe?
# rm favicon-*.png

echo Done
}

mkdir ico

for file in *.svg
do
    svg2png $file
    png2ico $file
done
