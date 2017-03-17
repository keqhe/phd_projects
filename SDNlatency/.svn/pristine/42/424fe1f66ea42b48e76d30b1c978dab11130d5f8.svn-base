from random import choice
import networkx as nx
from defaultRules import*
from random import *
import copy
import math
import copy
#from defaultRules import*

class TEQoS():

  def __init__(self,Nodes):

    for k in range(5):
      self.failOver(Nodes)

  def failOver(self,Nodes):
    # k number of ports on each switch

    self.topo = nx.DiGraph()
    self.topo.add_edges_from(self.getEdge(Nodes), type = 'tunnels')
    cap = 1200
    maxLinkCost = 10
    self.NMaxEnt = 40
    self.complThres = 100
    self.partitions = {}
    nodes = self.topo.node
    for k in nodes:
      #randomly assigning popularity index
      nodes[k]['ps_index'] = randint(0,5)
      nodes[k]['pd_index'] = randint(0,5)

    for k in nodes:
      #randomly assigning popularity index
      nodes[k]['hps_index'] = randint(0,5)
      nodes[k]['hpd_index'] = randint(0,5)

    for k in nodes:
      nodes[k]['choice'] = range(1,nodes[k]['hps_index']*nodes[k]['hpd_index'])
      nodes[k]['alreadyLowRules'] = randint(0,20)
      


    edges = self.topo.edge
    for src in edges.keys():
      for dst in edges[src].keys():
        # randomly assigning tunnels bandwidth
        # cap = 1 - w
        edges[src][dst]['cap'] = randint(100,cap)
        edges[src][dst]['cost'] = randint(1,maxLinkCost)


    TMLite = {}
    TM = {}
    self.ruleReset()
    for src in nodes:
      for dst in nodes:
        if src != dst:
          if src not in TMLite:
            TMLite[src] = {}
          TMLite[src][dst]= nodes[src]['ps_index'] * nodes[dst]['pd_index']
          
          if src not in TM:
            TM[src] = {}
          TM[src][dst]= nodes[src]['hps_index'] * nodes[dst]['hpd_index']

    
    totalVol = self.mapTraffic(TMLite,self.topo.node,self.topo.edge)
    print self.maxHosts() , totalVol

    if totalVol == 0:

      #reschedule flows
      # send a copy
      #print self.computePaths(firstNode,secondNode)
      TM1 = copy.deepcopy(TM)
      topo1 = copy.deepcopy(self.topo)
      
      remainingVol= self.rescheduleFlows(TM)
      if remainingVol !=0:
        return
      #print edgeNodes
      maxR = self.maxRules()
      maxC = self.getTotalCompletionTime()
      
      #maxER = self.maxRules_withoutEdge(edgeNodes)

      self.topo = topo1
      TM = TM1
      remainingVol = self.rescheduleFlowsNMaxEnt(TM)
      if remainingVol != 0:
        return
      #print edgeNodes
      print "base Case | FlowEngineering | flowengineering + flow Offload "
