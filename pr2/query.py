#!/usr/bin/python

from __future__ import division
import sys
import csv
import math
from xml.dom import minidom
from stemming.porter import stem


def incorrect_usage():
   print "Incorrect Usage."
   print "Usage:"
   print "./query.py --score RANK_ALGO"

Qvector = {}
doc_hash = {}
term_hash = {}
doc_term = {}
doc_len = {}
term_frq = {}
doc_score = {}
term_info = {}
Qtf = {}

sum_doclen = 0
num_doc = 0
avg_doclen = 0
lmbda = 0.2


def create_doc_hash():
   f_docid = open("docids.txt", "r")
   readlines = f_docid.readlines()

   for l in readlines:
      docl = l.split('\t')
      doc_hash[docl[1].strip()] = docl[0]
   global num_doc
   num_doc = len(doc_hash)


def create_term_hash():
   f_termid = open("termids.txt", "r")
   readlines = f_termid.readlines()
   
   for l in readlines:
      terml = l.split('\t')
      term_hash[terml[0]] = terml[1].strip()


def create_term_info():
   global term_info

   with open("term_info.txt", "r") as tsv:
         for doc_entry in csv.reader(tsv, delimiter="\t"):
	    term_info[doc_entry[0]] = [int(doc_entry[2]), int(doc_entry[3])]

def create_doc_term():
   global sum_doclen

   with open("doc_index.txt", "r") as tsv:
      for doc_entry in csv.reader(tsv, delimiter="\t"):
         docid = doc_entry[0]
         termid = doc_entry[1]
         tf = len(doc_entry[2:])
         sum_doclen += tf

         if doc_term.has_key(docid):
            doc_term[docid][0] += tf
   	    if doc_term[docid][1].has_key(termid):
	       doc_term[docid][1][termid] += tf
   	    else:
	       doc_term[docid][1][termid] = tf
         else:
            term_frq = {}
            doc_term[docid] = [tf]
   	    term_frq[termid] = tf
	    doc_term[docid].append(term_frq)


def OkapiTF(termid, tf, lenD, term):
   return (tf / (tf + 0.5 + (1.5 * (lenD / avg_doclen))))


def TFIDF(termid, tf, lenD, term):
   oktf = OkapiTF(termid, tf, lenD, term)
   return (oktf * math.log(num_doc / term_info[termid][1]))


def BM25(termid, tf, lenD, term):
   k1 = 1.2
   k2 = 100
   b = 0.75
   K = k1 * ((1-b) + (b * lenD / avg_doclen))

   T1 = math.log((num_doc + 0.5) / (term_info[termid][1] + 0.5))
   T2 = ((1 + k1) * tf) / (K + tf)
   T3 = (1 + k2) * Qtf[term] / (k2 + Qtf[term])
   return (T1 * T2 * T3)


def Laplace(termid, tf, lenD, term):
   Pd = (tf + 1) / (lenD + sum_doclen)
   return math.log(Pd)


def JM(termid, tf, lenD, term):
   Pd = (lmbda * tf / lenD) + ((1 - lmbda) * term_info[termid][0] / sum_doclen)
   return math.log(Pd)


Rank_function = {"TF" : OkapiTF,
        "TF-IDF" : TFIDF,
	"BM25" : BM25,
	"Laplace" : Laplace,
	"JM" : JM}


def Rank(query_list):
   global Qvector
   global doc_score
   global Qtf
   Qvector = {}
   for query in query_list:
      ### Calculate the Query oktf(q,i). ###
      Qvector = {}
      doc_score = {}
      Qwords = query[1].split()
      Qtf = {}
      Qvector = {}
      for word in Qwords:
         if Qtf.has_key(word):
            Qtf[word] = Qtf[word] + 1
         else:
            Qtf[word] = 1
      for word in Qwords:
         Qvector[word] = Qtf[word] / (Qtf[word] + 0.5 + 1.5)

      #if query[0] == "227":
      #   print query[0]
      #   print Qvector

      ### Calculate the Document D oktf(d,i) for each term i in query. ###
      for docid, doc_name in doc_hash.items():
         score = 0
	 d_q = 0
	 d2 = 0
	 q2 = 0
	 lenD = doc_term[docid][0]
         for term, qj in Qvector.items():
	    if term_hash.has_key(term):
	       termid = term_hash[term]
	       term_freq =  doc_term[docid][1]
	       if term_freq.has_key(termid):
                  tf = term_freq[termid]
                  di = Rank_function[sys.argv[2]](termid, tf, lenD, term)
		  #print di
		  if sys.argv[2] == "BM25" or sys.argv[2] == "Laplace" or sys.argv[2] == "JM":
		     score += di
		  else:
	             d_q += di * qj
	             q2 += qj * qj
	 
	 if sys.argv[2] == "TF" or sys.argv[2] == "TF-IDF":
            for term, di in doc_term[docid][1].items():
	       d2 += di * di
	    if d2 != 0 and q2 != 0:
	       score = d_q / math.sqrt(d2 * q2)
	       doc_score[docid] = score
	 elif score != 0:
	    doc_score[docid] = score

      rank = 1
      for docid in sorted(doc_score, key=doc_score.get, reverse=True):
         print query[0] + " 0 " + doc_hash[docid] + " " + str(rank) + " " + str(doc_score[docid]) + " " + sys.argv[2]
	 rank += 1




if len(sys.argv) == 3:
   if sys.argv[1] == "--score" and Rank_function.has_key(sys.argv[2]):
      create_doc_hash()
      create_term_hash()
      create_doc_term()
      create_term_info()

      avg_doclen = sum_doclen/num_doc

      ignore_file = open("ignore_tokens.txt")
      ignore_tokens = list(ignore_file.read().split())

      query_list = []
      xmldoc = minidom.parse('topics.xmls')
      itemlist = xmldoc.getElementsByTagName('topic')
      for s in itemlist:
         qnumber = s.attributes['number'].value
         Q = s.getElementsByTagName('query').item(0).childNodes[0].data.lower()
	 Qwords = Q.split(' ')
	 stem_words = []
	 query_str = ''
	 for w in Qwords:
	    if w not in ignore_tokens:
	       stem_word = stem(w)
	       stem_words.append(stem_word)
         query_str = ' '.join(stem_words)
	 query = [qnumber, query_str]
         query_list.append(query)

      Rank(query_list)
   else:
      incorrect_usage()
else:
   incorrect_usage()
