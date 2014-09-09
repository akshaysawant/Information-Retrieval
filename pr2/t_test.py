#!/usr/bin/python

from scipy import stats
import csv

stat_measure = ["AP", "F1", "NDCG"]

for measure in stat_measure:
   bm_vals = []
   jm_vals = []
   t_value = []
   with open("p2-scores.txt", "r") as tsv:
      for doc_entry in csv.reader(tsv, delimiter="\t"):
         if len(doc_entry) == 4 and doc_entry[0] == measure:
	    if doc_entry[1] == "BM25" and doc_entry[2] != "avg":
	       bm_vals.append(float(doc_entry[3]))
	    elif doc_entry[1] == "JM" and doc_entry[2] != "avg":
	       jm_vals.append(float(doc_entry[3]))
   t_value = stats.ttest_ind(bm_vals, jm_vals, equal_var=True)
   p_value = t_value[1]
   print "p-value for " + measure + " is " + str(p_value)
   if p_value < 0.05:
      print "Okapi BM25 is better than Language Model with Jelinek-Mercer Smoothing for " + measure + "\n"
   else:
      print "Okapi BM25 and Language Model with Jelinek-Mercer Smoothing are not different for " + measure + "\n"
