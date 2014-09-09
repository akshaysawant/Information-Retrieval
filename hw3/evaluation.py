#!/usr/bin/python
from __future__ import division
import sys
import argparse
from itertools import izip_longest
import math

def rmse(query_file,run_file,verb):
    """Root Mean Squared Error between a QREL and Run"""
    ret = 0
    cnt = 0
    with open(query_file) as qh, open(run_file) as rh:
      for exp, act in izip_longest(qh,rh):
        try:
          exp = float(exp.strip())
          act = float(act.strip())
        except AttributeError,e:
          print "Answers and run files are not the same length"
          sys.exit(1)
        except ValueError,e:
          print "Run (or answer) file contains invalid data"
          print e
          sys.exit(1)
        sqe = (exp - act) ** 2
        if verb:
          print "%0.4f" % sqe
        ret += sqe
        cnt += 1

    ret = math.sqrt(ret/cnt)
    print "Root Mean Squared Error: %0.4f" % ret

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('answers_path', help='path to qrel file')
    parser.add_argument('run_path', help='path to run file')
    parser.add_argument('-v', '--verbose', help='display score for each pair', action='store_true')
    args = parser.parse_args()

    rmse(args.answers_path, args.run_path, args.verbose)
