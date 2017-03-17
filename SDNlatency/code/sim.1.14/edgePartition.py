import networkx as nx
#import matplotlib.pyplot as plt
from ruleDepDAG import *
import copy
from defaultRules import*

class edgePartition:

  def __init__(self, edgeSwID, taggedPaths, dag, topo, maxRules):
    self.dep = dag
    self.switchID = edgeSwID
    self.partition = {}
    self.partition[edgeSwID] = dag.ruleSet
    self.taggedPaths = taggedPaths
    self.topo = topo
    self.maxRules = maxRules
    self.limit = 100 # Limit of flow entries in switches
    self.tablelimit = 3000000
    #self.parDag = ruleDepDAG()
    self.defaultRuless = {}
    
    self.constructOptimalPartitions(edgeSwID,1)

  #
  # Gets the next hop for rule k
  #
  def getNextHop(self,index,k):
    # Get the tag from the rule
    tag  = self.dep.dag.node[k]['tag']   
    # Get the path for tag from the tagged paths
    if str(tag) not in self.taggedPaths.keys():
      print "[Error]: tag:" + str(tag) + str(len(tag)) + "not found in the taggedPaths"
      return -1
    path = self.taggedPaths[tag] 
    # Terminal if end of path is reached
    # TODO: What should be the terminating condition? How many next hop to be explored?
    if index >= len(path)-1:
      return -1
    return path[index]

  #
  # Return the Partition
  #
  def GetEdgePartitions(self):
    return self.partition

  #
  # Optimal Partition
  #
  def constructOptimalPartitions(self,switchId,no):
    self.limit = self.maxRules
    #print "Starting with limit of: ",self.limit,switchId
    self.constructPartitions(switchId,no)
    #print "::::::::::: " + str(self.partition.keys())
    
  def GetDefaultRuleCount(self):
    return self.defaultRuless
  #
  # Construct partitions for switch: switchId
  #
  def constructPartitions(self,switchId,no):
    #print "___________________",switchId,len(self.partition[switchId].keys())
    updatedPartitions = {}
    checkedRules = {}
    swRuleCount = {}
    # Topological sort the dag
    rulenodes = self.dep.toposort()

    # Do the partition for rules of switchId 
    for k in reversed(rulenodes):

      # Find if rule #id k exists in the current Partition
      if k not in self.partition[switchId].keys():
        #print "Rule "+str(k)+ " not in partition of: "+str(switchId)
        continue 
 
      #print self.dep.dag.node[k]
      #print no,path,self.getNextHop(no,path)

      # Get the next hop Switch from the path
      nextHopSw = self.getNextHop(no,k)
      if nextHopSw == -1:
        self.dep.dag.node[k]['canOffload'] == True
        #print "Returning here"
        continue;
      #print nextHopSw, self.topo.out_degree(nextHopSw), self.topo.in_degree(nextHopSw) 
      offload = False

      # Offload Conditions
      # No dependicies set offload to true and start offload
      if self.dep.dag.out_degree(k) == 0:
         offload = True

      # If any dependent rule belongs to a diff next hop
      # Or if any dependent rule was not offloaded, stop offload 
      if offload == False:
        outdeg = self.dep.dag.successors(k)
        #print outdeg

        offload = True
        for x in outdeg:  
          if self.getNextHop(no,x) != nextHopSw or self.dep.dag.node[x]['canOffload'] == False:
            offload = False
            break

      # Check for the static nexthop rule quota
      # TODO: Account for default rules?
      if offload == True:
        if nextHopSw not in swRuleCount.keys():
          swRuleCount[nextHopSw] = 1
        elif no == 1 and swRuleCount[nextHopSw] > self.tablelimit/self.topo.in_degree(nextHopSw):
          offload = False
        elif no > 1 and swRuleCount[nextHopSw] > self.tablelimit/(self.topo.in_degree(nextHopSw)*self.topo.in_degree(switchId)):
          offload = False
        else:
          swRuleCount[nextHopSw] = swRuleCount[nextHopSw] + 1         
      
      if offload == True:
        # Add RuleID = k  to the nextHopPartition
        #print "OFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFf"
        if nextHopSw not in self.partition.keys():
          self.partition[nextHopSw] = {}

        self.partition[nextHopSw][k] = self.partition[switchId][k]
        updatedPartitions[nextHopSw] = True

        # Remove the offloaded rule from current partition
        del self.partition[switchId][k]
        
        #print "Offloaded Rule: " + str(k) + " from switch: " + str(switchId) + " to switch: " + str(nextHopSw)  
      else:
        # Rule can not be offloaded. Mark it to prevent it dependencies (parent rules in DAG) to get offloaded
        #print "Nothing to Offload"
        self.dep.dag.node[k]['canOffload'] = False
      checkedRules[k] = True

    if (len(updatedPartitions.keys()) == 0):
      return;
    #print "Check Rule Count: ",switchId, len(self.partition[switchId].keys())
    # copying the partition for getDefaultRules
    partPerSwitch = {}
    for key in updatedPartitions.keys():
      partPerSwitch[key] = copy.deepcopy(self.partition[key])
      #print " PArt: ",key, len(self.partition[key].keys())
    # computing default rules
    #print "computing default rules, switch, ",switchId 
    newpartitions, newRootrules, newdefaultSet, default = getDefaultRules(partPerSwitch)
    
    #print "Printing what Junaid returned"
    #print "Default Rules"
    #for key in newdefaultSet.keys():
      #print newdefaultSet[key]
    #for key in newpartitions.keys():
      #print ""
      #print "Partition: ",key
      #for rule in newpartitions[key]:
        #print rule.number,
    #print "\nFinished Printing what Junaid returned"

    # Push these rules back to the root
    for key in newRootrules:
      for newRule in newRootrules[key]:
        self.partition[switchId][newRule.number] = newRule
        self.dep.dag.node[newRule.number]['canOffload'] = False

    # Calulate the room left in root partition
    y = 1
    if no > 1: # means no a edge switch
      y = y * self.topo.in_degree(switchId)
  
    roomLeft = self.limit/y - len(self.partition[switchId].keys()) 
    #print self.limit,y,len(self.partition[switchId].keys()) ,no
    #print "Room: ",roomLeft
    
    # If room is left check if some offloaded rules can still be moved to the root 
    while roomLeft !=0 and roomLeft - len(newdefaultSet.keys()) >= 0 and len(newdefaultSet.keys()) > 0:
      
      shortestRuleCount = 10000
      shortestkey = 0
      # Get the shortest rule set and try to fit it in the root
      for key in newdefaultSet.keys():
        if len(newdefaultSet[key]) < shortestRuleCount:
          shortestRuleCount = len(newdefaultSet[key])
          shortestkey = key

      #print  "Shortest: ", shortestRuleCount,newdefaultSet[shortestkey],shortestkey

      if roomLeft == len(newdefaultSet.keys()) and shortestRuleCount != 1:
        #print "Returning"
        break

      if len(newdefaultSet[shortestkey]) + len(newdefaultSet.keys()) - 1 > roomLeft:
        for key in newdefaultSet.keys():
          if len(newdefaultSet[key]) > shortestRuleCount:
            shortestRuleCount = len(newdefaultSet[key])
            shortestkey = key
        #print  "Largest: ", shortestRuleCount,newdefaultSet[shortestkey],shortestkey


      if ( len(newdefaultSet.keys())) <= roomLeft:
        #print "Moving some rules further to root-------------------------------", switchId
        # get any rule no
        ruleno = newdefaultSet[shortestkey][0]
        #print "Hi: ", ruleno
        for key in newpartitions.keys():
          searchkey = 0
          for rule in newpartitions[key]:
            #print "hi",rule.number 
            if rule.number == ruleno:
              #print "found",key,ruleno
              searchkey = key
              break
          if searchkey == 0:
            continue
          count = 0
          for k in range(0,1):#len(newdefaultSet[shortestkey])):
            for rule in newpartitions[searchkey]:
              #print rule.number
              if rule.number == newdefaultSet[shortestkey][k] and roomLeft >= len(newdefaultSet.keys()):
                #print "Pushing: ", newdefaultSet[shortestkey][k]
                self.partition[switchId][newdefaultSet[shortestkey][k]] = rule
                lst = newpartitions[searchkey]
                #print lst
                lst.remove(rule)
                roomLeft = roomLeft - 1
                self.dep.dag.node[rule.number]['canOffload'] = False
                #print "Room:",roomLeft
                count = count + 1
          #print "count",count
          for k in range(0,count):
            #print k
            newdefaultSet[shortestkey].pop(0)
            
          if len(newpartitions[searchkey]) == 0:
            del newpartitions[searchkey]
          
        if len(newdefaultSet[shortestkey]) == 0:
          del newdefaultSet[shortestkey]
      else:
        break  
    #print "Finally : ", len( self.partition[switchId].keys()), len(newdefaultSet.keys())
    if switchId not in self.defaultRuless:
      self.defaultRuless[switchId] = len(newdefaultSet.keys())
    else:self.defaultRuless[switchId] = len(newdefaultSet.keys()) + self.defaultRuless[switchId]

    '''
    for key in updatedPartitions.keys():
      for rule in self.partition[key]:
        self.partition[key][rule].printRule()
    '''
    #updating patitions
    for key in updatedPartitions.keys():
      self.partition[key] = {}

      if key in newpartitions:
        for newRule in newpartitions[key]:
          self.partition[key][newRule.number] = newRule
          #newRule.printRule()
    #  print "After ",self.partition[key].keys(),len(self.partition[key].keys())

    #updating root patition
   # print "before",self.partition[switchId].keys(), len(self.partition[switchId].keys())   
    for key in newRootrules:
      for newRule in newRootrules[key]:
        self.partition[switchId][newRule.number] = newRule
        self.dep.dag.node[newRule.number]['canOffload'] = False

        if len(self.dep.dag.predecessors(newRule.number)) != 0:
          #print "Move the neighbor to ROOT +++++++++++++++++++++++++++++++++++"
          #print "Neighbor ",self.dep.dag.predecessors(newRule.number),"node",newRule.number
          for key in updatedPartitions.keys(): 
            for ruleNumber in self.dep.dag.predecessors(newRule.number):
              if ruleNumber in self.partition[key]:
                self.partition[switchId][ruleNumber] = self.partition[key][ruleNumber]
                del self.partition[key][ruleNumber]
    

      
    # Recursive calls for all the newly created Partitions          
    for key in updatedPartitions.keys(): 
      self.constructPartitions(key,no+1)       


