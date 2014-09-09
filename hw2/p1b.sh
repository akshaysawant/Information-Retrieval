#!/bin/bash

awk '{
        array[$0]++
     }END {
        for (i in array)
           print i" ", array[i] | "sort -k2 -n"
     }' output | awk 'BEGIN {counter = 0
     			     TotalCount = 0}
     		      {
		        if ($2 < 5)
			{
			  counter++
			}
			TotalCount++
		      }END {
		        print "Total Omitted Words = " counter
			print "Total Words in Collection = " TotalCount
			print "Proportion of omitted words = " (counter/TotalCount)
		      }'
