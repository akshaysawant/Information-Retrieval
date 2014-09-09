#!/bin/bash

awk '{
	array[$0]++
	TotalWords++
     }END {
	print TotalWords
        for (i in array)
	   print i" ", array[i] | "sort -k2 -n -r"
     }' output | awk 'BEGIN{
     			     counter = -1
			     Fcounter = 0
			     rank = 0}
			     {
			        if (NF == 1)
			  	{
			    	  TotalWords = $1
			  	}
			  	else if (counter < 25)
			  	{ 
			   	  probability = $2/TotalWords
			  	  print $1, $2, rank, probability, probability*rank
			  	}
			  	else if ((Fcounter < 25) && match($1, "^[fF]"))
			  	{
			  	  probability = $2/TotalWords
			  	  print $1, $2, rank, probability, probability*rank
			  	  Fcounter++
			  	}
				rank++
				counter++
			     }END {
			        print "Total Words = " TotalWords
				print "Total Unique Words = " counter
			     }' > p1a.txt

