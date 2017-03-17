from __future__ import division
import math
import numpy as np
import os, sys, commands
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

class ciscoBurstModel:

  def __init__(self): 
    self.dirname = "../../data/cisco_jan19/"
    self.filename = "compare_priority.txt"

    self.fullpath = self.dirname + self.filename
    self.same_prio = {}
    self.incr_prio = {}
    self.decr_prio = {}
    self.extractData()
    self.fitCurve()

  def extractData(self):   
    #print "Extracting data from" + self.fullpath
    count = 0
    for line in open(self.fullpath):
      count = count + 1
      if count == 1:
        continue  
      line = line.strip()
      if len(line) == 0:
        continue
      words = line.split()
      self.same_prio[int(words[0])] = float(words[1])
      self.decr_prio[int(words[0])] = float(words[2])
      self.incr_prio[int(words[0])] = float(words[3])
      
    #print self.same_prio
    #print self.decr_prio
    #print self.incr_prio
    

  def fitCurve(self):
    burst = sorted(self.same_prio.keys())
    same = sorted(self.same_prio.values())
    incr = sorted(self.incr_prio.values())
    decr = sorted(self.decr_prio.values())

    z = np.polyfit(burst,same,2)
    self.func_same = np.poly1d(z)

    z = np.polyfit(burst,incr,3)
    self.func_incr = np.poly1d(z)

    z = np.polyfit(burst,decr,3)
    self.func_decr = np.poly1d(z)

    #print self.func_same
    #print self.func_decr
    #print self.func_incr
    #plt.plot(x,y,'o',x,y)
    #plt.xlim(x[0]-1,x[-1]+1)
    #plt.show()
    #for i in self.same_prio.keys():
    #  print i, self.func_same(i)
 
  def getBurstComplTime_SamePrio(self,burstSize):
    if burstSize == 0:
      return 0;
    return self.func_same(burstSize)

  def getBurstComplTime_DecrPrio(self,burstSize):
    if burstSize == 0:
      return 0;
    return self.func_decr(burstSize)

  def getBurstComplTime_IncrPrio(self,burstSize):
    if burstSize == 0:
      return 0;
    return self.func_incr(burstSize)
'''
#Test code"   
def main():
  bm = burstModel(0)
  print "25", bm.getBurstComplTime_SamePrio(25)
  print "30", bm.getBurstComplTime_SamePrio(30)
  print "75", bm.getBurstComplTime_SamePrio(75)
  print "85", bm.getBurstComplTime_SamePrio(85)
  print "95", bm.getBurstComplTime_SamePrio(95)
  print "550", bm.getBurstComplTime_SamePrio(550)

if __name__ == "__main__":
    main()
''' 
