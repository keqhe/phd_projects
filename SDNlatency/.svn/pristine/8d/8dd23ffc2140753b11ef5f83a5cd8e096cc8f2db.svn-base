from random import choice
import networkx as nx
from random import *
import copy
import math
import copy
from defaultRules import*

class Failover():

  def __init__(self,Nodes):
    print "base Case | base Case w/o Edges | FlowEngineering |FlowEngineering w/o Edges| flowengineering + flow Offload "

    for k in range(0,15):
      self.failOver(Nodes)

  def failOver(self,Nodes):
    # k number of ports on each switch

    self.topo = nx.DiGraph()
    self.topo.add_edges_from(self.getEdge(Nodes), type = 'tunnels')
    cap = 900
    self.NMaxEnt = 4000
    self.complThres = 200

    nodes = self.topo.node
    for k in nodes:
      #randomly assigning popularity index
      nodes[k]['ps_index'] = randint(10,25)
      nodes[k]['pd_index'] = randint(10,25)

    edges = self.topo.edge
    for src in edges.keys():
      for dst in edges[src].keys():
        # randomly assigning tunnels bandwidth
        # cap = 1 - w
        edges[src][dst]['w'] = randint(100,cap)

    TM = {}
    self.ruleReset()
    for src in nodes:
      for dst in nodes:
        if src != dst:
          if src not in TM:
            TM[src] = {}
          TM[src][dst]= nodes[src]['ps_index'] * nodes[dst]['pd_index']

    #print TM
    #print self.topo.edge
    firstNode = choice(self.topo.nodes())
    secondNode = choice(self.topo.nodes())
    
    while secondNode == firstNode:
      secondNode = choice(self.topo.nodes())

    #print firstNode, secondNode
    #print self.topo.edge[firstNode][secondNode]
    totalVol = self.mapTraffic(TM,self.topo.node,self.topo.edge)
    self.assignpriorityrules()
    
