from netaddr import IPNetwork
from netaddr import IPAddress
from ruleOffload import rule as Rule  
import math

ruleToRect = {}
OverLappingRules  = 2
RatioOverLappingRules = 0.4


defaultSet   = []
partitionSet = {}
rootRulesSet = {}
ruleCount = 0
kcount = 0

def getDefaultRules(inputSet):
  
  ruletable = {}
  #Transform the input for defaultRules()
  
  global kcount
  kcount = 0
  for partitionID in inputSet:
    
    if partitionID not in ruletable:
        ruletable[partitionID] = []
    
    for rule in inputSet[partitionID]:
      kcount  = kcount + 1
      newRule = {}
      newRule['nw_src'] = IPNetwork(inputSet[partitionID][rule].srcIP)
      newRule['nw_dst'] = IPNetwork(inputSet[partitionID][rule].dstIP)
      newRule['priority'] = inputSet[partitionID][rule].priority
      newRule['tag'] = inputSet[partitionID][rule].tag
      newRule['number'] = inputSet[partitionID][rule].number
      newRule['pid'] = partitionID

      ruletable[partitionID].append(newRule)
  #print "inputSet",kcount
  count = 0
  for k in ruletable:
    for kk in ruletable[k]:
      count =count +1
      
  #print "inputSet",count
  
      
  defaultRules(ruletable)
  
  newRootRulesSet = {}
  
  for pid in rootRulesSet:
    if pid not in newRootRulesSet:
      newRootRulesSet[pid] = []
    for rule in rootRulesSet[pid]:
      newRule = Rule(rule['number'],rule['nw_src'],rule['nw_dst'],\
        rule['priority'],rule['tag'])
      newRootRulesSet[pid].append(newRule)
  
  newPartitionSet = {}
  for pid in partitionSet:
    if pid not in newPartitionSet:
      newPartitionSet[pid] = []
  #  print partitionSet[pid] 
    for rule in partitionSet[pid]:
      
      newRule = Rule(rule['number'],rule['nw_src'],rule['nw_dst'],\
        rule['priority'],rule['tag'])
      newPartitionSet[pid].append(newRule)  
 
  newdefaultSet = {}
  for entry in defaultSet:
    newRule = Rule(None,entry[0]['nw_src'],entry[0]['nw_dst'],\
        entry[0]['priority'],None)
    if newRule not in newdefaultSet:
      newdefaultSet[newRule] = entry[1]
    else: print "ERROR already exists"
  
 
  return newPartitionSet,newRootRulesSet,newdefaultSet,ruleCount
  
  

def defaultRules(ruleSet):

  #create a mapping between ip in dot format to their int value
  ruleSetValue = {}

  global defaultSet
  global partitionSet
  global rootRulesSet
  global ruleToRect
  global ruleCount
  
  defaultSet   = []
  partitionSet = {}
  rootRulesSet = {}
  ruleToRect = {}
  ruleCount = 0

  for k in ruleSet:
    
    for rule in ruleSet[k]:
      oldSize =len(ruleToRect)
      if ((rule['nw_src'].value,rule['nw_src'].last),(rule['nw_dst'].value,rule['nw_dst'].last)) in ruleToRect:
        print "old ",ruleToRect[((rule['nw_src'].value,rule['nw_src'].last),(rule['nw_dst'].value,rule['nw_dst'].last))]
        print "new",rule
      ruleToRect[((rule['nw_src'].value,rule['nw_src'].last),(rule['nw_dst'].value,rule['nw_dst'].last))]  = rule
      if oldSize == len(ruleToRect):
        print "DUPLICATE RULE"
      
  #print len(ruleToRect)  
  r=Rect((0,0xFFFFFFFF+1),(0,0xFFFFFFFF+1))
  
  computeDefaultRules(r,ruleToRect.keys())
