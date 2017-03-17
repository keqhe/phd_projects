import networkx as nx
from topoManager import *
import fatTree
from time import *
from ruleDepDAG import *
from rulePartition import *
from allPartition import *
from random import randrange
#import matplotlib.pyplot as plt
from edgePartition import *
#from ciscoLatencyModel import *
#from latencyModel import *
from parseClassBench import *
import os, sys, commands
import subprocess
import random
from netaddr import *

noofrules = 0
def main():

  topoo = fatTree.FatTree(8, serverUplink=1000, edgeUplink = 1000, aggUplink = 1000)
  t = TopoManager()
  t.addRawGraph(topoo.topo)
  #ciscolat = ciscoBurstModel()  
  bcmlat = bcmBurstModel(-1)
  #if len(sys.argv) != 2:
  #  print "ERROR: File name missing"
  #  print "usage: ruleOffload <fileName>" 
  #  exit()   
  global noofrules
  noofrules = 90
  #print "Total hosts ",len(t.hosts)
  print "ToR switches ", len(t.S_ToR )
  #print len(t.hosts)/len(t.S_ToR)
  
  #ip = IPNetwork('128.0.0.0/3')
  #sub = list(ip.subnet(4))
  #print ip, sub		
  #rules,swBaseTable = readFile(sys.argv[1]) 
  allpaths = allTaggedShortestPath(t)
  tagpaths = allTaggedShortestPath(t)
  for tag in tagpaths.keys():
    if len(tagpaths[tag]) == 3:
      del tagpaths[tag]
  #print tagpaths
  #raw_input("Press any key")
  rules,swBaseTable = readRulesFromClassBench(topoo.edgeSWs,allpaths,noofrules,t)
  
  for rule in rules:
    count = 0
    todel = list()
    for key in rules[rule].keys():
      #print allpaths[rules[rule][key].tag],
      #rules[rule][key].printRule()
      count = count + 1 
      if count > noofrules:
        todel.append(key)
        del rules[rule][key]
    #for d in todel:
     #del rules[rule][d]
        swBaseTable[rule] = swBaseTable[rule] - 1
    print "sw: ",rule, len(rules[rule].keys()), swBaseTable[rule]

  dummyRules = {}
  '''
  count = 1
  for sw in topoo.edgeSWs:
    dummyRules[sw] = createDummyRules(sw,count)
    count = count + 20
  '''
  
  ruleparins = allPartition(rules,topoo.edgeSWs,topoo.topo,allpaths)
  partitions, default = ruleparins.createPartitions()

 # cisco = open('./ruleOffload_Latency_cisco.txt','w')
  bcm = open('./ruleOffload_Latency_bcm.txt','w')
  count = 0  
  print "Switch_ID Rules Default_Rules Base_case"
  for n in partitions.keys():

    defaultRule = 0		
    if n in default.keys():
      defaultRule = default[n]
    count = count + defaultRule
    baseCase = 0
    if n in swBaseTable:
      baseCase = swBaseTable[n]

    print str(n),len( partitions[n].keys()), defaultRule, baseCase
    #cisco.write(str(n)+" "+str( len(partitions[n].keys()) + defaultRule) +" "+str( ciscolat.getBurstComplTime_SamePrio(len(partitions[n].keys()) + defaultRule)) +" "+ str(baseCase)+" "+ str(ciscolat.getBurstComplTime_SamePrio (baseCase))+"\n")
    bcm.write(str(n)+" "+str( len(partitions[n].keys()) + defaultRule) +" "+str( bcmlat.getBurstCompletionTime( len(partitions[n].keys()) + defaultRule)) + " "+ str(baseCase)+" "+str(bcmlat.getBurstCompletionTime (baseCase))+"\n")
  print count
    #for ruleno in partitions[n].keys():
      #print ruleno, 
    #print " "
  #ruleDag = ruleDepDAG(dummyRules[1])
  #partitions = rulePartition( 1, allpaths,ruleDag,topoo.topo)
  
  

import csv
import socket
import struct
from netaddr import IPNetwork

from defaultRules import *
def readFile(filename):
    count = 0
    fd = None
    ruleTable =[]
    table={}
    swBaseTable = {}
    try:
      fd = open(filename, "rb")
    except:
      print "ERROR: unable to open file"
      return
    reader = csv.reader(fd)
    for row in reader:
      rule = {}
      sw = None
      for item in row:
        pair = item.split("=")
        if pair[0] == 'swid':
          sw = int(pair[1])
        elif pair[0] == 'nw_src' or pair[0] == 'nw_dst':
          if pair[1] != '*':
            pair[1]  = IPNetwork(pair[1])
        elif pair[0] == 'tag':
          pair[1] = pair[1].strip()
        else:
          pair[1] = int(pair[1])
        rule[pair[0]] = pair[1]

      if sw not in table:
        table[sw] = {}
      table[sw][count] = Rule(count,rule['nw_src'].__str__(),rule['nw_dst'].__str__(),rule['priority'],rule['tag'])
      
      if sw not in swBaseTable:
        swBaseTable[sw] = 0
      swBaseTable[sw] = swBaseTable[sw] + 1  
      
      count = count + 1
    return table,swBaseTable




    
        
