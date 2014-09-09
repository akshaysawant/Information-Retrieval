#!/usr/bin/python

import sys
import csv 

def incorrect_usage():
   print "Incorrect Usage."
   print "Usage:"
   print "./read_index.py --doc DOCNAME"
   print "./read_index.py --term TERM"
   print "./read_index.py --term TERM --doc DOCNAME"

if len(sys.argv) == 3:
   if sys.argv[1] == "--doc":
      docid = ''
      doc_name = sys.argv[2]
      f_docid = open("docids.txt", "r")
      docids_data = f_docid.readlines()
      for line in docids_data:
         docid_list = line.split("\t")
         if doc_name == docid_list[0]:
	    docid = docid_list[1]
	    break
      
      f_doc_index = open("doc_index.txt", "r")
      index_data = f_doc_index.readlines()
      dist_terms = 0
      total_terms = 0
      found = False
      docid_num = int(docid)
      for data in index_data:
         line = data.split('\t')
	 if docid_num == int(line[0]):
	    found = True
	    dist_terms += 1
	    total_terms += len(line[2:])
	 elif found == True:
	    break

      print "Listing for document: " + doc_name
      print "DOCID: " + docid.strip()
      print "Distinct terms: " + str(dist_terms)
      print "Total terms: " + str(total_terms)

   elif sys.argv[1] == "--term":
      docid = ''
      term_name = sys.argv[2]
      f_termid = open("termids.txt", "r")
      termids_data = f_termid.readlines()
      for line in termids_data:
         termid_list = line.split("\t")
         if term_name == termid_list[0]:
            termid = termid_list[1]
            break
      
      f_term_index = open("term_info.txt", "r")
      index_data = f_term_index.readlines()
      term_offset = ''
      no_occur = ''
      no_docs = ''
      termid_num = int(termid)
      for data in index_data:
         line = data.split('\t')
         if termid_num == int(line[0]):
            term_offset = line[1]
            no_occur = line[2]
            no_docs = line[3]
            break

      print "Listing for term: " + term_name
      print "TERMID: " + termid.strip()
      print "Number of documents containing term: " + no_docs.strip()
      print "Term frequency in corpus: " + no_occur.strip()
      print "Inverted list offset: " + term_offset.strip()
   else:
      incorrect_usage()
elif len(sys.argv) == 5:
   if sys.argv[1] == "--term" and sys.argv[3] == "--doc":
      term_name = sys.argv[2]
      doc_name = sys.argv[4]
      term_offset = 0

      with open("termids.txt", "r") as tsv:
         for line in csv.reader(tsv, delimiter="\t"):
	    if term_name == line[0]:
	       termid = int(line[1])
	       break

      with open("docids.txt", "r") as tsv:
         for line in csv.reader(tsv, delimiter="\t"):
            if doc_name == line[0]:
               docid = int(line[1])
               break

      with open("term_info.txt", "r") as tsv:
         for line in csv.reader(tsv, delimiter="\t"):
            if termid == int(line[0]):
               term_offset = int(line[1])
               break

      f_term_ind = open("term_index.txt", "r")
      f_term_ind.seek(term_offset)
      term_data = f_term_ind.readline().split('\t')
      freq = 0
      cur_pos = 0
      cur_docid = 0
      pos = []

      for tdata in term_data[1:]:
         data = tdata.split(':')
	 cur_docid += int(data[0])
	 if docid == cur_docid:
	    freq += 1
	    cur_pos += int(data[1])
	    pos.append(cur_pos)
      
      pos_str = str(pos[0])
      for x in pos[1:]:
         pos_str += ', ' + str(x)

      print "Inverted list for term: " + term_name
      print "In document: " + doc_name
      print "TERMID: " + str(termid)
      print "DOCID: " + str(docid)
      print "Term frequency in document: " + str(freq)
      print "Positions: " + pos_str

   else:
      incorrect_usage()
else:
   incorrect_usage()
