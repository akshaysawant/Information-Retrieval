#!/usr/bin/python

import os
import sys
import re
import collections
from bs4 import BeautifulSoup
from stemming.porter import stem

path = sys.argv[1]
docid = 1
termid = 1
all_tokens = {}
seek_index = collections.OrderedDict()


def tokenize(file):
   current = os.path.join(path, file)
   print current

   f = open(current,'rU')
   lines = f.read()
   lines = lines.lower()
   html_list = lines.split("content-type: ")[2:]
   html_docs=''
   for line in html_list:
      html_docs = html_docs + '\n' + line

   html_docs = unicode(html_docs, "utf-8", errors="ignore")
   soup = BeautifulSoup(html_docs)
   [s.extract() for s in soup('script')]
   html_doc_only_text = soup.get_text()
   wordList = re.findall("(\w+(\.\w+)*)", html_doc_only_text)
   return wordList


ignore_file = open("ignore_tokens.txt")
ignore_tokens = list(ignore_file.read().split())

f_docids = open("docids.txt", "w")
f_termids = open("termids.txt", "w")
f_doc_index = open("doc_index.txt", "w")
f_doc_read = open("doc_index.txt", "r")

for file in os.listdir(path):
   docid_str = file + '\t' + str(docid) + '\n'
   f_docids.write(docid_str)
   count = 1
   wordList = tokenize (file)

   doc_words = collections.OrderedDict()
   stem_list = []
   for word in wordList:
      stem_word = stem(word[0])
      if stem_word not in doc_words.keys() and word[0] not in ignore_tokens:
         doc_words[stem_word] = 1
	 if stem_word not in all_tokens.keys():
	    all_tokens.update({stem_word : termid})
            termid_str = ''.join([stem_word, '\t', str(termid), '\n'])
            f_termids.write(termid_str)
	    termid += 1
      stem_list.append(stem_word)

   for token in doc_words:
      doc_idx_str = ''.join([str(docid), '\t', str(all_tokens[token])])
      position = 1
      for s in stem_list:
         if token == s:
	    doc_idx_str = ''.join([doc_idx_str.strip(), '\t', str(position)])
	 position += 1
      doc_idx_str = ''.join([doc_idx_str, '\n'])
      f_doc_index.write(doc_idx_str)

   docid += 1

f_docids.close()
f_termids.close()
f_doc_index.close()
print docid
