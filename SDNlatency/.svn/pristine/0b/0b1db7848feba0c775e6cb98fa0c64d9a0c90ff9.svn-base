import networkx as nx
from topoManager import *
import fatTree
import tier2
from TrafficMatrix import *
from binPacking import *
from time import *
#from ciscoLatencyModel import *
#from latencyModel import *
#import matplotlib.pyplot as plt




def main():

  #topoo = tier2.Tier2(n_cores=2, n_edges=20, hostPerEdge=20, serverUplink=1000, edgeUplink = 1000*10)
  k_fatree = 8
  topoo = fatTree.FatTree(k_fatree, serverUplink=1000, edgeUplink = 1000, aggUplink = 1000)
  topoMgr = TopoManager()
  topoMgr.addRawGraph(topoo.topo)
 # ciscolat = ciscoBurstModel()
  #bcmlat = bcmBurstModel()
  print "Total hosts ",len(topoMgr.hosts)
  print "ToR switches ", len(topoMgr.S_ToR )
  print len(topoMgr.hosts)/len(topoMgr.S_ToR)
  allpaths = allShortestPath(topoMgr)
  
  #cisco = open('./microTELatency_cisco.txt','w')
  bcm = open('./microTELatency_bcm.txt','w')

  i = 0

  for i in range(50):
    trafficMatrix = TrafficMatrix(len(topoMgr.S_ToR), len(topoMgr.hosts)/len(topoMgr.S_ToR) , bw=1000, factor = 1,k= k_fatree/2 ) #len(t.hosts)/len(t.S_ToR)

    bp = BinPacking(allpaths,topoMgr)
    t1 =time()
    matrix =trafficMatrix.GetZipfArray()
    t2 = time()
#    print "time ",t2-t1
#    print matrix.max(),matrix.sum()
    bp.binPacker(matrix)
    t1 = time()
#    print "time ",t1-t2
    microTE_util = topoMgr.maxUtil(1000, 1000, 1000)
    microTE_rules, typ = topoMgr.maxRules()
#    print matrix.max(),matrix.sum()
    topoMgr.resetLinkCap(1000,1000,1000)  

    bp.binPacker_NMaxEnt(matrix,20)
    t2 = time()
#    print "time ",t2-t1

    print microTE_util,microTE_rules,typ,topoMgr.maxUtil(1000, 1000, 1000), topoMgr.maxRules()
    microTE_rules_2, typ_2 = topoMgr.maxRules()
    #cisco.write( str(i)+" Cisco"+" MircoTE: " + str(microTE_rules)+ " " + str(ciscolat.getBurstComplTime_SamePrio(int(microTE_rules)))+ " MicroTE+MaxRule: "+ str( microTE_rules_2) + " "+str( ciscolat.getBurstComplTime_SamePrio(int(microTE_rules_2)))+"\n")
    #bcm.write( str(i)+" BCM"+" MircoTE: "+ str(microTE_rules) + " "+ str(bcmlat.getBurstCompletionTime(int(microTE_rules))) +" MicroTE+MaxRule: "+str( microTE_rules_2) +" "+ str(bcmlat.getBurstCompletionTime(int(microTE_rules_2)))+"\n")
    topoMgr.resetLinkCap(1000,1000, 1000)  



# Compute all the shortest paths
#
def allShortestPath(topo):
  shortestPaths = {}

  for src in topo.S_ToR:
    for dst in topo.S_ToR:
      if src == dst:
        continue
      paths = nx.all_shortest_paths(topo.topo,src,dst)
 		    
      if src not in shortestPaths:
        shortestPaths[src]={}
        
      try:
        shortestPaths[src][dst] = [p for p in paths]
        #print topo.S_ToR
        #print src,dst, shortestPaths[src][dst]
      except nx.NetworkXNoPath:
        print "NO PATH"
        continue
  
  for k in shortestPaths.keys():
    if len(shortestPaths[k]) == 0:
      shortestPaths.pop(k)
  return	shortestPaths    




if __name__ == "__main__":
    main()