#  print "input rules",len(ruleToRect.keys())
  tmp = 0
  for p in rootRulesSet:
    tmp = tmp + len(rootRulesSet[p])
  #print "rootRulesSet " , tmp    
  
  pt = 0
  for p in partitionSet:
    pt = pt + len(partitionSet[p])
  #print "partitionSet " , pt    
  #print "Default Rules at Root",ruleCount
#  if pt+tmp != kcount :
#    print ruleSet







def computeDefaultRules(rec, ruleSet):


  resizedRec = {}
  buckets =  []  
  global defaultSet
  global partitionSet
  global rootRulesSet
  global ruleToRect
  global ruleCount
  cannotSplit = False
  resizedRec[0] = Rect((rec.left,(rec.left + rec.right)/2 ),\
    (rec.bottom,(rec.bottom + rec.top)/2))
  #print "rec",resizedRec[0].left,  resizedRec[0].right
  resizedRec[1] = Rect((rec.left,(rec.left + rec.right)/2),\
    ((rec.bottom + rec.top)/2,rec.top))
  resizedRec[2] = Rect(((rec.left + rec.right)/2,rec.right),\
    (rec.bottom,(rec.bottom + rec.top)/2))
  resizedRec[3] = Rect(((rec.left + rec.right)/2,rec.right),\
    ((rec.bottom + rec.top)/2,rec.top))

  for k in range(len(resizedRec)):
    buckets.append([])
    

  for k in ruleSet:
    rtn =  getRuleRec(k, resizedRec)
    if rtn == None:
      # Merge buckets / dont split
      mergeRect(k,buckets,resizedRec)  
    else:
      buckets[rtn].append(k)
  
  zeroAreaRecs = 0 
  for k in range(len(resizedRec)):
    if isAreaZero(resizedRec[k]) == True:
      zeroAreaRecs = zeroAreaRecs + 1
  # rec can not be split further    
  if  zeroAreaRecs ==3:
    cannotSplit = True
    print "cannotSplit"
   
       
  

  #  check for overlap    
  partitionsTable  ={}
  for rulebucket in buckets:
    if len(rulebucket) != 0:
      partitionsTable[buckets.index(rulebucket)] = checkOverlap(rulebucket)    

  # merges the buckets which belong to same partiton
  # it also resized the rectangles
  
  mergeBuckets(partitionsTable,buckets,resizedRec) 
     

  for rulebucket in buckets:
    if len(rulebucket) != 0:
      #none empty buckets

      partitions = partitionsTable[buckets.index(rulebucket)]
      if len(partitions) > 1: 
        #subdivide
        #print "sub dividing"
        
        rulePerPartition = []
        #print partitions
        for p in partitions:
          rulePerPartition.append((len(partitions[p]),p))

        rulePerPartition = sorted(rulePerPartition,  key=lambda tup: tup[0])
        primary = rulePerPartition[-1][0]
        primaryPartition = rulePerPartition[-1][1]
        other = 0
        for i in range(len(rulePerPartition)-1):
          other = other + rulePerPartition[i][0]
          
        #FIXME it will fail if there are redundant rule
        #  a low priority rule fully overlapped by a high priority rule

        #if number of primary rules == 1 so no need to install default rule
        if primary == 1:
          primary = 0
        if float(primary)/float(primary+other) >= RatioOverLappingRules :
          #print "rule  RATIO is high" , primary, other, \
          #  partitions[rulePerPartition[-1][1]]
          offloaded_rules = []
          for rulekey in partitions[rulePerPartition[-1][1]]:
            partitionID = ruleToRect[rulekey]["pid"]
            if partitionID not in partitionSet:
              partitionSet[partitionID] = []
            partitionSet[partitionID].append(ruleToRect[rulekey])
            
            offloaded_rules.append(ruleToRect[rulekey]['number'])
            
            #print "offloaded ,nw_src=",ruleToRect[rulekey]['nw_src']\
            #  ,"nw_dst=",ruleToRect[rulekey]['nw_dst'], "priority = ",\
            #  ruleToRect[rulekey]['priority'],",tag = ", ruleToRect[rulekey]['tag']
            

          srcIP, dstIP = recToIP(resizedRec[buckets.index(rulebucket)])
          tmpDefaultRule = {"nw_src":srcIP, 'nw_dst':dstIP , "priority":10}
          if tmpDefaultRule not in defaultSet:
            defaultSet.append((tmpDefaultRule,offloaded_rules))
            offloaded_rules = []
          else:
            print "ERROR default rule already exists"
          ruleCount = ruleCount + 1  

          for rulekey in partitions:
            if rulekey != primaryPartition:
              for ruleEntry in partitions[rulekey]:
                partitionID = ruleToRect[ruleEntry]["pid"]
                if partitionID not in rootRulesSet:
                  rootRulesSet[partitionID] = []
                rootRulesSet[partitionID].append(ruleToRect[ruleEntry])
                
                #print "root ,nw_src=",ruleToRect[ruleEntry]['nw_src']\
                #  ,"nw_dst=",ruleToRect[ruleEntry]['nw_dst'], "priority = ",\
                #  ruleToRect[ruleEntry]['priority'],",tag = ", ruleToRect[ruleEntry]['tag']  
                
        else:
          # recursive call
          if cannotSplit == False:
            computeDefaultRules(resizedRec[buckets.index(rulebucket)] ,rulebucket)
          else:
            # can not split 
            # put 
            for p in partitions:
              rulePerPartition.append((len(partitions[p]),p))
            sorted(rulePerPartition)
            primary = rulePerPartition[-1][0]
            primaryPartition = None

            #if primary has more than one rule
            if primary != 1: 
              primaryPartition = rulePerPartition[-1][1]
              offloaded_rules = []
              for rulekey in partitions[rulePerPartition[-1][1]]:
                partitionID = ruleToRect[rulekey]["pid"]
                if partitionID not in partitionSet:
                  partitionSet[partitionID] = []
                partitionSet[partitionID].append(ruleToRect[rulekey])
                offloaded_rules.append(ruleToRect[rulekey]['number'])
                
                #print "offloaded ,nw_src=",ruleToRect[rulekey]['nw_src']\
                #  ,"nw_dst=",ruleToRect[rulekey]['nw_dst'], "priority = ",\
                #  ruleToRect[rulekey]['priority'],",tag = ", ruleToRect[rulekey]['tag']
                
                
              srcIP,dstIP = recToIP(resizedRec[buckets.index(rulebucket)])
              tmpDefaultRule = {"nw_src":srcIP, 'nw_dst':dstIP , "priority":10}
              if tmpDefaultRule not in defaultSet:
                defaultSet.append((tmpDefaultRule,offloaded_rules))
                offloaded_rules = []
              else:
                print "ERROR default rule already exists" 
              
              ruleCount = ruleCount + 1  

            for rulekey in partitions:
              if rulekey != primaryPartition:
                for ruleEntry in partitions[rulekey]:
                  partitionID = ruleToRect[ruleEntry]["pid"]
                  if partitionID not in rootRulesSet:
                    rootRulesSet[partitionID] = []
                  rootRulesSet[partitionID].append(ruleToRect[ruleEntry])
                  
                  #print "root ,nw_src=",ruleToRect[ruleEntry]['nw_src']\
                  #  ,"nw_dst=",ruleToRect[ruleEntry]['nw_dst'], "priority = ",\
                  #  ruleToRect[ruleEntry]['priority'],",tag = ", ruleToRect[ruleEntry]['tag']         
                  


            '''        
            for rulekey in partitions:
              for ruleEntry in partitions[rulekey]:
                partitionID = ruleToRect[ruleEntry]["pid"]
                if partitionID not in rootRulesSet:
                  rootRulesSet[partitionID] = []
                rootRulesSet[partitionID].append(ruleToRect[ruleEntry])
            '''

      else:
        if len(partitions.items()[0][1]) > 1:
          # more than one rule with same next hop
          #print "more than one rule with same next hop"
          offloaded_rules = []
          for rulekey in partitions.items()[0][1]:
            partitionID = ruleToRect[rulekey]["pid"]
            if partitionID not in partitionSet:
              partitionSet[partitionID] = []
            partitionSet[partitionID].append(ruleToRect[rulekey])
            offloaded_rules.append(ruleToRect[rulekey]['number'])
            
            #print "offloaded ,nw_src=",ruleToRect[rulekey]['nw_src']\
            #  ,"nw_dst=",ruleToRect[rulekey]['nw_dst'], "priority = ",\
            #  ruleToRect[rulekey]['priority'],",tag = ", ruleToRect[rulekey]['tag']
            
          ruleCount = ruleCount + 1
          srcIP,dstIP = recToIP(resizedRec[buckets.index(rulebucket)])

          tmpDefaultRule = {"nw_src":srcIP, 'nw_dst':dstIP , "priority":10}
          if tmpDefaultRule not in defaultSet:
            defaultSet.append((tmpDefaultRule,offloaded_rules))
            offloaded_rules = []
          else:
            print "ERROR default rule already exists" 
              

          r =resizedRec[buckets.index(rulebucket)]
        #  print r.left,r.right,r.bottom,r.top
          
        else:
          #only one rule in the partition 
          rulekey= partitions.items()[0][1]
          partitionID = ruleToRect[rulekey[0]]["pid"]
          if partitionID not in rootRulesSet:
            rootRulesSet[partitionID] = []
          rootRulesSet[partitionID].append(ruleToRect[rulekey[0]])
          
          #print "root ,nw_src=",ruleToRect[rulekey[0]]['nw_src']\
          #,"nw_dst=",ruleToRect[rulekey[0]]['nw_dst'], "priority = ",\
          #ruleToRect[rulekey[0]]['priority'],",tag = ", ruleToRect[rulekey[0]]['tag']
          
        
