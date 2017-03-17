from __future__ import division
import math
import numpy as np
import os, sys, commands
#from scipy.optimize import curve_fit
from collections import defaultdict
from netaddr import *
class parseClassBench:

  def __init__(self): 
    self.dirname = "./"
    self.filename = "x"

    self.fullpath = self.dirname + self.filename
    self.dst = defaultdict(list)
    self.extractData()

  def extractData(self):   
    #print "Extracting data from" + self.fullpath
    count = 0
    for line in open(self.fullpath):
      line = line.strip()
      if len(line) == 0:
        continue
      count = count + 1
      words = line.split()
      self.dst[words[0][1:]].append(IPNetwork(words[1]))
    #print self.dst  
    #for key in sorted(self.dst.keys()):
    #  print key, self.dst[key] 
    #print len(self.dst.keys())
    #print self.same_prio
    #print self.decr_prio
    #print self.incr_prio
    
  def getRules(self):
    return self.dst

#Test code"   
def main():
  bm = parseClassBench()

if __name__ == "__main__":
    main()
