#!/usr/bin/python

import csv

term_index = {}

with open("doc_index.txt", "r") as tsv:
   for line in csv.reader(tsv, delimiter="\t"):
      key = int(line[1])
      print line[0] + '\t' + line[1]
      if key in term_index.keys():
         docid = int(line[0])
         term_val = term_index[key]
	 prev_docid = term_val[0]
	 term_val[1] = term_val[1] + 1
	 occurance = term_val[2]
	 index_str = term_val[3]
	 index_str = index_str + '\t' + str(docid - prev_docid) + ':' + line[2]
	 if len(line) > 3:
	    prev_pos = int(line[2])
	    for pos in line[3:]:
	       index_str = index_str + '\t' + '0:' + str(int(pos) - prev_pos)
	       prev_pos = int(pos)
	 term_index[key] = [int(line[0]), term_val[1], occurance + len(line[2:]), index_str]
      else:
         index_str = line[0] + ':' + line[2]
         #term_index[key] = [key, 1, 1, '']
	 if len(line) > 3:
	    prev_pos = int(line[2])
	    for pos in line[3:]:
	       index_str = index_str + '\t' + '0:' + str(int(pos) - prev_pos)
	       prev_pos = int(pos)
	 term_index[key] = [int(line[0]), 1, len(line[2:]), index_str]

f_term_index = open("term_index.txt", "w")
f_term_info = open ("term_info.txt", "w")
offset = 0

for key, value in term_index.items():
   index_str = str(key) + '\t' + value[3] + '\n'
   f_term_index.write(index_str)
   info_str = str(key) + '\t' + str(offset) + '\t' + str(value[2]) + '\t' + str(value[1]) + '\n'
   offset = offset + len(index_str)
   f_term_info.write(info_str)

f_term_index.close()
f_term_info.close()



