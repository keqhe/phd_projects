import networkx as nx
#import matplotlib.pyplot as plt
from ruleDepDAG import *

# Dummy file. Not used

class rulePartition:

  def __init__(self, edgeSwID, taggedPaths, dag, topo):
    self.dep = dag
    self.switchID = edgeSwID
    self.partition = {}
    self.partition[edgeSwID] = dag.ruleSet
    self.taggedPaths = taggedPaths
    self.topo = topo
    self.flowlimit = 800 # Limit of flow entries in switches
    self.constructPartitions(edgeSwID,1)
    #self.parDag = ruleDepDAG()

  #
  # Gets the next hop for rule k
  #
  def getNextHop(self,index,k):
    # Get the tag from the rule
    tag  = self.dep.dag.node[k]['tag']   
    # Get the path for tag from the tagged paths
    path = self.taggedPaths[tag] 
    # Terminal if end of path is reached
    # TODO: What should be the terminating condition? How many next hop to be explored?
    if index == len(path)-1:
      return -1
    return path[index]

  #
  # Construct partitions for switch: switchId
  #
  def constructPartitions(self,switchId,no):
    
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
        return;
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
        elif no == 1 and swRuleCount[nextHopSw] > self.flowlimit/self.topo.in_degree(nextHopSw):
          offload = False
        elif no > 1 and swRuleCount[nextHopSw] > self.flowlimit/(self.topo.in_degree(nextHopSw)*self.topo.in_degree(switchId)):
          offload = False
        else:
          swRuleCount[nextHopSw] = swRuleCount[nextHopSw] + 1         

      if offload == True:
        # Add RuleID = k  to the nextHopPartition
        if nextHopSw not in self.partition.keys():
          self.partition[nextHopSw] = {}

        self.partition[nextHopSw][k] = self.partition[switchId][k]
        updatedPartitions[nextHopSw] = True

        # Remove the offloaded rule from current partition
        del self.partition[switchId][k]

        print "Offloaded Rule: " + str(k) + " from switch: " + str(switchId) + " to switch: " + str(nextHopSw)  
      else:
        # Rule can not be offloaded. Mark it to prevent it dependencies (parent rules in DAG) to get offloaded
        self.dep.dag.node[k]['canOffload'] == False
      checkedRules[k] = True

    # Recursive calls for all the newly created Partitions          
    for key in updatedPartitions.keys(): 
      self.constructPartitions(key,no+1)       