#        print "--->",partitions
        #print "Done with partitioning "
        #TODO merge Bucket  
  
'''  
     merges the buckets which belong to same partiton
       # it also resized the rectangles
'''      
def mergeBuckets(partitionsTable,buckets, resizedRec):

  for bucketID in partitionsTable.keys():
    if bucketID in partitionsTable and bucketID != 3:  
      if len(partitionsTable[bucketID].keys())== 1:
        
        partitionID = partitionsTable[bucketID].keys()[0]
        targetPartition = None
        if bucketID == 0:
          Flag = 0
          if 1 in partitionsTable and len(partitionsTable[1].keys())== 1:
            if partitionID == partitionsTable[1].keys()[0]:
              targetPartition = 1
              Flag = 1
          if 2 in partitionsTable and len(partitionsTable[2].keys())== 1 and Flag != 1:
            if partitionID == partitionsTable[2].keys()[0]:
              targetPartition = 2 
        else:
          if 3 in partitionsTable and len(partitionsTable[3].keys())== 1:
            if partitionID == partitionsTable[3].keys()[0]:
              targetPartition = 3
        if targetPartition != None:
          # merging two bucktes
          partitionsTable[bucketID][partitionID].\
              extend(partitionsTable[targetPartition][partitionID])
          partitionsTable[targetPartition]= {}

          buckets[bucketID].extend(buckets[targetPartition])
          buckets[targetPartition]= {}
          #Resizing the rectangles #TODO verfiy this
          resizedRec[bucketID].top = resizedRec[targetPartition].top
          resizedRec[bucketID].right = resizedRec[targetPartition].right
          # destroying empty rectangle
          resizedRec[targetPartition].bottom = resizedRec[targetPartition].top
          resizedRec[targetPartition].left = resizedRec[targetPartition].right     
          k =  targetPartition    
          k =  bucketID    

          
          
          