#      print  maxR,self.maxRules(),

      
   
      self.assignTunnelSWs()
      self.fillPartitions()
      
      
      maxx, compl =  self.ruleOffload()
      
      print  maxR,self.maxRules(),maxx,"Time ",maxC, self.getTotalCompletionTime(), compl      
    '''
    for n in self.topo.node:
      print self.topo.node[n]['rules'],self.topo.node[n]['HighpRules'],self.topo.node[n]['LowpRules']
    '''

    '''
         
    for rule in self.topo.node[6]['lowRuleSet']:
      print rule
      #rule.printRule()
#    for rule in self.topo.node[6]['highRuleSet']:
#      rule.printRule()
    '''
    
    
  def fillPartitions(self):
  
    for n in self.topo.node:
      i = 0
      for ruleH in self.topo.node[n]['highRuleSet']:
        ruleH.number = i
        if n not in self.partitions:
          self.partitions[n] = {}
        self.partitions[n][i] = ruleH
        i = i+1

      for ruleL in self.topo.node[n]['lowRuleSet']:
        ruleL.number = i
        if n not in self.partitions:
          self.partitions[n] = {}
        self.partitions[n][i] = ruleL
        i = i + 1
        
  def assignTunnelSWs(self):
    self.tunnelSWs = {}
    for s in self.topo.node:
      if s not in self.tunnelSWs:
        self.tunnelSWs[s] = {}
      for d in self.topo.node:
        self.tunnelSWs[s][d] = list()
        for i in range(0,5):
          self.tunnelSWs[s][d].append(randint(3,6))
      

        
  def maxHosts(self):

    max_pd_index = 0
    max_ps_index = 0
    max_hpd_index = 0
    max_hps_index = 0    
    for node in self.topo.node:
      if max_pd_index < self.topo.node[node]['pd_index']:
        max_pd_index = self.topo.node[node]['pd_index']

      if max_ps_index < self.topo.node[node]['ps_index']:
        max_ps_index = self.topo.node[node]['ps_index']
        
      if max_hpd_index < self.topo.node[node]['hpd_index']:
        max_hpd_index = self.topo.node[node]['hpd_index']

      if max_hps_index < self.topo.node[node]['hps_index']:
        max_hps_index = self.topo.node[node]['hps_index']
        
    return max(max_ps_index * max_pd_index,max_hps_index * max_hpd_index)


  def rescheduleFlowsNMaxEnt(self,TM):

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

            p = self.computePaths(src,dst,'cost')
            if p[0][1] ==0:
                continue
              
            selectedPath, ruleToInstall = self.selectPath(p)
            #print selectedPath
            
            for k in range(len(selectedPath[0])-1):
              e1 = selectedPath[0][k]
              e2 = selectedPath[0][k+1]
              
              volumeTran = min(ruleToInstall,TM[src][dst],selectedPath[1])

              
              self.topo.edge[e1][e2]['cap'] \
                =  self.topo.edge[e1][e2]['cap'] - volumeTran
              self.topo.edge[e1][e2]['cost'] \
                =  self.topo.edge[e1][e2]['cost'] + volumeTran *0.2
              
              if 'flows' not in self.topo.edge[e1][e2]:
                self.topo.edge[e1][e2]['flows'] = {}

              
              #print volumeTran, ruleToInstall,TM[src][dst],selectedPath[1]
              if tuple(selectedPath[0]) not in self.topo.edge[e1][e2]['flows']:
                self.topo.edge[e1][e2]['flows'][tuple(selectedPath[0])] = 0
              self.topo.edge[e1][e2]['flows'][tuple(selectedPath[0])] \
                = self.topo.edge[e1][e2]['flows'][tuple(selectedPath[0])] + volumeTran

            TM[src][dst] = TM[src][dst] -volumeTran
            totalVol = totalVol -volumeTran
            self.installRules(selectedPath[0],volumeTran,(src,dst),'high')

            #print "volumeTran",volumeTran,selectedPath

    return totalVol



  def selectPath(self, paths):
    #print "selectPath"
    ruleToInstall = 0
    flag = True

    while True:
      
      for p in paths:
        
        existingRules = self.getMaxRules(p[0],p[0][0],p[0][-1])
        remRules   = self.getMinRemRules(p[0],p[0][0],p[0][-1])		        

        if  remRules > 0:
          ruleToInstall = remRules
          flag = False
          return p,ruleToInstall         
          

        if p[1] == 0:
          if flag == False:
            print "ERROR no space"
            return None,None
          #increase self.NMaxEnt
          self.complThres = self.complThres =   + 10
          flag = False
          break

        if flag == True:
          self.complThres = self.complThres =   + 10            
    
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
              
            selectedPath= p[0]
            #print selectedPath
            
            for k in range(len(selectedPath[0])-1):
              e1 = selectedPath[0][k]
              e2 = selectedPath[0][k+1]
              
              volumeTran = min(TM[src][dst],selectedPath[1])

              
              self.topo.edge[e1][e2]['cap'] \
                =  self.topo.edge[e1][e2]['cap'] - volumeTran
              self.topo.edge[e1][e2]['cost'] \
                =  self.topo.edge[e1][e2]['cost'] + volumeTran *0.2
              
              if 'flows' not in self.topo.edge[e1][e2]:
                self.topo.edge[e1][e2]['flows'] = {}

              
              #print volumeTran, ruleToInstall,TM[src][dst],selectedPath[1]
              if tuple(selectedPath[0]) not in self.topo.edge[e1][e2]['flows']:
                self.topo.edge[e1][e2]['flows'][tuple(selectedPath[0])] = 0
              self.topo.edge[e1][e2]['flows'][tuple(selectedPath[0])] \
                = self.topo.edge[e1][e2]['flows'][tuple(selectedPath[0])] + volumeTran

            TM[src][dst] = TM[src][dst] -volumeTran
            totalVol = totalVol -volumeTran
            self.installRules(selectedPath[0],volumeTran,(src,dst),"high")
            #print "volumeTran",volumeTran,selectedPath

    return totalVol

  def ruleOffload(self):
    factor = 0.2
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
    detailedMaxRule = {}
 
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
      for rule_no in partitions[node]:
        if node not in detailedMaxRule:
            detailedMaxRule[node] = {'H':0,'L':0}

        if partitions[node][rule_no].priority == 100:
          detailedMaxRule[node]['L'] = detailedMaxRule[node]['L'] + 1
        else:
          detailedMaxRule[node]['H'] = detailedMaxRule[node]['H'] + 1
      detailedMaxRule[node]['L'] = detailedMaxRule[node]['L'] + len(newdefaultSet.keys())

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
    kkey = None
    for key in MaxRule:
      #print key , self.MaxRule
      if maxx < MaxRule[key]:
        maxx  = MaxRule[key]      
    
    
    
    ComplTime = 0.0
    for key in MaxRule:
      alreadyLowRules =  self.topo.node[key]['alreadyLowRules']
      HighpRules =   detailedMaxRule[key]['H']
      LowpRules =   detailedMaxRule[key]['L']

      time = self.getDummyComplTime(alreadyLowRules ,HighpRules) + self.getDummyComplTime(0 ,LowpRules) 


      if ComplTime < time:
        ComplTime = time
    #print "HI:",ComplTime
    return maxx, ComplTime 

     
  def getNextHop(self,node,path):
    #print node, path, len(path)
    for i in range(0,len(path)-1):
      #print path[i]
      if str(node) == str(path[i]):
        return path[i+1]
    print " Error"
    return -1
      
  def getDummyComplTime(self,displ,size):
    a = 3.0
    b = 0.15
    c = 3.1
    #self.complThres = 2000
    if displ == 0: 
      return a * size
    else:
      return ((b * displ) + c) * size

  def getTotalCompletionTime(self):
    ComplTime = 0.0
    for node in self.topo.node:

      alreadyLowRules =  self.topo.node[node]['alreadyLowRules']
      HighpRules =   self.topo.node[node]['HighpRules']
      LowpRules =   self.topo.node[node]['LowpRules']

      time = self.getDummyComplTime(alreadyLowRules ,HighpRules) + self.getDummyComplTime(0 ,LowpRules) 
      if ComplTime < time:
        ComplTime = time
    return ComplTime

  def getMinRemRules(self,path,src,dst):
    minRules = 100000
    for node in path:
      if node != src and node !=dst:

        alreadyLowRules =  self.topo.node[node]['alreadyLowRules']
        HighpRules =   self.topo.node[node]['HighpRules']
        LowpRules =   self.topo.node[node]['LowpRules']
	

        
        HighTime = self.getDummyComplTime(alreadyLowRules,HighpRules+1)
        LowTime = self.getDummyComplTime(0,LowpRules)
        presentComplTime = HighTime + LowTime
        while presentComplTime < self.complThres:
          HighpRules = HighpRules + 1

          HighTime = self.getDummyComplTime(alreadyLowRules,HighpRules+1)
          LowTime = self.getDummyComplTime(0,LowpRules)
          presentComplTime = HighTime + LowTime
        
        rulesLeft = HighpRules - self.topo.node[node]['HighpRules']
                
        if rulesLeft < minRules:
          minRules = rulesLeft

    return minRules



    
  def installRules(self, path, rules, match, priority = 'low'):
    if rules ==0:
      print "WHYYYYYYYYYYYYYYYYYY"
    match =  (path[0],path[-1])
       
    startip = None
    if priority == 'high':
      if match not in self.topo.node[match[0]]['offset']:
        self.topo.node[match[0]]['offset'][match] = 0
      startip = self.topo.node[match[0]]['offset'][match]
      self.topo.node[match[0]]['offset'][match] = self.topo.node[match[0]]['offset'][match] + rules

    if priority == 'low':
      rules = 1
    
    for n in range(len(path)):
      node = path[n]
      
      if node != path[-1]:
      
        self.topo.node[node]['rules'] = self.topo.node[node]['rules'] + rules
        if priority == 'low':
          self.topo.node[node]['LowpRules'] = self.topo.node[node]['LowpRules'] + rules
          self.topo.node[node]['lowRuleSet'].append(rule(None,"0."+str(match[0])+\
            ".0.0/24","0."+str(match[1])+".0.0/24",100,path))
        else:
          self.topo.node[node]['HighpRules'] = self.topo.node[node]['HighpRules'] + rules
 
          for k in range(startip,startip+rules):  
            self.topo.node[node]['highRuleSet'].append(rule(None,"0."+str(match[0])+\
              ".0."+str(k),"0."+str(match[1])+".0.0",200,path))         