#    print self.topo.edge
#    print self.topo.edge[firstNode][secondNode]
    if totalVol == 0:
      TM = self.tunnelFailure(self.topo.edge[firstNode][secondNode],firstNode, secondNode,TM)
      self.topo.remove_edge(firstNode,secondNode) 
      #print self.computePaths(firstNode,secondNode)
      #reschedule flows
      # send a copy
      #print self.computePaths(firstNode,secondNode)
      TM1 = copy.deepcopy(TM)
      topo1 = copy.deepcopy(self.topo)
       
      edgeNodes, remainingVol= self.rescheduleFlows(TM)
      if remainingVol !=0:
        return
      #print edgeNodes
      maxR = self.maxRules()
      maxER = self.maxRules_withoutEdge(edgeNodes)
      maxCR = self.getTotalCompletionTime()
      maxCER = self.getTotalCompletionTime_withoutEdge(edgeNodes)

      self.topo = topo1
      TM = TM1
      edgeNodes, remainingVol = self.rescheduleFlowsNMaxEnt(TM)
      if remainingVol != 0:
        return
      #print edgeNodes
      #print "base Case | base Case w/o Edges | FlowEngineering |FlowEngineering w/o Edges| flowengineering + flow Offload "
      print maxR,maxER, self.maxRules(),self.maxRules_withoutEdge(edgeNodes),
      self.assignTunnelSWs()
      self.assignRules()
      maxx, compl =  self.ruleOffload()
      print maxx
      print maxCR,maxCER, self.getTotalCompletionTime(),self.getTotalCompletionTime_withoutEdge(edgeNodes),compl
      


  def rescheduleFlowsNMaxEnt(self,TM):

    totalVol = 0
    for i in TM:
      for j in TM[i]:
        totalVol = totalVol + TM[i][j]
    print "NMaxEnt"        
    
    oldVol = 0
    edgeNodes = []
    while oldVol != totalVol:
      oldVol = totalVol
      for src in self.topo.node:
        for dst in self.topo.node:

          volumeTran = 0
          if src != dst and TM[src][dst] != 0:
            # Get the path in greedy order
            p = self.computePaths(src,dst)
            # if capacity is 0
            if p[0][1] ==0:
                continue
              
            selectedPath, ruleToInstall = self.selectPath(p)
            #print selectedPath
            if selectedPath == None:
              print "ERRRRR"
              continue
            for k in range(len(selectedPath[0])-1):
              e1 = selectedPath[0][k]
              e2 = selectedPath[0][k+1]
              
              # Min of ruleToInstall, Traffic to map, 
              volumeTran = min(ruleToInstall,TM[src][dst],selectedPath[1])

              
              self.topo.edge[e1][e2]['w'] \
                =  self.topo.edge[e1][e2]['w'] - volumeTran
              
              if 'flows' not in self.topo.edge[e1][e2]:
                self.topo.edges[e1][e2]['flows'] = {}

              
              #print volumeTran, ruleToInstall,TM[src][dst],selectedPath[1]
              if tuple(selectedPath[0]) not in self.topo.edge[e1][e2]['flows']:
                self.topo.edge[e1][e2]['flows'][tuple(selectedPath[0])] = 0
              self.topo.edge[e1][e2]['flows'][tuple(selectedPath[0])] \
                = self.topo.edge[e1][e2]['flows'][tuple(selectedPath[0])] + volumeTran

            if src not in edgeNodes:
              edgeNodes.append(src)
            if dst not in edgeNodes:
              edgeNodes.append(dst)
            TM[src][dst] = TM[src][dst] -volumeTran
            totalVol = totalVol -volumeTran
            self.installRules(selectedPath[0],volumeTran,(src,dst))

            #print "volumeTran",volumeTran,selectedPath
    #if totalVol != 0:
      #print "ERROR"
    return edgeNodes,totalVol



  def selectPath(self, paths):
    #print "selectPath"
    ruleToInstall = 0
    flag = True
    x = 0
    while True:
      
      for p in paths:
        
        existingRules = self.getMaxRules(p[0],p[0][0],p[0][-1])
        remRules, isNMaxExhausted = self.getMinRemRules(p[0],p[0][0],p[0][-1])
        #print remRules, self.NMaxEnt - existingRules
        '''
        if  existingRules < self.NMaxEnt:
          ruleToInstall = self.NMaxEnt - existingRules
          flag = False
          #print ruleToInstall
          #print ";;",p ,existingRules
          return p,ruleToInstall         
        '''  
        if  remRules > 0:
          ruleToInstall = remRules
          flag = False
          #print ruleToInstall
          #print ";;",p ,existingRules
          return p,ruleToInstall         
 
        if p[1] == 0:
          if flag == False:
            #print "ERROR no space"
            return None,None
          #increase self.NMaxEnt
          #print "Incr", x, self.NMaxEnt, self.complThres
          x = x+1 
          if isNMaxExhausted:
            self.NMaxEnt = self.NMaxEnt  + 10
          else:
            self.complThres = self.complThres  + 100
          flag = False
          break

  def ruleOffload(self):
    factor = 0.20
    maxx = 0
    while True:
      partitions = copy.deepcopy(self.partitions)
      maxx,compl = self.rulOffload(factor,partitions)
       
      if maxx > 0:
        return maxx, compl 
      #print "Increasing factor to: ",factor
      factor = factor + 0.05
      
    print "Error"
    return -1

  def rulOffload(self,factor,partitions):

    # Parameters: 
    MaxRules = 0
    TotalRulesPerPar = {} 
    defaultRuless = {}
    MaxRule = {}
    for node in partitions:
      TotalRulesPerPar[node]  = len(partitions[node].keys())  
      if MaxRules <  TotalRulesPerPar[node]:
        MaxRules = TotalRulesPerPar[node]
    
    MaxRules = int(MaxRules * factor)
    #print " MAX Rules: ", MaxRules
    for node in partitions:
      #print "Partitioning node :",node, "no of rules: ", len(self.partitions[node].keys())
      newparts = {}

      for ruleno in partitions[node].keys():
         nexthop = self.getNextHop(node, partitions[node][ruleno].tag)
         if nexthop not in newparts:
           newparts[nexthop] = {}
         newparts[nexthop][ruleno] =  partitions[node][ruleno]
         del  partitions[node][ruleno]
      #print "No of Parts : ",len(newparts)
      
      partPernode = {}
      for key in newparts.keys():
        partPernode[key] = copy.deepcopy(newparts[key])
      #print " PArt: ",key, len(self.partition[key].keys())
      # computing default rules
      #print "computing default rules, node, ",node 
      newpartitions, newRootrules, newdefaultSet, default = getDefaultRules(partPernode)
 
      # move the rules to the root
      for key in newRootrules:
        for newRule in newRootrules[key]:
          partitions[node][newRule.number] = newRule

      roomLeft = MaxRules - len(partitions[node].keys()) 
      #print "Max no of rules :", MaxRules,"Room LEft : ",roomLeft, "No of default rules :", len(newdefaultSet.keys())
      
      ###################################################################3333
      # If room is left check if some offloaded rules can still be moved to the root 
      while roomLeft !=0 and roomLeft - len(newdefaultSet.keys()) >= 0 and len(newdefaultSet.keys()) > 0:
      
        shortestRuleCount = 10000
        shortestkey = 0
        # Get the shortest rule set and try to fit it in the root
        for key in newdefaultSet.keys():
          if len(newdefaultSet[key]) < shortestRuleCount:
            shortestRuleCount = len(newdefaultSet[key])
            shortestkey = key

        #print  roomLeft,"Shortest: ", shortestRuleCount,newdefaultSet[shortestkey],shortestkey

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
            searchkey = -1
            for rule in newpartitions[key]:
              #print "hi",rule.number 
              if rule.number == ruleno:
                #print "found",key,ruleno
                searchkey = key
                break
            if searchkey == -1:
              continue
            count = 0
            for k in range(0,1):#len(newdefaultSet[shortestkey])):
              for rule in newpartitions[searchkey]:
                #print rule.number
                if rule.number == newdefaultSet[shortestkey][k] and roomLeft >= len(newdefaultSet.keys()):
                  #print "Pushing: ", newdefaultSet[shortestkey][k]
                  partitions[node][newdefaultSet[shortestkey][k]] = rule
                  lst = newpartitions[searchkey]
                  #print lst
                  lst.remove(rule)
                  roomLeft = roomLeft - 1
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
      #print "Finally : ", len( self.partitions[node].keys()), len(newdefaultSet.keys())
      if node not in defaultRuless:
        defaultRuless[node] = len(newdefaultSet.keys())
      else:
        defaultRuless[node] = len(newdefaultSet.keys()) + defaultRuless[switchId]

      '''
      for key in updatedPartitions.keys():
        for rule in self.partition[key]:
          self.partition[key][rule].printRule()
      '''
      #updating patitions
      for key in newparts.keys():
        newparts[key] = {}

        if key in newpartitions:
          for newRule in newpartitions[key]:
            newparts[key][newRule.number] = newRule
          #newRule.printRule()
      #  print "After ",self.partition[key].keys(),len(self.partition[key].keys())

      #updating root patition
      # print "before",self.partition[switchId].keys(), len(self.partition[switchId].keys())   
      for key in newRootrules:
        for newRule in newRootrules[key]:
          partitions[node][newRule.number] = newRule

      MaxRule[node] = len(partitions[node].keys()) + len(newdefaultSet.keys())
      ######################################################################
      # Calculate the agg SW offload capacity
      
      for dst in newparts.keys():
        noOfrulesTooffload = len(newparts[dst].keys())
        noOfnexthopTooffload = 3
        limit = 0 
        noofdefaultrules = 2
        for i in range(0,noOfnexthopTooffload):
          limit = limit + int(MaxRules/self.tunnelSWs[node][dst][i])
        excess =  noOfrulesTooffload + noofdefaultrules - limit       
        if excess > 0 :
          return -1,0
          if MaxRule[node] < MaxRule[node] + excess:    
            MaxRule[node] = MaxRule[node] + excess #?    
      
    maxx = 0
    for key in MaxRule:
      #print key , self.MaxRule
      if maxx < MaxRule[key]:
        maxx  = MaxRule[key]      

    ComplTime = 0.0
    for key in MaxRule:
      burst = MaxRule[key]
      #print "Burst", burst
      L = self.topo.node[key]['lowPrio']
      #burst = self.topo.node[key]['rules']
      time = self.getDummyComplTime(L,burst) 
      if ComplTime < time:
        ComplTime = time
    #print "HI:",ComplTime
    return maxx, ComplTime 

  def assignTunnelSWs(self):
    self.tunnelSWs = {}
    for s in self.topo.node:
      if s not in self.tunnelSWs:
        self.tunnelSWs[s] = {}
      for d in self.topo.node:
        self.tunnelSWs[s][d] = list()
        for i in range(0,10):
          self.tunnelSWs[s][d].append(randint(1,5))
      
  def getNextHop(self,node,path):
    #print node, path, len(path)
    for i in range(0,len(path)-1):
      #print path[i]
      if str(node) == str(path[i]):
        return path[i+1]
    print " Error"
    return -1
      

  def assignRules(self):
    maxRules = 0
    #print " "
    srcIPs = {}
    pathscovered = {}
    self.partitions = {}
    ruleno = 0
    # Node iterator
    for node in self.topo.node:
      # Assign some random IP to this node.  
      srcIPs[node] = "10.0.0." + str(node) 

    byte0= 0
    for node in self.topo.node:
      rulePerR = 0
      maxRulesIntR = 0

      
      #print node,self.topo.node[node]
      # Iterate through the next hops
      byte1 = 0
      for nextHop in self.topo.node[node]['rules_hop']:
        # Itearate through the next hop path
        byte2 = 0
        for path in self.topo.node[node]['rules_hop'][nextHop]:
          #print path
          # If path is already seen continue
          if path in pathscovered:
            continue
          pathscovered[path] = True
          # Create the rule set for the path
          noofrules = self.topo.node[node]['rules_hop'][nextHop][path]
          #print "DEBUG: ", node , noofrules
          rules = {}
          count = 0
          for i in range(0,noofrules):
            #print str(byte0)+"."+ str(+byte1)+"."+ str(byte2)+"."+str(count)
            rules[ruleno] = rule(ruleno, "10.0.0."+str(path[0]) , str(byte0)+"."+ str(byte1)+"."+ str(byte2)+"."+str(count),count, (path) )
            count = count + 1
            ruleno = ruleno + 1
          byte2 = byte2+1
          # Assign the rule set to all the nodes in the path
          for i in range(0,len(path)-1):
            p = path[i]
            if p not in self.partitions:
              self.partitions[p] = {}
            for i in rules:
              self.partitions[p][i] = copy.deepcopy(rules[i])  
        byte1 = byte1+1  
      byte0 = byte0 + 1      
    #for p in self.partitions: 
      #print "Partition no: ",p, "Len of partition :", len(self.partitions[p])
      #for x in self.partitions[p]:
      #  print self.partitions[p][x].printRule() 
      
    
  def rescheduleFlows(self,TM):

    totalVol = 0
    for i in TM:
      for j in TM[i]:
        totalVol = totalVol + TM[i][j]
        
    
    oldVol = 0
    edgeNodes = []
    while oldVol != totalVol:
      oldVol = totalVol
      for src in self.topo.node:
        for dst in self.topo.node:

          volumeTran = 0
          if src != dst and TM[src][dst] != 0:

            p = self.computePaths(src,dst)
            if p[0][1] ==0:
                continue
            for k in range(len(p[0][0])-1):
              e1 = p[0][0][k]
              e2 = p[0][0][k+1]
              
              
              if 'flows' not in self.topo.edge[e1][e2]:
                self.topo.edges[e1][e2]['flows'] = {}

              if p[0][1] >= TM[src][dst]:
                volumeTran = TM[src][dst]
              else:
                volumeTran = p[0][1]

              self.topo.edge[e1][e2]['w'] \
                =  self.topo.edge[e1][e2]['w'] -volumeTran

              if tuple(p[0][0]) not in self.topo.edge[e1][e2]['flows']:
                self.topo.edge[e1][e2]['flows'][tuple(p[0][0])] = 0
              self.topo.edge[e1][e2]['flows'][tuple(p[0][0])] \
                = self.topo.edge[e1][e2]['flows'][tuple(p[0][0])] + volumeTran

            if src not in edgeNodes:
              edgeNodes.append(src)
            if dst not in edgeNodes:
              edgeNodes.append(dst)
            TM[src][dst] = TM[src][dst] -volumeTran
            totalVol = totalVol -volumeTran
            self.installRules(p[0][0],volumeTran,(src,dst))

            #print "volumeTran",volumeTran

    return edgeNodes,totalVol

    
  def installRules(self, path, rules, match):
    if rules ==0:
      print "WHYYYYYYYYYYYYYYYYYY"

    for n in range(len(path)):
      node = path[n]
      
      
      if node != path[-1]:
      
        self.topo.node[node]['rules'] = self.topo.node[node]['rules'] + rules
        if path[n+1] not in self.topo.node[node]['rules_hop']:
          self.topo.node[node]['rules_hop'][path[n+1]] = {}
      
        if tuple(path) not in self.topo.node[node]['rules_hop'][path[n+1]]:
          self.topo.node[node]['rules_hop'][path[n+1]][tuple(path)] = 0
          
        self.topo.node[node]['rules_hop'][path[n+1]][tuple(path)] = \
          self.topo.node[node]['rules_hop'][path[n+1]][tuple(path)] + rules
        

  def assignpriorityrules(self):
    for node in self.topo.node:
      self.topo.node[node]['lowPrio'] = randint(50,90)

  def getTotalCompletionTimeForOffload(self, partitions):
    ComplTime = 0.0
    for part in partitions:
      burst = partitions[part]
      L = self.topo.node[part]['lowPrio']
      burst = self.topo.node[part]['rules']
      time = self.getDummyComplTime(L,burst) 
      if ComplTime < time:
        ComplTime = time
    return ComplTime

  def getTotalCompletionTime(self):
    ComplTime = 0.0
    for node in self.topo.node:
      L = self.topo.node[node]['lowPrio']
      burst = self.topo.node[node]['rules']
      time = self.getDummyComplTime(L,burst) 
      if ComplTime < time:
        ComplTime = time
    return ComplTime

  def getTotalCompletionTime_withoutEdge(self,edgeNodes):
    ComplTime = 0.0
    for node in self.topo.node:
      if node not in edgeNodes:
        L = self.topo.node[node]['lowPrio']
        burst = self.topo.node[node]['rules']
        time = self.getDummyComplTime(L,burst) 
        if ComplTime < time:
          ComplTime = time
    return ComplTime
      
  def getDummyComplTime(self,displ,size):
    a = 3.0
    b = 0.15
    c = 3.1
    #self.complThres = 2000
    if displ == 0: 
      return a * size
    else:
      return ((b * displ) + c) * size

  def getMaxRules(self,path,src,dst):
    maxRules = 0
    for node in path:
      if node != src and node !=dst:
        if self.topo.node[node]['rules'] > maxRules:
          maxRules = self.topo.node[node]['rules']
    return maxRules

  def getMinRemRules(self,path,src,dst):
    minRules = 100000
    isNmax = False
    for node in path:
      if node != src and node !=dst:
        # NMaxEnt Check
        if self.NMaxEnt - self.topo.node[node]['rules'] < minRules:
          minRules = self.NMaxEnt - self.topo.node[node]['rules']
          if minRules == 0:
            isNmax = True
        assRules =  self.topo.node[node]['rules'] 
        lowRules = self.topo.node[node]['lowPrio']
        #print assRules, lowRules
        presentComplTime = self.getDummyComplTime(lowRules,assRules+1)
        while presentComplTime < self.complThres:
         assRules = assRules + 1
         presentComplTime = self.getDummyComplTime(lowRules,assRules+1)
        
        rulesLeft = assRules - self.topo.node[node]['rules']
                
        if rulesLeft < minRules:
          minRules = rulesLeft

    return minRules, isNmax



  def maxRules(self):
    maxRules = 0
    for node in self.topo.node:
      if self.topo.node[node]['rules'] > maxRules:
        maxRules = self.topo.node[node]['rules']
    return maxRules

  def maxRules_withoutEdge(self,edgeNodes):
    maxRules = 0
    for node in self.topo.node:
      if node not in edgeNodes:
        if self.topo.node[node]['rules'] > maxRules:
          maxRules = self.topo.node[node]['rules']
    return maxRules


  def tunnelFailure(self, failedEdge,e1,e2,TM):
    #print "Tunnel failure"
    #print failedEdge
    for path in failedEdge['flows']:
      for k in range(len(path)-1):
        E1= path[k]
        E2 = path [k+1]
        if E1!=e1 and E2!=e2:
          self.topo.edge[E1][E2]['w'] = self.topo.edge[E1][E2]['w'] + failedEdge['flows'][path]
          self.topo.edge[E1][E2]['flows'].pop(path)
          
      TM[path[0]][path[-1]] = TM[path[0]][path[-1]] +  failedEdge['flows'][path]
      failedEdge['flows'][path] = 0  
    return TM

  def ruleReset(self):

    for node in self.topo.node:
      self.topo.node[node]['rules'] = 0
      self.topo.node[node]['rules_hop'] = {}


  def mapTraffic (self, TM,nodes,edges):

    totalVol = 0
    for i in TM:
      for j in TM[i]:
        totalVol = totalVol + TM[i][j]
        
    #map traffic to hop one
    for src in nodes:
      for dst in nodes:
        if src != dst:
          if TM[src][dst] !=0 and TM[src][dst] >=  edges[src][dst]['w'] :
            TM[src][dst] = TM[src][dst] -  edges[src][dst]['w']
            totalVol = totalVol -  edges[src][dst]['w']
            if 'flows' not in edges[src][dst]:
              edges[src][dst]['flows'] = {}
            if (src,dst) not in edges[src][dst]['flows']:
              edges[src][dst]['flows'][(src,dst)] = 0
            edges[src][dst]['flows'][(src,dst)] = edges[src][dst]['w']
            edges[src][dst]['w'] = 0

          else:
            edges[src][dst]['w'] = edges[src][dst]['w'] - TM[src][dst]
            totalVol = totalVol - TM[src][dst]
            if 'flows' not in edges[src][dst]:
              edges[src][dst]['flows'] = {}
            if (src,dst) not in edges[src][dst]['flows']:
              edges[src][dst]['flows'][(src,dst)] = 0
            edges[src][dst]['flows'][(src,dst)] = TM[src][dst]
            TM[src][dst] = 0

    oldVol = 0

    while oldVol != totalVol:
      oldVol = totalVol
      for src in nodes:
        for dst in nodes:
          if src != dst and TM[src][dst] != 0:

            p = self.computePaths(src,dst)
            if p[0][1] ==0:
                continue
            for k in range(len(p[0][0])-1):
              e1 = p[0][0][k]
              e2 = p[0][0][k+1]
              
              self.topo.edge[e1][e2]['w'] \
                =  self.topo.edge[e1][e2]['w'] -1
              
              if 'flows' not in edges[e1][e2]:
                self.topo.edges[e1][e2]['flows'] = {}
              if tuple(p[0][0]) not in self.topo.edge[e1][e2]['flows']:
                self.topo.edge[e1][e2]['flows'][tuple(p[0][0])] = 0
              self.topo.edge[e1][e2]['flows'][tuple(p[0][0])] \
                = self.topo.edge[e1][e2]['flows'][tuple(p[0][0])] +1

            TM[src][dst] = TM[src][dst] -1
            totalVol = totalVol -1

      #print "TotalVolume",totalVol
    return totalVol


  def computePaths(self,src,dst):

    paths  = list(nx.all_simple_paths(self.topo,src,dst,4))
    pathTmp = []
    for path in paths:
      pathTmp.append((path,self.computePathCap(path)))
    return sorted(pathTmp,key=lambda x: x[1],reverse = True)


  def computePathCap(self,path):

    edges = self.topo.edge
    min = edges[path[0]][path[1]]['w']
    for index in range(len(path) -1):
      if edges[path[index]][path[index+1]]['w'] < min:
        min = edges[path[index]][path[index+1]]['w']
    return min

  def getEdge(self,Nodes):
    edges = []
    for src  in range(Nodes):
      for dst in range(Nodes):
        if src !=dst:
                            edges.append((src,dst))
    return      edges



  '''
    This method draw the topology
    Some code in this method is copied from mininet

  '''
  def plotTopo(self, topo):
    import matplotlib.pyplot as plt


    edge_width = 10
    node_size = 100
    node_color = 'g'
    edge_color = 'b'


    nx.draw(topo)
    plt.show()

    plt.show()

class rule:
  def __init__(self,number,srcIP,dstIP,priority,tag):
    self.number = number
    self.srcIP = srcIP
    self.dstIP = dstIP
    self.priority = priority
    self.tag = tag
    
  def printRule(self):    
    print "ID ",self.number," srcIP ",self.srcIP," dstIP ", \
      self.dstIP, " priority ",self.priority, "tag ",self.tag
    

if __name__ == "__main__":
    Failover(25)