def recToIP(rec):
  
  srcIP = IPAddress(rec.left)
  netmask = 32-int(math.log(rec.right-rec.left,2))
  srcIP = srcIP.__str__()+"/"+str(netmask)
  dstIP = IPAddress(rec.bottom)
  netmask = 32-int(math.log(rec.top -rec.bottom,2))
  dstIP = dstIP.__str__()+"/"+str(netmask)
  srcIP = IPNetwork(srcIP)
  dstIP = IPNetwork(dstIP)
  return srcIP,dstIP
  


def mergeRect(rule,buckets, resizedRec):
  p1 = None
  p2 = None
  
  for k in range(len(resizedRec)):
    if isInRec((rule[0][0],rule[1][0]) , resizedRec[k]):
      if p1 != None:
        print "ERROR"
      p1 = k
    if isInRec((rule[0][1],rule[1][1]) , resizedRec[k]):
      if p2 != None:
        print "ERROR"
      p2 = k
  primaryRec = p1
  otherRec = None
  if p1 == 0 and p2 ==3: otherRec = [1,2,3]
  else:
    if (resizedRec[p1].right - resizedRec[p1].left) == (resizedRec[p2].right -resizedRec[p2].left) and \
         (resizedRec[p1].top - resizedRec[p1].bottom) == (resizedRec[p2].top -resizedRec[p2].bottom):
      otherRec = [p2]
    else:
      otherRec = []
      for k in range(len(resizedRec)):
        if not isAreaZero(resizedRec[k]):
          otherRec.append(k)
      otherRec = sorted(otherRec)
      primaryRec = otherRec.pop(0)
          

  for rec in otherRec:
   
    buckets[primaryRec].extend(buckets[rec])
    buckets[rec]= {}
    #Resizing the rectangles #TODO verfiy this
    if resizedRec[primaryRec].top < resizedRec[rec].top:
      resizedRec[primaryRec].top = resizedRec[rec].top
    if resizedRec[primaryRec].right < resizedRec[rec].right:
      resizedRec[primaryRec].right = resizedRec[rec].right
    # destroying empty rectangle
    resizedRec[rec].bottom = resizedRec[rec].top
    resizedRec[rec].left = resizedRec[rec].right  
    
    # puting the rule in bucket

  buckets[primaryRec].append(rule)

