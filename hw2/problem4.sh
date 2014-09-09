#!/bin/bash

rm -f output.txt
head -n 10 p1a.txt | cut -d" " -f1 > input

while read in;
do
   awk -v iword="$in" -f p4.awk biagram > abc.txt
   grep -w "MIM" abc.txt | sort -k2 -n -r | head -n 5 > MIM
   grep -w "EMIM" abc.txt | sort -k2 -n -r | head -n 5 > EMIM
   grep -w "CHISQ" abc.txt | sort -k2 -n -r | head -n 5 > CHISQ
   grep -w "DICE" abc.txt | sort -k2 -n -r | head -n 5 > DICE

   for file in MIM EMIM CHISQ DICE
   do
      awk -v output="$in $file" '{
	      output = output " " $1 ":" $2
	   }END {print output}' $file >> output.txt
   done
   rm -f MIM EMIM CHISQ DICE abc.txt
done < input

rm -f input p4.txt
