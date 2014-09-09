#!/bin/sh

wget -r www.ccs.neu.edu -U firefox -S --spider -A pdf  -w 5 -o out.txt

grep -e "--  http" out.txt | cut -d " " -f 4 | awk '!_[$1]++' | head -n 100 > p1.txt

rm -rf out.txt www.ccs.neu.edu