'''
return rules for each distinct partition      

'''
def checkOverlap(ruleBucket):
  partitions = {}
  
  for rule in ruleBucket:
    if ruleToRect[rule]['pid'] not in partitions:
      partitions[ruleToRect[rule]['pid']] = []
    partitions[ruleToRect[rule]['pid']].append(rule)
    
  return partitions
'''
  Return None if rule can not be but in one rectangle 
  else bucket id
    1  |  3
   ----+---- 
    0  |  2
  
'''   
   
def getRuleRec(rule, resizedRec) : 
  
  tmp = []
  for k in range(len(resizedRec)):
    if isInRec((rule[0][0],rule[1][0]) , resizedRec[k]) \
      and isInRec((rule[0][1],rule[1][1]) , resizedRec[k]):
      tmp.append(k)
  if len(tmp) == 1:
    return tmp[0]
  return None


def isAreaZero(rec):

  if rec.left == rec.right:
    return True
  if rec.top == rec.bottom:
    return True
    
  return False
  
  
def isInRec(point , r):
  if point[0] < r.left or point[0] >= r.right:
    return False
  if point[1] < r.bottom or point[1] >= r.top:
    return False
  return True  
  
class Rect(object):
  def __init__(self, p1, p2): 
    '''Store the top, bottom, left and right values for points 
       p1 and p2 are the (corners) in either order
       src is on x axis
    '''
    self.left   = p1[0]
    self.right  = p1[1]

    self.top    = p2[1]
    self.bottom = p2[0]    
    
              
def createCoverRect(ruleSet):
  
  for k in ruleSet:
  
      maxpoint = (max(c,key=lambda item:item[0])[0],max(c,key=lambda item:item[1])[1])    
  
  if len(ruleSet) == 1:

    minpoint = (min(c,key=lambda item:item[0])[0],min(c,key=lambda item:item[1])[1])
  

  
  
