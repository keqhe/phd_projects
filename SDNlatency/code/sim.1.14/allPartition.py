import networkx as nx
from topoManager import *
import fatTree
from time import *
from ruleDepDAG import *
from edgePartition import *
#import matplotlib.pyplot as plt

class allPartition:

  def __init__(self, rulesPerEdge, edgeSws, topo, taggedPaths):
    self.rulesPerEdge  = rulesPerEdge
    self.edgeSws = edgeSws
    self.topo = topo 
    self.taggedPaths = taggedPaths
    self.aggPartitions = {}
    self.aggDefault = {}
    self.partitions = {}
    self.optaggPartitions = {}
    self.optaggDefault = {}
    self.calMaxRuleInEdge()
    self.optRules = 100000
  #
  # Add the rules in new partition (par) to the global partition (aggPartitions)
  #
  def aggregatePartitions(self,par):
    for swId in par.keys():
      if swId not in self.aggPartitions.keys():
        self.aggPartitions[swId] = {}
      for ruleNumber in par[swId]:
        self.aggPartitions[swId][ruleNumber] = par[swId][ruleNumber]
        #print "Adding Rule: " + str(ruleNumber) + " to switch: " + str(swId)


  def aggregateDefaultPartitions(self,par):
    for swId in par.keys():
      if swId not in self.aggDefault.keys():
        self.aggDefault[swId] = 0
      self.aggDefault[swId] =  self.aggDefault[swId] + par[swId]


  def calMaxRuleInEdge(self):
    self.maxRule = 0
    for sw in self.edgeSws:
      if sw not in self.rulesPerEdge.keys():
        print "Switch: "+ str(sw) + " has no rules"
        continue
       
      if self.maxRule < len(self.rulesPerEdge[sw].keys()):
        self.maxRule = len(self.rulesPerEdge[sw].keys())
    print "Max No of Rules is: ",self.maxRule

  def calMaxRule(self):
    maxRule = 0
    for sw in self.aggPartitions.keys():
      d = 0
      if sw in self.aggDefault.keys():
        d = self.aggDefault[sw]
      #print "Sw: ",sw, "Rules: ",len(self.aggPartitions[sw].keys()), d 
      if len(self.aggPartitions[sw].keys()) + d > maxRule:
        maxRule = len(self.aggPartitions[sw].keys()) + d
    return maxRule
  
  def printPar(self):
    count = 0
    for sw in self.aggPartitions.keys():
      d = 0
      if sw in self.aggDefault.keys():
        d = self.aggDefault[sw]
      print sw, len(self.aggPartitions[sw].keys()), d 
      count = count + len(self.aggPartitions[sw].keys())
    print "Total:", count
  # 
  # Create Partitions for each edge switches in edgeSws
  #
  def createPartitions(self):
    start = 0.8
    while True:
      for sw in (self.edgeSws):
        if sw not in self.rulesPerEdge.keys():
          print "Switch: "+ str(sw) + " has no rules"
          continue
        #print " Start Partition for: " + str(sw)
        rulesDag = ruleDepDAG(self.rulesPerEdge[sw])
        rulesDagToSend = copy.deepcopy(rulesDag)
        edgeParIns = edgePartition(sw, self.taggedPaths, rulesDagToSend, self.topo, int(self.maxRule*start))
        edgePar = edgeParIns.GetEdgePartitions()
        defaultRules = edgeParIns.GetDefaultRuleCount()
      
        self.aggregatePartitions(edgePar)
        self.aggregateDefaultPartitions(defaultRules)
      print start, "MaxRules: ",int(self.maxRule*start), "No of Rules: ", self.calMaxRule()
      #self.printPar()
      if self.optRules > self.calMaxRule():
        self.optaggPartitions = {}
        self.optaggDefault = {}
        self.optaggPartitions = copy.deepcopy(self.aggPartitions)
        self.optaggDefault = copy.deepcopy(self.aggDefault)
        self.optRules = self.calMaxRule()
        self.aggPartitions = {}
        self.aggDefault = {}
      start = start - 0.05
      if start < 0.50:
        #print "-----------------------EdGe ",sw,len(self.aggPartitions[sw].keys())
        break

    return self.optaggPartitions, self.optaggDefault

