#!/usr/bin/python

import numpy as nm
from random import randint

class TrafficMatrix:

    def __init__(self,noOfTors=10, noOfServ=10, bw=1, factor=1, k=4):
        self.noOfTors = noOfTors;
        self.noOfServ = noOfServ;
        self.bw = bw;
        self.factor = factor;
        self.k = k

    ''' Gets Traffic Matrix based on Zipf distribution'''
    def GetZipfArray(self):
        a = 2.5
        mat = nm.random.zipf(a,(self.noOfTors,self.noOfTors,self.noOfServ*self.noOfServ))
        rand = 50*randint(1,5)
        mat = nm.round(mat,-1)
        for i in range(len(mat)):
          mat[i] = mat[i]%(rand)
          
        i = 0
        for u in mat:
          j = 0 
          
          if u.sum() >1000*self.k:
            print "ERROR: exceeding cap", u.sum()
          
          for v in u:
            
            
            if v.sum() >1000:
              print "ERROR: exceeding cap"
            j=j+1
          i = i +1
        
          
        
        return mat * self.factor

''' Test code'''
'''
TestObj = TrafficMatrix(bw =2, factor = 3)
print TestObj.GetZipfArray()
print TestObj.GetZipfArray()


'''
