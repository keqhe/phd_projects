from __future__ import division
import math
import numpy as np
import os, sys, commands
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

class bcmBurstModel:

  def __init__(self, prioOrder=0, L=0): #0: Same Prio, -1: Decr Prio, 1: Incr Prio, L is the number of lower priority rules in the switch
    self.prioOrder = prioOrder
    self.L = L
    if prioOrder == 0: 
      self.dirname = "../../data/BCM_JAN9/burstSize/"
      self.filename = "bcm_burst_size_effects.txt"
    elif prioOrder == 1:
      self.dirname = "../../data/BCM_JAN9/burstSize_Incr/"
      self.filename = "bcm_burst_size_effects.txt"
    elif prioOrder == -1:
      self.dirname = "../../data/BCM_JAN9/burstSize_Decr/"
      self.filename = "bcm_burst_size_effects.txt"

    self.fullpath = self.dirname + self.filename
    self.data = {}
    self.displacement = {}
    self.extractData()
    self.fitCurve()

  def extractData(self):   
    #print "Extracting data from" + self.fullpath
    for line in open(self.fullpath):
      line = line.strip()
      words = line.split()
      if self.prioOrder == -1 and int(words[0]) >= 400: # The decr prio data is arbitary. Filter out larger values
        continue
      self.data[int(words[0])] = float(words[1])
    #print self.data

  def fitCurve(self):
    x = sorted(self.data.keys())
    y = sorted(self.data.values())
    z = np.polyfit(x,y,6)
    print z
    self.func = np.poly1d(z)
    #print self.func
    #plt.plot(x,y,'o',x,y)
    #plt.xlim(x[0]-1,x[-1]+1)
    #plt.show()
    #for i in x:
    #  print i, self.func(i)
 
  def getBurstCompletionTime(self,burstSize, L=0):
    if burstSize == 0:
      return 0
    #for line in open('../../data/rule_displacement_model_data/displacement.txt'): #a rush file open :(
	#line = line.strip()
	#words = line.split()
	#u = int(words[0])
	#v = float(words[1])
	#self.displacement[u] = v
    #x = sorted(self.displacement.keys())
    #y = sorted(self.displacement.values())
    #z = np.polyfit(x,y,1)
    #print z
    #temp = np.poly1d(z)
    #print temp
    return self.func(burstSize) + 14.9*L  ##hard coded

#Test code"   
def main():
  bm = bcmBurstModel(0)
  print "25", bm.getBurstCompletionTime(25)
  print "30", bm.getBurstCompletionTime(30)
  print "75", bm.getBurstCompletionTime(75)
  print "85", bm.getBurstCompletionTime(85)
  print "100", bm.getBurstCompletionTime(100, L=100)
  print "550", bm.getBurstCompletionTime(550)

if __name__ == "__main__":
    main()
