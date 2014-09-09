#!/usr/bin/python

from __future__ import division

import math
import operator
import itertools
import collections
import csv
import sys

movies = {}
dev_movies = {}
test_movies = {}
movie_votes = {}
movie_votes2 = {}
movie_dist = {}

default = 1086
default_dist = 1.0 / 3


def incorrect_usage():
   print "Incorrect Usage."
   print "Usage:"
   print "./pr1.py --method [Mean/WMean] --K [Number]"

if len(sys.argv) != 5:
   incorrect_usage()
   exit()

pred_method = sys.argv[2]
k = int(sys.argv[4])

if pred_method != "Mean" and pred_method != "WMean":
   incorrect_usage()
   exit()

with open('HW3_data/train.csv') as f:
    for data in csv.reader(f):
       movieid = int(data[0])
       userid = int(data[1])
       vij = int(data[2])

       if movies.has_key(movieid):
          movies[movieid][userid] = vij
       else:
          movies[movieid] = {}
          movies[movieid][userid] = vij

with open('HW3_data/dev.csv') as f:
    for data in csv.reader(f):
       movieid = int(data[0])
       userid = int(data[1])
       vij = int(data[2])

       if movies.has_key(movieid):
          movies[movieid][userid] = vij
       else:
          movies[movieid] = {}
          movies[movieid][userid] = vij


with open('HW3_data/test.csv') as f:
    for data in csv.reader(f):
       movieid = int(data[0])
       userid = int(data[1])
       vij = int(data[2])

       if movies.has_key(movieid):
          movies[movieid][userid] = vij
       else:
          movies[movieid] = {}
          movies[movieid][userid] = vij


with open('HW3_data/dev.queries') as f:
    for data in csv.reader(f):
       movieid = int(data[0])
       dev_movies[movieid] = 1

with open('HW3_data/test.queries') as f:
    for data in csv.reader(f):
       movieid = int(data[0])
       test_movies[movieid] = 1


for movie in movies:
   vij = 0.0
   vij2 = 0.0
   n = 0.0
   for user in movies[movie]:
      vij += movies[movie][user]
      vij2 += movies[movie][user]**2
      n += 1
   movie_votes[movie] = vij / n
   movie_votes2[movie] = math.sqrt(vij2)

'''for movie in test_movies:
   vij = 0
   vij2 = 0
   n = 0
   for movie in movies[movie]:
      vij += movies[movie][movie]
      vij2 += movies[movie][movie]**2
      n += 1
   movie_votes[user] = vij / n
   movie_votes2[user] = math.sqrt(vij2)'''


print "Starting with Cosine distances."
flag = False

for a in dev_movies:
   if movies.has_key(a):
      a_users = list(movies[a].keys())
   else:
      flag = True
      a_users = list(movies[default].keys())
   movie_dist[a] = {}
   temp = {}
   sorted_movies = collections.OrderedDict()
   for i in movies:
      if a != i:
         w_ai = 0.0
         i_users = list(movies[i].keys())
	 ai_users = list(set(a_users).intersection(i_users))
	 if flag == False:
	    for user in ai_users:
	       w_ai += (movies[a][user] * movies[i][user]) / (movie_votes2[a] * movie_votes2[i])
	 else:
	    w_ai = default_dist
	 temp[i] = w_ai
   movie_dist[a] = dict(sorted(temp.iteritems(), key=operator.itemgetter(1), reverse=True)[:k])
   print a, movie_dist[a]

print "Done with Cosine distances for dev_movies."
flag = False

for a in test_movies:
   if movie_dist.has_key(a):
      print a, movie_dist[a]
   else:
      if movies.has_key(a):
         a_users = list(movies[a].keys())
      else:
         flag = True
         a_users = list(movies[default].keys())

      movie_dist[a] = {}
      temp = {}
      sorted_movies = collections.OrderedDict()
      for i in movies:
         if a != i:
            w_ai = 0.0
            i_users = list(movies[i].keys())
            ai_users = list(set(a_users).intersection(i_users))
   	    if flag == False:
               for user in ai_users:
                  w_ai += (movies[a][user] * movies[i][user]) / (movie_votes2[a] * movie_votes2[i])
            else:
	       w_ai = default_dist
      	    temp[i] = w_ai
      movie_dist[a] = dict(sorted(temp.iteritems(), key=operator.itemgetter(1), reverse=True)[:k])
      print a, movie_dist[a]
   
print "Done with Cosine distances for test_movies."


# Calculate Predicted rating for queries.

dev_file = "p2-k" + str(k) + "-" + pred_method + "-dev.txt"
dev_op = open(dev_file, 'w')

with open('HW3_data/dev.queries') as f:
    for data in csv.reader(f):
       movieid = int(data[0])
       userid = int(data[1])
       if movie_votes.has_key(movieid):
          va = movie_votes[movieid]
       else:
          va = -2
       mean = 0

       if pred_method == "Mean":
          for i, vij in movie_dist[movieid].items():
	     vi = movie_votes[i]
             if movies[i].has_key(userid):
                mean += (vij - vi)
	     else:
	        mean += (vi - 2)
       elif pred_method == "WMean":
          for i, vij in movie_dist[movieid].items():
	     vi = movie_votes[i]
             if movies[i].has_key(userid):
                mean += movie_dist[movieid][i] * (vij - vi)
	     else:
	        mean += movie_dist[movieid][i] * (vi - 2)
       pred_rating = int(round(va + (mean / k)))
       rating_str = str(pred_rating) + "\n"
       dev_op.write(rating_str)
       print pred_rating
dev_op.close()


test_file = "p2-k" + str(k) + "-" + pred_method + "-test.txt"
test_op = open(test_file, 'w')

with open('HW3_data/test.queries') as f:
    for data in csv.reader(f):
       movieid = int(data[0])
       userid = int(data[1])
       if movie_votes.has_key(movieid):
          va = movie_votes[movieid]
       else:
          va = -2
       mean = 0

       if pred_method == "Mean":
          for i, vij in movie_dist[movieid].items():
             vi = movie_votes[i]
             if movies[i].has_key(userid):
                mean += (vij - vi)
             else:
                mean += (vi - 2)
       elif pred_method == "WMean":
          for i, vij in movie_dist[movieid].items():
             vi = movie_votes[i]
             if movies[i].has_key(userid):
                mean += movie_dist[movieid][i] * (vij - vi)
             else:
                mean += movie_dist[movieid][i] * (vi - 2)
       pred_rating = int(round(va + (mean / k)))
       rating_str = str(pred_rating) + "\n"
       test_op.write(rating_str)
       print pred_rating
test_op.close()