#
# Return Tagged Paths
#
def allTaggedShortestPath(topo):
  taggedPaths = {}
  for src in topo.S_ToR:
    for dst in topo.S_ToR:
      if src == dst:
        continue
      paths = nx.all_shortest_paths(topo.topo,src,dst)
 		    
      try:
        k = 0;
        for p in paths:
          tag = str(src) + "." + str(dst) + "." + str(k)
          taggedPaths[tag] = p
          k = k + 1
          #print tag, taggedPaths[tag]
      except nx.NetworkXNoPath:
        print "NO PATH"
        continue
  
  return taggedPaths    

#
# Test code for creating dummy Rules for constructing DAG
#
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
    

def createDummyRules(sw, c):
  dummyRules = {}
  for k in range(c,c+20):
    x = randrange (0,8)
    if x == sw:
      x = (sw + 1) % 8
    y = randrange (0,2)
    z = randrange (0,20)
    if k % 2 == 0:
      dummyRules[k] = rule(k, "192.168.1."+str(k%256), "192.168.1."+str(z), k+10,str(sw)+"." + str(x) +"." + str(y))
    else:
      dummyRules[k] = rule(k, "192.168.1.0/24", "192.168.1."+str(z), k+10,str(sw)+"." + str(x) +"."+str(y))
  
  #print dummyRules
  return dummyRules  

SynRuleSet = {}
Ruleno = 0
def readRulesFromClassBench(edgeSws,taggedPaths,no,t):
  global SynRuleSet
  baseRuleSet = {}
  noOfEdgeSws = len(edgeSws)
  ruleno = 0
  cmd = "./db_generator/db_generator"    
  process = subprocess.Popen([cmd, "-c","./db_generator/parameter_files/acl3_seed", "200000", "40","+1.0", "+1.0" , "x"] )
  #process = subprocess.Popen([cmd, "-r", no, "x"] )
  process.wait()
  bm = parseClassBench()
  rules = bm.getRules()
  print "Total unique srcIPs: ",len(rules.keys())
  l = rules.keys()
  random.shuffle(l)
  for key in l:
    rules[key] = list(set(rules[key]))
    random.shuffle(rules[key])
    rules[key].sort()
    #print "Key: ",key, (rules[key])
  sw = 0

  # Best Case
  for src in sorted(rules.keys(),key=lambda x:len(rules[x]), reverse = True):
    print "Creating rule for src_sw: ", sw, "Available rules: ", len(rules[src])

    SynRuleSet[sw] = {}
    baseRuleSet[sw] = 0
    n = no
    if no > len(rules[src]):
      n = len(rules[src])
    baseRuleSet[sw] = n

    tags = list()
    for tag in taggedPaths.keys():
      words = tag.split('.')
      if words[0] == str(sw):
        tags.append(tag)
    assignPathsToRules(0,taggedPaths,n,sw,src,rules[src],tags,IPNetwork('0.0.0.0/0'),0)
    baseRuleSet[sw] = len(SynRuleSet[sw].keys())
    sw = sw + 1
    if sw == noOfEdgeSws:
      break
  '''
  for sw in edgeSws:
    print "Creating rule for src_sw: ", sw, len(rules.keys())
    for src in rules.keys():
      words = src.split('.')
      src_sw = int(words[0][1:]) % noOfEdgeSws
      #if src_sw != sw:
      #  continue
      if sw not in SynRuleSet.keys():
        SynRuleSet[sw] = {}
        baseRuleSet[sw] = 0
      for k in range(0,len(rules[src])):
        #print rules[src][k]

        words = rules[src][k].split('.')
        dst_sw = (int(words[0]) + int(words[1]))% noOfEdgeSws
        if int(sw) == dst_sw:
          dst_sw = (dst_sw + 4) % noOfEdgeSws
        lst = list()
        # get a tag for this rule:
        for tag in taggedPaths.keys():
          if len(taggedPaths) == 3:
            continue
          words = tag.split('.')
          if int(words[0]) == int(sw) and int(words[1]) == dst_sw:
            lst.append(tag)
        if len(lst) == 0:
          continue
        #print "List: ",lst
        tag = str(sw) + "."+ str(dst_sw)+"."+ str(randrange(0,len(lst)))
        SynRuleSet[sw][ruleno] = rule(ruleno, src[1:], rules[src][k], ruleno, tag)
        ruleno = ruleno + 1
        baseRuleSet[sw] = baseRuleSet[sw] +1
        #y =  rule(ruleno, words[0][1:], rules[src][k], ruleno, " ")
  for key in SynRuleSet.keys():
    print "Switch: ",key, len(SynRuleSet[key].keys())
    for ke in SynRuleSet[key].keys():
      print SynRuleSet[key][ke].printRule()
  os.system("pause")
  '''
  return SynRuleSet, baseRuleSet