#              "+str(choice(self.topo.node[match[1]]['choice']))\



        if path[n+1] not in self.topo.node[node]['rules_hop']:
          self.topo.node[node]['rules_hop'][path[n+1]] = {}
      
        if tuple(path) not in self.topo.node[node]['rules_hop'][path[n+1]]:
          self.topo.node[node]['rules_hop'][path[n+1]][tuple(path)] = 0
          
        self.topo.node[node]['rules_hop'][path[n+1]][tuple(path)] = \
          self.topo.node[node]['rules_hop'][path[n+1]][tuple(path)] + rules
        

  def getMaxRules(self,path,src,dst):
    maxRules = 0
    for node in path:
      if node != src and node !=dst:
        if self.topo.node[node]['rules'] > maxRules:
          maxRules = self.topo.node[node]['rules']
    return maxRules


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
          self.topo.edge[E1][E2]['cap'] = self.topo.edge[E1][E2]['cap'] + failedEdge['flows'][path]
          self.topo.edge[E1][E2]['flows'].pop(path)
          
      TM[path[0]][path[-1]] = TM[path[0]][path[-1]] +  failedEdge['flows'][path]
      failedEdge['flows'][path] = 0  
    return TM

  def ruleReset(self):

    for node in self.topo.node:
      self.topo.node[node]['rules'] = 0
      self.topo.node[node]['offset'] = {}
      self.topo.node[node]['HighpRules'] = 0
      self.topo.node[node]['LowpRules'] = 0
      self.topo.node[node]['lowRuleSet']  = []
      self.topo.node[node]['highRuleSet'] = []     
      self.topo.node[node]['rules_hop'] = {}

  def getMaxVol(self, TM):

    src = None
    dst = None
    maxVol = 0
    for i in TM:
      for j in TM[i]:
        if maxVol <= TM[i][j] and i != j:
          src = i
          dst = j
          maxVol = TM[i][j]
    return maxVol,src,dst


  def mapTraffic (self, TM,nodes,edges):

    totalVol = 0
    for i in TM:
      for j in TM[i]:
        totalVol = totalVol + TM[i][j]
    
    #map traffic to hop one

    oldVol = 0
    self.oo =[]
    while oldVol != totalVol:
      oldVol = totalVol
      if totalVol == 0:
        break

      vol,src,dst = self.getMaxVol(TM)
      
      p = self.computePaths(src,dst)
      if p[0][1] == 0 or p[0][1] < vol:
        continue


      for k in range(len(p[0][0])-1):
        e1 = p[0][0][k]
        e2 = p[0][0][k+1]
              
        self.topo.edge[e1][e2]['cap'] \
          =  self.topo.edge[e1][e2]['cap'] - vol
        
        if 'flows' not in edges[e1][e2]:
          self.topo.edge[e1][e2]['flows'] = {}
          
        if tuple(p[0][0]) not in self.topo.edge[e1][e2]['flows']:
          self.topo.edge[e1][e2]['flows'][tuple(p[0][0])] = 0
        self.topo.edge[e1][e2]['flows'][tuple(p[0][0])] \
            = self.topo.edge[e1][e2]['flows'][tuple(p[0][0])] + vol

      TM[src][dst] = TM[src][dst] - vol
      totalVol = totalVol - vol
      
      self.installRules(p[0][0],vol,(src,dst))

    return totalVol


  def computePaths(self, src, dst, obj = 'cap'):

    paths  = list(nx.all_simple_paths(self.topo,src,dst,4))
    pathTmp = []
    rtn = None
    for path in paths:
      pathTmp.append((path,self.computePathCap(path),self.computePathCap(path)))

    if obj == 'cap':
      rtn = sorted(pathTmp,key=lambda x: x[1],reverse = True)
    elif obj == 'cost':
      rtn = sorted(pathTmp,key=lambda x: x[2],reverse = True)
    else:
      print "ERROR: invaild obj for computing paths"
    return rtn


  def computePathCap(self,path):

    edges = self.topo.edge
    min = edges[path[0]][path[1]]['cap']
    for index in range(len(path) -1):
      if edges[path[index]][path[index+1]]['cap'] < min:
        min = edges[path[index]][path[index+1]]['cap']
    return min

  def computePathCost(self,path):

    edges = self.topo.edge
    cost = 0
    for index in range(len(path) -1):
      cost = cost + edges[path[index]][path[index+1]]['cost']
    return cost


  def getEdge(self,Nodes):
    edges = []
    for src  in range(Nodes):
      for dst in range(Nodes):
        if src !=dst:
          edges.append((src,dst))
    return  edges



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
    TEQoS(25)

