#!/usr/bin/python

from __future__ import division

import math
import operator
import itertools
import collections
import csv
import sys

users = {}
dev_users = {}
test_users = {}
user_votes = {}
user_votes2 = {}
user_dist = {}

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
   exit

with open('HW3_data/train.csv') as f:
    for data in csv.reader(f):
       movieid = int(data[0])
       userid = int(data[1])
       vij = int(data[2])

       if users.has_key(userid):
          users[userid][movieid] = vij
       else:
          users[userid] = {}
          users[userid][movieid] = vij

with open('HW3_data/dev.csv') as f:
    for data in csv.reader(f):
       movieid = int(data[0])
       userid = int(data[1])
       vij = int(data[2])

       if users.has_key(userid):
          users[userid][movieid] = vij
       else:
          users[userid] = {}
          users[userid][movieid] = vij


with open('HW3_data/test.csv') as f:
    for data in csv.reader(f):
       movieid = int(data[0])
       userid = int(data[1])
       vij = int(data[2])

       if users.has_key(userid):
          users[userid][movieid] = vij
       else:
          users[userid] = {}
          users[userid][movieid] = vij


with open('HW3_data/dev.queries') as f:
    for data in csv.reader(f):
       userid = int(data[1])
       dev_users[userid] = 1

with open('HW3_data/test.queries') as f:
    for data in csv.reader(f):
       userid = int(data[1])
       test_users[userid] = 1


for user in users:
   vij = 0.0
   vij2 = 0.0
   n = 0.0
   for movie in users[user]:
      vij += users[user][movie]
      vij2 += users[user][movie]**2
      n += 1
   user_votes[user] = vij / n
   user_votes2[user] = math.sqrt(vij2)

'''for user in test_users:
   vij = 0
   vij2 = 0
   n = 0
   for movie in users[user]:
      vij += users[user][movie]
      vij2 += users[user][movie]**2
      n += 1
   user_votes[user] = vij / n
   user_votes2[user] = math.sqrt(vij2)'''


print "Starting with Cosine distances."
flag = False

for a in dev_users:
   if users.has_key(a):
      a_movies = list(users[a].keys())
   else:
      flag = True
      a_movies = list(users[default].keys())
   user_dist[a] = {}
   temp = {}
   sorted_users = collections.OrderedDict()
   for i in users:
      if a != i:
         w_ai = 0.0
         i_movies = list(users[i].keys())
	 ai_movies = list(set(a_movies).intersection(i_movies))
	 if flag == False:
	    for movie in ai_movies:
	       w_ai += (users[a][movie] * users[i][movie]) / (user_votes2[a] * user_votes2[i])
	 else:
	    w_ai = default_dist
	 temp[i] = w_ai
   user_dist[a] = dict(sorted(temp.iteritems(), key=operator.itemgetter(1), reverse=True)[:k])
   print a, user_dist[a]

print "Done with Cosine distances for dev_users."
flag = False

for a in test_users:
   if user_dist.has_key(a):
      print a, user_dist[a]
   else:
      if users.has_key(a):
         a_movies = list(users[a].keys())
      else:
         flag = True
         a_movies = list(users[default].keys())

      user_dist[a] = {}
      temp = {}
      sorted_users = collections.OrderedDict()
      for i in users:
         if a != i:
            w_ai = 0.0
            i_movies = list(users[i].keys())
            ai_movies = list(set(a_movies).intersection(i_movies))
   	    if flag == False:
               for movie in ai_movies:
                  w_ai += (users[a][movie] * users[i][movie]) / (user_votes2[a] * user_votes2[i])
            else:
	       w_ai = default_dist
      	    temp[i] = w_ai
      user_dist[a] = dict(sorted(temp.iteritems(), key=operator.itemgetter(1), reverse=True)[:k])
      print a, user_dist[a]
   
print "Done with Cosine distances for test_users."


# Calculate Predicted rating for queries.

dev_file = "p1-k" + str(k) + "-" + pred_method + "-dev.txt"
dev_op = open(dev_file, 'w')

with open('HW3_data/dev.queries') as f:
    for data in csv.reader(f):
       movieid = int(data[0])
       userid = int(data[1])
       va = 0
       vi = 0
       if user_votes.has_key(userid):
          va = user_votes[userid]
       else:
          va = -2
       mean = 0

       if pred_method == "Mean":
          for i, vij in user_dist[userid].items():
	     vi = user_votes[i]
             if users[i].has_key(movieid):
                mean += (vij - vi)
	     else:
	        mean += (vi - 2)
       elif pred_method == "WMean":
          for i, vij in user_dist[userid].items():
	     vi = user_votes[i]
             if users[i].has_key(movieid):
                mean += user_dist[userid][i] * (vij - vi)
	     else:
	        mean += user_dist[userid][i] * (vi - 2)
       pred_rating = int(round(va + (mean / k)))
       if pred_rating < 0:
          pred_rating = 0
       elif pred_rating > 5:
          pred_rating = 5
       rating_str = str(pred_rating) + "\n"
       dev_op.write(rating_str)
       print pred_rating
dev_op.close()


test_file = "p1-k" + str(k) + "-" + pred_method + "-test.txt"
test_op = open(test_file, 'w')

with open('HW3_data/test.queries') as f:
    for data in csv.reader(f):
       movieid = int(data[0])
       userid = int(data[1])
       va = 0
       vi = 0
       if user_votes.has_key(userid):
          va = user_votes[userid]
       else:
          va = -2
       mean = 0

       if pred_method == "Mean":
          for i, vij in user_dist[userid].items():
             vi = user_votes[i]
             if users[i].has_key(movieid):
                mean += (vij - vi)
             else:
                mean += (vi - 2)
       elif pred_method == "WMean":
          for i, vij in user_dist[userid].items():
             vi = user_votes[i]
             if users[i].has_key(movieid):
                mean += user_dist[userid][i] * (vij - vi)
             else:
                mean += user_dist[userid][i] * (vi - 2)
       pred_rating = int(round(va + (mean / k)))
       if pred_rating < 0:
          pred_rating = 0
       elif pred_rating > 5:
          pred_rating = 5
       rating_str = str(pred_rating) + "\n"
       test_op.write(rating_str)
       print pred_rating
test_op.close()