def assignPathsToRules(it,taggedPaths,n,sw,src,dsts,tags,subnet,div):
  #print "Switch:",sw, it,n
  global Ruleno
  global SynRuleSet
  global noofrules
  if len(SynRuleSet[sw].keys()) >= noofrules:
    return
  if len(dsts) == 0:
    #print "Returning"
    return

  if len(tags) == 1:
    #print "Install",src,dsts,tags[0],n,Ruleno
    random.shuffle(dsts)
    for dst,count in zip(dsts,range(0,n)):
     SynRuleSet[sw][Ruleno] = Rule(Ruleno,src,dst,Ruleno,tags[0])
     Ruleno = Ruleno + 1 
    #print Ruleno
    return
 
  if n == 1 or n == 0:
    #print "Install2",src,dsts,tags[0],n
    random.shuffle(tags)
    random.shuffle(dsts)
    SynRuleSet[sw][Ruleno] = Rule(Ruleno,src,dsts[0],Ruleno,tags[0])
    Ruleno = Ruleno + 1 
    return
  if n >= len(dsts):
    #print "Install3",src,dsts,tags[0],n
    for dst in dsts:
      SynRuleSet[sw][Ruleno] = Rule(Ruleno,src,dst,Ruleno,tags[0])
      Ruleno = Ruleno + 1 
    return

  if sw == -1:
    print "HaHa: Install",src,dsts,tags[0],n
    return

  sameNextHopTags = {}
  #print "tags: ", tags, len(tags)
  count = 0
  for tag in tags:
    #print tag
    count = count + 1
    nexthop = getNextHop(taggedPaths,tag,it+1)  
    if nexthop == -1:
      print "____________________________"
    if nexthop not in sameNextHopTags.keys():
      sameNextHopTags[nexthop] = list()  
    sameNextHopTags[nexthop].append(tag)
    if len(sameNextHopTags.keys()) > n or count > 10000:
      break	
  noofrulespernexthop = int(math.ceil(n/len(sameNextHopTags.keys())))

  #print "No of Uplinks: ",len(sameNextHopTags.keys())
  if noofrulespernexthop > 0 and n%len(sameNextHopTags.keys())!=0:
    noofrulespernexthop = noofrulespernexthop + 1 
  if noofrulespernexthop == 0:
    noofrulespernexthop = 1
  
  division = 1
  while math.pow(2,division) < len(sameNextHopTags.keys()):
    division = division * 2
  div = div + division
  #print "no of division: ",division, " total dst: ",len(dsts)    
  subnetdivision = subnet.subnet(div)
  su = 0
  subnetdsts = {} 
  for sub in subnetdivision:
    subnetdsts[sub] = list()
    for dst in dsts:
      if dst in sub:
        subnetdsts[sub].append(dst)
    #print "Len:",sub,len(subnetdsts[sub])  
    su = su + len(subnetdsts[sub])
    if len(subnetdsts[sub]) == 0:
      del subnetdsts[sub]
  k = 0
  #print sorted(subnetdsts.keys(),key=lambda x:len(subnetdsts[x]),reverse=True)
  #print "I see: ",it,len(sameNextHopTags.keys())
  l = sameNextHopTags.keys()
  random.shuffle(l)
  if len(subnetdsts.keys()) > len(sameNextHopTags.keys()):
    su = 0
    for key in sorted(subnetdsts.keys(),key=lambda x:len(subnetdsts[x]),reverse = True):
      su = su + len(subnetdsts[key])
      k = k + 1
      if k == len(sameNextHopTags.keys()):
        break
  #print "Sum: ", su
  k = 0
  for key,key1 in zip(l,sorted(subnetdsts.keys(),key=lambda x:len(subnetdsts[x]),reverse = True)):
    #if k + noofrulespernexthop >= n:
    #  if k < n:
    #    assignPathsToRules(it+1,taggedPaths,noofrulespernexthop,sw,src,subnetdsts[key1],sameNextHopTags[key],key1,div)
    #  break
    noofrulespernexthop = int(math.ceil((len(subnetdsts[key1])*(n))/su))  + 1
    assignPathsToRules(it+1,taggedPaths,noofrulespernexthop,sw,src,subnetdsts[key1],sameNextHopTags[key],key1,div)
    k = k + noofrulespernexthop
    
  #print "Iter:",it, "Switch: ", "Total to ins: ",n, "noofrules passed : ",k 

def getNextHop(taggedPaths,tag,index):

  if tag not in taggedPaths.keys():
    print "[Error]: tag:" + str(tag) + str(len(tag)) + "not found in the taggedPaths"
    return 
  path = taggedPaths[tag]
  if index == len(path):
      return -1 
  return path[index]


  
     
  


if __name__ == "__main__":
    main()





